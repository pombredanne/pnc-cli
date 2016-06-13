import argparse
import logging

from argh import arg

from six import iteritems

from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli import buildconfigurations
from pnc_cli import productversions
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi

sets_api = BuildconfigurationsetsApi(utils.get_api_client())
configs_api = BuildconfigurationsApi(utils.get_api_client())


def set_set_id(id, name):
    if id:
        return id
    if name:
        return get_build_config_set_id_by_name(name)
    else:
        raise argparse.ArgumentTypeError("Either a BuildConfigurationSet ID or name is required.")


def unique_set_name(name_input):
    if get_build_config_set_id_by_name(name_input):
        raise argparse.ArgumentTypeError("BuildConfigurationSet name '{}' is already in use".format(name_input))
    return name_input


def existing_set_name(name_input):
    if not get_build_config_set_id_by_name(name_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with the name {} exists".format(name_input))
    return name_input


def existing_set_id(id_input):
    utils.valid_id(id_input)
    if not _set_exists(id_input):
        raise argparse.ArgumentTypeError("no BuildConfigurationSet with ID {} exists".format(id_input))
    return id_input


def _create_build_config_set_object(**kwargs):
    created_build_config_set = swagger_client.BuildConfigurationSetRest()
    for key, value in iteritems(kwargs):
        setattr(created_build_config_set, key, value)
    return created_build_config_set


def get_build_config_set_id_by_name(search_name):
    sets = sets_api.get_all(q='name==' + search_name).content
    if sets:
        config_set = sets[0]
        return config_set.id
    return None


def _set_exists(set_id):
    existing = utils.checked_api_call(sets_api, 'get_specific', id=set_id)
    if not existing:
        return False
    return True


@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configuration_sets(page_size=200, sort="", q=""):
    """
    List all build configurtion sets
    """
    response = utils.checked_api_call(sets_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("name", help="Name for the new BuildConfigurationSet.", type=unique_set_name)
@arg("-pvi", "--product-version-id",
     help="ID of the product version to associate this BuildConfigurationSet.",
     type=productversions.existing_product_version)
@arg("-bcs", "--build-configuration-ids", type=buildconfigurations.existing_bc_id, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
def create_build_configuration_set(**kwargs):
    """
    Create a new BuildConfigurationSet.
    """
    config_set = _create_build_config_set_object(**kwargs)
    response = utils.checked_api_call(sets_api, 'create_new', body=config_set)
    if response:
        return response.content


@arg("-id", "--id", help="ID of the BuildConfigurationSet to retrieve", type=existing_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to retrieve", type=existing_set_name)
def get_build_configuration_set(id=None, name=None):
    """
    Get a specific BuildConfigurationSet by name or ID
    """
    found_id = set_set_id(id, name)
    response = utils.checked_api_call(sets_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg("id", help="ID of the BuildConfigurationSet to update.", type=existing_set_id)
@arg("-n", "--name", help="Updated name for the BuildConfigurationSet.", type=unique_set_name)
@arg("-pvi", "--product-version-id",
     help="Updated product version ID for the BuildConfigurationSet.", type=productversions.existing_product_version)
@arg("-bcs", "--build-configuration-ids", type=buildconfigurations.existing_bc_id, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
def update_build_configuration_set(id, **kwargs):
    """
    Update a BuildConfigurationSet
    """
    set_to_update = utils.checked_api_call(sets_api, 'get_specific', id=id).content

    for key, value in kwargs.items():
        if value is not None:
            setattr(set_to_update, key, value)

    response = utils.checked_api_call(sets_api, 'update', id=id, body=set_to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet to delete.", type=existing_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to delete.", type=existing_set_name)
# TODO: in order to delete a config set successfully, any buildconfigsetrecords must be deleted first
# TODO: it may be impossible / undesireable to remove
# buildconfigsetrecords. so perhaps just check and abort
def delete_build_configuration_set(id=None, name=None):
    set_id = set_set_id(id, name)
    response = utils.checked_api_call(sets_api, 'delete_specific', id=set_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.", type=existing_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.", type=existing_set_name)
def build_set(id=None, name=None):
    """
    Start a build of the given BuildConfigurationSet
    """
    found_id = set_set_id(id, name)
    response = utils.checked_api_call(sets_api, 'build', id=found_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.", type=existing_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.", type=existing_set_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_set(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all build configurations in a given BuildConfigurationSet.
    """
    found_id = set_set_id(id, name)
    response = utils.checked_api_call(sets_api, 'get_configurations', id=found_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-sid", "--set-id", help="ID of the BuildConfigurationSet to add to", type=existing_set_id)
@arg("-sn", "--set-name", help="Name of the BuildConfigurationSet to add to", type=existing_set_name)
@arg("-cid", "--config-id",
     help="ID of the build configuration to add to the given set", type=buildconfigurations.existing_bc_id)
@arg("-cn", "--config-name",
     help="Name of the build configuration to add to the given set", type=buildconfigurations.valid_existing_bc_name)
def add_build_configuration_to_set(
        set_id=None, set_name=None, config_id=None, config_name=None):
    """
    Add a build configuration to an existing BuildConfigurationSet
    """
    config_set_id = set_set_id(set_id, set_name)
    bc = buildconfigurations.get_build_configuration(id=config_id, name=config_name)
    response = utils.checked_api_call(
        sets_api,
        'add_configuration',
        id=config_set_id,
        body=bc)
    if response:
        return response.content


@arg("-sid", "--set-id", help="ID of the BuildConfigurationSet to remove from", type=existing_set_id)
@arg("-sn", "--set-name", help="Name of the BuildConfigurationSet to remove from", type=existing_set_name)
@arg("-cid", "--config-id", help="ID of the BuildConfiguration to remove from the set",
     type=buildconfigurations.existing_bc_id)
@arg("-cn", "--config-name", help="Name of the BuildConfiguration to remove from the set",
     type=buildconfigurations.valid_existing_bc_name)
def remove_build_configuration_from_set(set_id=None, set_name=None, config_id=None, config_name=None):
    config_set_id = set_set_id(set_id, set_name)
    bc_id = buildconfigurations.set_bc_id(config_id, config_name)
    response = utils.checked_api_call(
        sets_api,
        'remove_configuration',
        id=config_set_id,
        config_id=bc_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet", type=existing_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet", type=existing_set_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records_for_set(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all build records for a BuildConfigurationSet
    """
    found_id = set_set_id(id, name)
    response = utils.checked_api_call(sets_api, 'get_build_records', id=found_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
