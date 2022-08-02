from typing import Any as _Any
from typing import Dict as _Dict
from typing import Generator as _Generator
from typing import List as _List
from typing import Optional as _Optional

from nedrex import config as _config
from nedrex._common import check_pagination_limit as _check_pagination_limit
from nedrex._common import check_response as _check_response
from nedrex._common import get_pagination_limit as _get_pagination_limit
from nedrex._common import http as _http


def get_effect_choices() -> _List[str]:
    """Gets a list of possible `effect` values for variant-disorder edges

    Returns
    -------
    list[str]
        A list of possible values in the `effect` array attribute of
        variant-disorder associations.
    """
    url = f"{_config.url_base}/variants/get_effect_choices"
    resp = _http.get(url, headers={"x-api-key": _config.api_key})
    result: _List[str] = _check_response(resp)
    return result


def get_review_status_choices() -> _List[str]:
    """Gets a list of possible `reviewStatus` values for variant-disorder edges

    Returns
    -------
    list[str]
        A list of possible values in the `reviewStatus` (string) attribute of
        variant-disorder associations.
    """
    url = f"{_config.url_base}/variants/get_review_choices"
    resp = _http.get(url, headers={"x-api-key": _config.api_key})
    result: _List[str] = _check_response(resp)
    return result


# pylint: disable=R0913
def get_variant_disorder_associations(
    variant_ids: _Optional[_List[str]] = None,
    disorder_ids: _Optional[_List[str]] = None,
    review_status: _Optional[_List[str]] = None,
    effect: _Optional[_List[str]] = None,
    limit: _Optional[int] = None,
    offset: int = 0,
) -> _List[_Dict[str, _Any]]:
    """Gets variant-disorder associations based on requested filtering

    Parameters
    ----------
    variant_ids : list[str], optional
        A list of variant IDs to filter on. The default, None, does no variant
        ID-based filtering
    disorder_ids : list[str], optional
        A list of disorder IDs to filter on. The default, None, does no
        disorder ID-based filtering
    review_status : list[str], optional
        A list of review statuses to filter on. The default, None, returns only
        associations with "practical guideline" or "reviewed by expert panel"
        as the review status
    effect : list[str], optional
        A list of effect values to filter on. The default, None, returns only
        associations with "Pathogenic", "Likely pathogenic", or
        "Pathogenic/Likely pathogenic" as a listed effect
    limit : int, optional
        The maximum number of records to return. The default, None, uses the
        API's "pagination_max" value to set the limit
    offset : int, optional
        The offset to use before returning records. The default is 0

    Returns
    -------
    list[dict[str, Any]]
        A list of variant-disorder association records matching the specified
        query
    """
    max_limit = _get_pagination_limit()
    if isinstance(limit, int):
        _check_pagination_limit(limit, max_limit)
    else:
        limit = max_limit

    params = {
        "variant_id": variant_ids,
        "disorder_id": disorder_ids,
        "review_status": review_status,
        "effect": effect,
        "limit": limit,
        "offset": offset,
    }

    url = f"{_config.url_base}/variants/get_variant_disorder_associations"
    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: _List[_Dict[str, _Any]] = _check_response(resp)
    return result


# pylint: enable=R0913


def iter_variant_disorder_associations(
    variant_ids: _Optional[_List[str]] = None,
    disorder_ids: _Optional[_List[str]] = None,
    review_status: _Optional[_List[str]] = None,
    effect: _Optional[_List[str]] = None,
) -> _Generator[_Dict[str, _Any], None, None]:
    """Iterator over variant-disorder associations

    Parameters
    ----------
    variant_ids : list[str], optional
        A list of variant IDs to filter on. The default, None, does no variant
        ID-based filtering
    disorder_ids : list[str], optional
        A list of disorder IDs to filter on. The default, None, does no
        disorder ID-based filtering
    review_status : list[str], optional
        A list of review statuses to filter on. The default, None, returns only
        associations with "practical guideline" or "reviewed by expert panel"
        as the review status
    effect : list[str], optional
        A list of effect values to filter on. The default, None, returns only
        associations with "Pathogenic", "Likely pathogenic", or
        "Pathogenic/Likely pathogenic" as a listed effect

    Yields
    ------
    dict[str, Any]
        A variant-disorder association matching the requested filtering
    """
    max_limit = _get_pagination_limit()
    offset = 0

    kwargs = {
        "variant_ids": variant_ids,
        "disorder_ids": disorder_ids,
        "review_status": review_status,
        "effect": effect,
        "limit": max_limit,
        "offset": offset,
    }

    while True:
        results = get_variant_disorder_associations(**kwargs)
        if len(results) == 0:
            return
        yield from results

        offset += max_limit
        kwargs["offset"] = offset


