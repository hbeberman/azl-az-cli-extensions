# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm.custom import create_vm
from azext_aks_preview.custom import aks_create

import sys
from azure.cli.core.extension import get_extension_path
sys.path.append(get_extension_path('aks-preview'))

def echo_shipwright(cmd, echo_back):
    print(f"echo: '{echo_back}'")

def create_vm_shipwright(cmd, vm_name):
    print(f"Creating VM '{vm_name}'...")

def get_resource_groups_client(cli_ctx, subscription_id=None):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.profiles import ResourceType

    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resource_groups

def get_rg(cli_ctx, resource_group_name, subscription_id=None):
    from knack.util import CLIError
    groups = get_resource_groups_client(cli_ctx, subscription_id=subscription_id)
    # Just do the get, we don't need the result, it will error out if the group doesn't exist.
    rg = groups.get(resource_group_name)
    if rg is None:
        raise CLIError(f"Resource group {resource_group_name} not found.")
    return rg

    # from azure.cli.core.commands.client_factory import get_mgmt_service_client
    # from azure.cli.core.profiles import ResourceType

    # resource_group = get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES).resource_groups.get(resource_group_name)
    # return resource_group.location


def shipwright_aks_create(cmd, resource_group, cluster_name):
    azsecpack_ua_rg = "azsecpackautoconfigrg"
    azsecpack_uai_basename="azsecpackautoconfigua-"

    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.commands.parameters import get_resources_in_subscription
    from azure.cli.core.profiles import ResourceType
    from azure.cli.core.profiles import CustomResourceType

    from azext_aks_preview._client_factory import cf_managed_clusters

    print(f"Creating AKS cluster '{cluster_name}' in resource group '{resource_group}'...")
    print("AKS cluster created.")

    # get cluster resource object
    # get cluster location, nodepool resource group, and nodepool name(s)
    # build azsecpack UAI name
    # assign azsecpack UAI to cluster's nodepool(s)

    rg = get_rg(cmd.cli_ctx, resource_group)
    location = "Unknown"
    if rg is not None:
        location = rg.location

    print(f"Resource group location: {location}")

    print(f"Resource group: {rg}")

    # rg_location = get_mgmt_service_client(cmd.cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
    #                         subscription_id=subscription_id).resource_groups.

    # resources = get_mgmt_service_client(cmd.cli_ctx, ResourceType.MGMT_COMPUTE,
    #                                subscription_id=None).resources

    # print(f"Resources: {resources}")
    # from azure.cli.command_modules.acs.custom import aks_agentpool_list
    # from azure.cli.command_modules.acs._format import aks_agentpool_list_table_format
    client = cf_managed_clusters(cmd.cli_ctx)#cf_agent_pools(cmd.cli_ctx)
    # print(f"Client: {client}")

    # results = aks_agentpool_list(cmd, client, resource_group, cluster_name)
    # nodepool_list = aks_agentpool_list_table_format(results)
    # #nodepool_list = list(client.list(resource_group, cluster_name))
    # print(f"List: {nodepool_list}")
    # # print(f"Instance: {instance}")

    from  azure.mgmt.containerservice import ContainerServiceClient

    from azure.identity import DefaultAzureCredential
    from azure.cli.core import get_default_cli

    from azure.cli.core.commands.client_factory import get_subscription_id, get_az_user_agent
    subscription = get_subscription_id(cmd.cli_ctx)
    print(f"Subscription: {subscription}")

    from azure.cli.command_modules.acs.custom import aks_show
    result = aks_show(cmd, client, resource_group, cluster_name)

    print(f"Result: {result}\n\n{type(result)}\n\n")

    print(f"AgentPool: {result.agent_pool_profiles}")



    # import sys

    # print(f"sys.path: {sys.path}")
    # sys.path.append(get_extension_path('aks-preview'))

    # print(f"sys.path: {sys.path}")


    # print(f"Get Extension path {get_extension_path('aks-preview')}")
    # client = ContainerServiceClient(identity=DefaultAzureCredential().get_token("openid"), subscription_id=subscription)
    # print(f"Client: {client}")
