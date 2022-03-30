#!/usr/bin/env python

"""Tests for `python_nedrex` package."""

from functools import lru_cache

import pytest
import requests

import python_nedrex
from python_nedrex.core import (
    get_edges,
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


@lru_cache(maxsize=1)
def get_node_collections():
    python_nedrex.set_url_base(API_URL)
    collections = get_node_types()
    python_nedrex.config._url_base = None
    return collections


@lru_cache(maxsize=1)
def get_edge_collections():
    python_nedrex.set_url_base(API_URL)
    collections = get_edge_types()
    python_nedrex.config._url_base = None
    return collections


@pytest.fixture
def config():
    return {"api_url": API_URL, "api_key": API_KEY}


@pytest.fixture
def set_api_key(config):
    python_nedrex.set_api_key(config["api_key"])
    yield
    python_nedrex.config._api_key = None


@pytest.fixture
def set_base_url(config):
    python_nedrex.set_url_base(config["api_url"])
    yield
    python_nedrex.config._url_base = None


def test_set_api_base(set_base_url):
    assert python_nedrex.config._url_base == API_URL.rstrip("/")


class TestGetNodeTypes:
    @pytest.fixture
    def result(self, set_base_url):
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
    def result(self, set_base_url):
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
    def test_get_node_collection_attributes(self, set_base_url, collection):
        expected_attributes = ("primaryDomainId", "domainIds", "type")
        coll_attributes = get_collection_attributes(collection)
        assert all(attr in coll_attributes for attr in expected_attributes)

    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_edge_collection_attributes(self, set_base_url, collection):
        coll_attributes = get_collection_attributes(collection)
        assert "type" in coll_attributes

        assert all(
            attr in coll_attributes for attr in ("memberOne", "memberTwo")
        ) or all(
            attr in coll_attributes for attr in ("sourceDomainId", "targetDomainId")
        )


class TestGetNodeIds:
    @pytest.mark.parametrize("collection", get_node_collections())
    def test_get_node_ids(self, set_base_url, collection):
        if collection == "drug":
            with pytest.raises(ConfigError):
                get_node_ids(collection)
        else:
            assert get_node_ids(collection)

    def test_get_drugs_works_with_api_key(self, set_base_url, set_api_key):
        assert get_node_ids("drug")

    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_node_ids_fails_for_edges(self, set_base_url, collection):
        with pytest.raises(NeDRexError):
            get_node_ids(collection)


class TestGetEdgeRoutes:
    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_all_edges(self, set_base_url, collection):
        if collection in (
            "drug_has_target",
            "gene_associated_with_disorder",
        ):
            with pytest.raises(ConfigError):
                get_edges(collection, limit=1_000)
        else:
            assert isinstance(get_edges(collection, limit=1_000), list)


class TestGetNodeRoutes:
    @pytest.mark.parametrize("collection", get_node_collections())
    def test_get_all_nodes(self, set_base_url, collection):
        if collection == "drug":
            with pytest.raises(ConfigError):
                get_nodes(collection)
        else:
            assert isinstance(get_nodes(collection), list)

    def test_get_specific_nodes(self, set_base_url):
        nodes = get_nodes("disorder", node_ids=["mondo.0000001"])
        assert isinstance(nodes, list)
        assert len(nodes) == 1
        assert nodes[0]["primaryDomainId"] == "mondo.0000001"

    def test_get_drugs_with_api_key(self, set_base_url, set_api_key):
        nodes = get_nodes("drug")
        assert isinstance(nodes, list)

    def test_get_specific_attributes(self, set_base_url):
        nodes = get_nodes("disorder", attributes=["displayName"])
        assert isinstance(nodes, list)
        assert [set(i.keys()) == {"primaryDomainId", "displayName"} for i in nodes]

    def test_get_specific_attribute_and_nodes(self, set_base_url):
        nodes = get_nodes(
            "disorder", attributes=["displayName"], node_ids=["mondo.0000001"]
        )
        assert isinstance(nodes, list)
        assert len(nodes) == 1
        assert nodes[0] == {
            "displayName": "disease or disorder",
            "primaryDomainId": "mondo.0000001",
        }

    def test_pagination(self, set_base_url):
        nodes = get_nodes("genomic_variant", limit=1000, offset=1000)
        assert isinstance(nodes, list)
        assert len(nodes) == 1000

    def test_consistent_pagination(self, set_base_url):
        offset = 1234
        limit = 69

        nodes = get_nodes("genomic_variant", limit=limit, offset=offset)

        for _ in range(10):
            nodes_repeat = get_nodes("genomic_variant", limit=limit, offset=offset)
            assert nodes_repeat == nodes


class TestDisorderRoutes:
    def test_search_by_icd10(self, set_base_url):
        result = search_by_icd10("I52")
        assert result == []


class TestRoutesFailWithoutAPIUrl:
    def test_get_node_type(self):
        with pytest.raises(ConfigError):
            get_node_types()

    def test_get_edge_type(self):
        with pytest.raises(ConfigError):
            get_edge_types()
