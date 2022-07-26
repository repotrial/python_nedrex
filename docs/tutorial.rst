========
Tutorial
========

After installation, the nedrex library can be importated as follows::

    import nedrex


####################
Connecting to NeDRex
####################

Once imported, the NeDRex instance needs to be configured to point at a NeDRex endpoint.
For a list of endpoints, see :ref:`available-endpoints-label`.

The Python library can be connected to an instance of NeDRex as follows::

    # replace ... with the URL (as a string)
    nedrex.config.set_url_base(...)


Additionally, some versions of NeDRex require an API key.
This can be checked with the :code:`nedrex.core.api_keys_active` function.
If a NeDRex instance requires an API key, one can be obtained with the :code:`nedrex.core.get_api_key` function.
Note that this function requires you accept the EULA of that NeDRex instance.
Do not use this function if you do not accept the EULA of the NeDRex instance you are connecting to.
The following example checks whether API keys are active and, if so, obtains one::

    from nedrex.core import api_keys_active, get_api_key

    if api_keys_active():
        api_key = get_api_key(accept_eula=True)
        nedrex.config.set_api_key(api_key)

########################
Exploring data in NeDRex
########################
The NeDRex database can be thought of as a network composed of nodes (the "things" in the network) and edges (the relationships between the "things").
Nodes and edges are subdivided into *collections* based on their type.
For example, there is a node in the graph representing the drug paracetamol/acetaminophen, which is a member of the :code:`drug` collection.
A full list of the node and edge collections available in NeDRex can be obtained using the :code:`get_node_types` and :code:`get_edge_types` functions, respectively::

    from nedrex.core import get_node_types, get_edge_types

    print(get_node_types())
    # ['disorder', 'drug', 'gene', ..., 'tissue']
    print(get_edge_types())
    # ['disorder_has_phenotype', ..., 'variant_associated_with_disorder']

These types are used in other functions when accessing the data.

Getting nodes and edges of a particular type
============================================
Nodes and edges each have two seperate functions that can be used to access the data.

For nodes, these are:

* :code:`get_nodes`
* :code:`iter_nodes`

For edges, these are:

* :code:`get_edges`
* :code:`iter_edges`

These behave similarly, but have slightly different options. 
The :code:`get_` prefixed routes are used for obtaining a list of nodes or edges from the NeDRex database.
However, because the NeDRex database contains a large a number of certain types, these routes are *paginated* to only return a subset at each function call.
The subset returned is determined by the :code:`limit` and :code:`offset` keyword argument.
By default, :code:`offset=0`, and :code:`limit` defaults to the NeDRex instance's maximum limit.
The default limit can be obtained using the :code:`nedrex.core.get_pagination_limit` function.

An example of using the :code:`get_nodes` function to get two subsets of drugs is as follows::

    from nedrex.core import get_nodes, get_pagination_limit

    limit = get_pagination_limit()
    offset = 0

    batch1 = get_nodes("drug", limit=limit, offset=offset)
    offset += limit
    batch2 = get_nodes("drug", limit=limit, offset=offset)

If your aim is to obtain all of the nodes or edges of a particular type, then consider using the :code:`iter_` functions instead.
The :code:`iter_` prefixed functions automatically handle the :code:`limit` and :code:`offset` arguments, returning a generator over all items of the requested type.
For example, the following example uses the :code:`iter_nodes` function to get all of the drugs in NeDRex::

    from nedrex.core import iter_nodes

    for drug in iter_nodes("drug"):
        # do something...
        print(drug['displayName'])

The node routes can optionally take two additional arguments to filter the output.
The first, :code:`node_ids`, allows you to pass a list of NeDRex node IDs to filter the returned nodes.
The second, :code:`attributes`, allows you to specify which attributes are retrieved for the returned nodes.
An example of using these in the previous example to get the :code:`displayName` attribute for paracetamol is as follows::

    from nedrex.core import iter_nodes

    for drug in iter_nodes("drug", attributes=["displayName"], node_ids=["drugbank.DB00316"]):
        print(drug)
        # {'primaryDomainId': 'drugbank.DB00316', 'displayName': 'Acetaminophen'}


###################
How NeDRex IDs work
###################
Every node in NeDRex has a unique ID attribute, :code:`primaryDomainId`.
Each of these IDs has the same format, :code:`<database>.<database_id>`.
In the previous example, the primaryDomainId for the drug paracetamol/acetaminophen is :code:`drugbank.DB00316`.
In the current version of NeDRex, **with the exception of the signature type, only one data source per type is used for the primaryDomainId**.
This means, for instance, that :code:`drugbank.` is used to prefix all drugs.
The table below shows the data source and prefix used for each type in NeDRex (as of 2022-07-26).

=============== ============================== =================
type            data source                    prefix
=============== ============================== =================
disorder        MONDO                          :code:`mondo.`
drug            DrugBank                       :code:`drugbank.`
gene            NCBI                           :code:`entrez.`
genomic_variant ClinVar                        :code:`clinvar.`
go              GO                             :code:`go.`
pathway         Reactome                       :code:`reactome.`
phenotype       Human Phenotype Ontology (HPO) :code:`hpo.`
protein         UniProt                        :code:`uniprot.`
side_effect     bioontology.org                :code:`meddra.`
signature       InterPro (via UniProt)         Various
tissue          Uberon                         :code:`uberon.`
=============== ============================== =================

.. _available-endpoints-label:

###################
Available endpoints
###################

The available, officially supported endpoints are listed in the table below.

===============  ========================== =================
Description      URL                        License
===============  ========================== =================
Open NeDRex      TBD                        TBD
Licensed NeDRex  http://82.148.225.92:8123/ `NeDRex License`_
===============  ========================== =================


.. _NeDRex License: https://raw.githubusercontent.com/repotrial/nedrex_platform_licence/main/licence.txt