def get_variant_gene_associations(
    variant_ids: _Optional[_List[str]] = None,
    gene_ids: _Optional[_List[str]] = None,
    limit: _Optional[int] = None,
    offset: int = 0,
) -> _List[_Dict[str, _Any]]:
    """Gets variant-gene associations based on requested filtering

    Parameters
    ----------
    variant_ids : list[str], optional
        A list of variant IDs to filter on. The default, None, does no variant
        ID-based filtering
    gene_ids : list[str], optional
        A list of gene IDs to filter on. The default, None, does no gene
        ID-based filtering
    limit : int, optional
        The maximum number of records to return. The default, None, uses the
        API's "pagination_max" value to set the limit
    offset : int, optional
        The offset to use before returning records. The default is 0

    Returns
    -------
    list[dict[str, Any]]
        A list of variant-gene association records matching the specified
        query
    """

    max_limit = _get_pagination_limit()
    if isinstance(limit, int):
        _check_pagination_limit(limit, max_limit)
    else:
        limit = max_limit

    params = {"variant_id": variant_ids, "gene_id": gene_ids, "offset": offset, "limit": limit}

    url = f"{_config.url_base}/variants/get_variant_gene_associations"
    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: _List[_Dict[str, _Any]] = _check_response(resp)
    return result


def iter_variant_gene_associations(
    variant_ids: _Optional[_List[str]] = None, gene_ids: _Optional[_List[str]] = None
) -> _Generator[_Dict[str, _Any], None, None]:
    """Iterator over variant-gene associations

    Parameters
    ----------
    variant_ids : list[str], optional
        A list of variant IDs to filter on. The default, None, does no variant
        ID-based filtering
    gene_ids : list[str], optional
        A list of gene IDs to filter on. The default, None, does no gene
        ID-based filtering

    Yields
    ------
    dict[str, Any]
        A variant-gene association matching the requested filtering
    """
    max_limit = _get_pagination_limit()
    offset = 0

    kwargs = {"variant_ids": variant_ids, "gene_ids": gene_ids, "limit": max_limit, "offset": offset}

    while True:
        results = get_variant_gene_associations(**kwargs)
        if len(results) == 0:
            return
        yield from results

        offset += max_limit
        kwargs["offset"] = offset


def get_variant_based_disorder_associated_genes(
    disorder_id: str,
    review_status: _Optional[_List[str]] = None,
    effect: _Optional[_List[str]] = None,
) -> _List[str]:
    """Gets a list of genes associated with a disorder using variant relations

    Parameters
    ----------
    disorder_id : str
        The disorder ID to get associated genes for
    review_status : list[str], optional
        A list of review statuses to filter on. The default, None, returns only
        associations with "practical guideline" or "reviewed by expert panel"
        as the review status
    effect : list[str], optional
        A list of effect values to filter on. The default, None, returns only
        associations with "Pathogenic", "Likely pathogenic", or
        "Pathogenic/Likely pathogenic" as a listed effect

    Returns
    -------
    list[str]
        A list of genes associated with the query disorder
    """
    params = {"disorder_id": disorder_id, "review_status": review_status, "effect": effect}

    url = f"{_config.url_base}/variants/variant_based_disorder_associated_genes"

    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: _List[str] = _check_response(resp)
    return result


def get_variant_based_gene_associated_disorders(
    gene_id: str, review_status: _Optional[_List[str]] = None, effect: _Optional[_List[str]] = None
) -> _List[str]:
    """Gets a list of disorders associated with a gene using variant relations

    Parameters
    ----------
    gene_id : str
        The gene ID to get associated disorders for
    review_status : list[str], optional
        A list of review statuses to filter on. The default, None, returns only
        associations with "practical guideline" or "reviewed by expert panel"
        as the review status
    effect : list[str], optional
        A list of effect values to filter on. The default, None, returns only
        associations with "Pathogenic", "Likely pathogenic", or
        "Pathogenic/Likely pathogenic" as a listed effect

    Returns
    -------
    list[str]
        A list of disorders associated with the query gene
    """
    params = {"gene_id": gene_id, "review_status": review_status, "effect": effect}

    url = f"{_config.url_base}/variants/variant_based_gene_associated_disorders"

    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: _List[str] = _check_response(resp)
    return result
