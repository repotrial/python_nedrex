#!/usr/bin/env python

"""Tests for `python_nedrex` package."""

import pytest

import python_nedrex
from python_nedrex.core import get_node_types, get_edge_types, get_collection_attributes
from python_nedrex.exceptions import ConfigError

API_URL = "http://82.148.225.92:8123/"


def get_node_collections():
    python_nedrex.set_url_base(API_URL)
    collections = get_node_types()
    python_nedrex.config._url_base = None
    return collections


def get_edge_collections():
    python_nedrex.set_url_base(API_URL)
    collections = get_edge_types()
    python_nedrex.config._url_base = None
    return collections


@pytest.fixture
def config():
    return {
        "api_url": API_URL,
    }


@pytest.fixture
def resource(config):
    python_nedrex.set_url_base(config["api_url"])
    yield
    python_nedrex.config._url_base = None


def test_set_api_base(resource):
    assert python_nedrex.config._url_base == API_URL.rstrip("/")


class TestGetNodeTypes:
    @pytest.fixture
    def result(self, resource):
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
    def result(self, resource):
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
    def test_get_node_collection_attributes(self, resource, collection):
        expected_attributes = (
            "primaryDomainId",
            "domainIds",
            "type",
        )
        assert all(
            attr in get_collection_attributes(collection)
            for attr in expected_attributes
        )

    @pytest.mark.parametrize("collection", get_edge_collections())
    def test_get_edge_collection_attributes(self, resource, collection):
        coll_attributes = get_collection_attributes(collection)
        assert "type" in coll_attributes

        assert all(
            attr in coll_attributes
            for attr in (
                "memberOne",
                "memberTwo",
            )
        ) or all(
            attr in coll_attributes
            for attr in (
                "sourceDomainId",
                "targetDomainId",
            )
        )


class TestRoutesFailWithoutAPIUrl:
    def test_get_node_type(self):
        from python_nedrex.exceptions import ConfigError

        with pytest.raises(ConfigError):
            get_node_types()

    def test_get_edge_type(self):
        from python_nedrex.exceptions import ConfigError

        with pytest.raises(ConfigError):
            get_edge_types()
