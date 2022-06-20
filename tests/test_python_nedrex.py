#!/usr/bin/env python

"""Tests for `python_nedrex` package."""

from collections import defaultdict
from contextlib import contextmanager
from functools import lru_cache
from typing import Optional, Tuple

import pytest
import requests

import python_nedrex
from python_nedrex.core import (
    get_edges,
    iter_edges,
    iter_nodes,
    get_node_types,
    get_edge_types,
    get_collection_attributes,
    get_node_ids,
    get_nodes,
)
from python_nedrex.disorder import (
    get_disorder_ancestors,
    get_disorder_children,
    get_disorder_descendants,
    get_disorder_parents,
    search_by_icd10,
)
from python_nedrex.exceptions import ConfigError, NeDRexError


API_URL = "http://82.148.225.92:8123/"
API_KEY = requests.post(
    f"{API_URL}admin/api_key/generate", json={"accept_eula": True}
).json()


@contextmanager
def url_base():
    python_nedrex.config.set_url_base(API_URL)
    yield
    python_nedrex.config._url_base = None

@contextmanager
def api_key():
    python_nedrex.config.set_api_key(API_KEY)
    yield
    python_nedrex.config._api_key = None


@lru_cache(maxsize=10)
def get_node_collections():
    with api_key(), url_base():
        collections = get_node_types()
    return collections


@lru_cache(maxsize=10)
def get_edge_collections():
    with api_key(), url_base():
        collections = get_edge_types()
    return collections


@pytest.fixture
def config():
    return {"api_url": API_URL, "api_key": API_KEY}


@pytest.fixture
def set_api_key(config):
    with api_key():
        yield

@pytest.fixture
def set_base_url(config):
    with url_base():
        yield


def test_set_api_base(set_base_url):
    assert python_nedrex.config._url_base == API_URL.rstrip("/")


class TestGetNodeTypes:
    @pytest.fixture
    def result(self, set_base_url, set_api_key):
        result = get_node_types()
        return result

    def test_return_type(self, result):
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)

    def test_ordering(self, result):
        assert result == sorted(result)

    def test_content(self, result):
        assert "protein" in result


class TestGetEdgeTypes:
    @pytest.fixture
    def result(self, set_base_url, set_api_key):
        result = get_edge_types()
        return result

    def test_return_type(self, result):
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)

    def test_ordering(self, result):
        assert result == sorted(result)

    def test_content(self, result):
        assert "protein_encoded_by_gene" in result


class TestGetCollectionAttributes:
    @pytest.mark.parametrize("collection", get_node_collections())
    def test_get_node_collection_attributes(self, set_base_url, set_api_key, collection):
        expected_attributes = ("primaryDomainId", "domainIds", "type")
        coll_attributes = get_collection_attributes(collection)
        assert all(attr in coll_attributes for attr in expected_attributes)

    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_edge_collection_attributes(self, set_base_url, set_api_key, collection):
        # NOTE: Exclude the protein_interacts_with_protein collection because of its size.
        coll_attributes = get_collection_attributes(collection)
        assert "type" in coll_attributes

        assert all(
            attr in coll_attributes for attr in ("memberOne", "memberTwo")
        ) or all(
            attr in coll_attributes for attr in ("sourceDomainId", "targetDomainId")
        )


class TestGetNodeIds:
    @pytest.mark.parametrize("collection", get_node_collections())
    def test_get_node_ids(self, set_base_url, set_api_key, collection):
        assert get_node_ids(collection)


    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_node_ids_fails_for_edges(self, set_base_url, set_api_key, collection):
        with pytest.raises(NeDRexError):
            get_node_ids(collection)


class TestGetEdgeRoutes:
    @pytest.mark.parametrize("collection", get_edge_collections())    
    def test_return_type_get_edges(self, set_base_url, set_api_key, collection):
        edges = get_edges(collection, limit=1_000)
        assert isinstance(edges, list)

    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_edge_attributes(self, set_base_url, set_api_key, collection):
        result = get_collection_attributes(collection, include_counts=True)
        total = result['document_count']
        attr_counts = result['attribute_counts']

        assert attr_counts['type'] == total
        assert (
            (attr_counts.get('memberOne', 0) == attr_counts.get('memberTwo', 0) == total and 
              attr_counts.get('sourceDomainId', 0) == attr_counts.get('targetDomainId', 0) == 0)
              ^
            (attr_counts.get('memberOne', 0) == attr_counts.get('memberTwo', 0) == 0 and 
            attr_counts.get('sourceDomainId', 0) == attr_counts.get('targetDomainId', 0) == total)
        )

class TestGetNodeRoutes:
    @pytest.mark.parametrize("collection", get_node_collections())
    def test_get_all_nodes(self, set_base_url, set_api_key, collection):
        assert isinstance(get_nodes(collection), list)

    def test_get_specific_nodes(self, set_base_url, set_api_key):
        nodes = get_nodes("disorder", node_ids=["mondo.0000001"])
        assert isinstance(nodes, list)
        assert len(nodes) == 1
        assert nodes[0]["primaryDomainId"] == "mondo.0000001"

    def test_get_drugs_with_api_key(self, set_base_url, set_api_key):
        nodes = get_nodes("drug")
        assert isinstance(nodes, list)

    def test_get_specific_attributes(self, set_base_url, set_api_key):
        nodes = get_nodes("disorder", attributes=["displayName"])
        assert isinstance(nodes, list)
        assert [set(i.keys()) == {"primaryDomainId", "displayName"} for i in nodes]

    def test_get_specific_attribute_and_nodes(self, set_base_url, set_api_key):
        nodes = get_nodes(
            "disorder", attributes=["displayName"], node_ids=["mondo.0000001"]
        )
        assert isinstance(nodes, list)
        assert len(nodes) == 1
        assert nodes[0] == {
            "displayName": "disease or disorder",
            "primaryDomainId": "mondo.0000001",
        }

    def test_pagination(self, set_base_url, set_api_key):
        nodes = get_nodes("genomic_variant", limit=1000, offset=1000)
        assert isinstance(nodes, list)
        assert len(nodes) == 1000

    def test_consistent_pagination(self, set_base_url, set_api_key):
        offset = 1234
        limit = 69

        nodes = get_nodes("genomic_variant", limit=limit, offset=offset)

        for _ in range(10):
            nodes_repeat = get_nodes("genomic_variant", limit=limit, offset=offset)
            assert nodes_repeat == nodes


class TestDisorderRoutes:
    def test_search_by_icd10(self, set_base_url, set_api_key):
        result = search_by_icd10("I52")
        assert result == []


class TestRoutesFailWithoutAPIUrl:
    def test_get_node_type(self):
        with pytest.raises(ConfigError):
            get_node_types()

    def test_get_edge_type(self):
        with pytest.raises(ConfigError):
            get_edge_types()
