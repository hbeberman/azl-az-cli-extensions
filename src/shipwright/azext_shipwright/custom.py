# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from time import sleep
from azure.cli.command_modules.vm.custom import create_vm
import azure.cli.command_modules.vm.custom
import functools
from knack.log import get_logger
from azext_aks_preview.custom import aks_create

from azext_shipwright.utils import (get_resource_group, get_user_assigned_identity, get_vmss_list, assign_identity_to_vmss)

logger = get_logger(__name__)

AZSECPACK_UAI_RG = "azsecpackautoconfigrg"
AZSECPACK_UAI_BASENAME = "azsecpackautoconfigua-"


def add_azsecpack_uai_to_aks_vmss(cmd, cluster_name, resource_group_name):

    print(f"Getting AKS cluster {cluster_name} info...")
    cluster_rg = get_resource_group(cmd.cli_ctx, resource_group_name)
    location = cluster_rg.location


    from azext_aks_preview._client_factory import cf_managed_clusters, cf_agent_pools
    from azext_aks_preview.custom import aks_show, aks_agentpool_list

    managed_cluster_client = cf_managed_clusters(cmd.cli_ctx)
    #print(f"Managed Cluster Client: {managed_cluster_client}")

    managed_cluster_info = aks_show(cmd, managed_cluster_client, resource_group_name, cluster_name)
    # print(f"Result: {managed_cluster_info}")

    nodepool_rg_name = managed_cluster_info.node_resource_group
    nodepool_rg_details = get_resource_group(cmd.cli_ctx, nodepool_rg_name)
    location = nodepool_rg_details.location
    azsecpack_uai = f"{AZSECPACK_UAI_BASENAME}{location}"
    print(f"Identity name: {azsecpack_uai}")

    # get ID of the User Assigned Identity with the name contained in azsecpack_uai
    azsecpack_uai_object = get_user_assigned_identity(cmd.cli_ctx, AZSECPACK_UAI_RG, azsecpack_uai)
    azsecpack_uai_id = azsecpack_uai_object.id
    print(f"\n{azsecpack_uai_id}\n")
    print(f"UAI object: {azsecpack_uai_object}")

    print("Getting VMSSes for the cluster...")
    vmsses = get_vmss_list(cmd.cli_ctx, nodepool_rg_name)

    if not vmsses:
        raise ValidationError(f"No VMSS found in the managed resource group {nodepool_rg_name}!")

    vmss_list = list(vmsses)

    print(f"Found {len(vmss_list)} VMSSes in the managed resource group {nodepool_rg_name}.")

    for vmss in vmss_list:
        print("\n\n")
        print(f"VMSS: {vmss.name}")
        #print(f"VMSS ID: {vmss.id}")
        #print(f"VMSS Tags: {vmss.tags}")

        # print(f"VMSS Identity: {vmss.identity}\n\n")
        print(f"VMSS User Assigned Identities: {vmss.identity.user_assigned_identities}\n\n")

        if azsecpack_uai_id.lower() not in [id.lower() for id in vmss.identity.user_assigned_identities.keys()]:
            print(f"Adding identity '{azsecpack_uai}' to VMSS '{vmss.name}'...")
            from azure.cli.core.commands.client_factory import get_subscription_id
            subscription_id = get_subscription_id(cmd.cli_ctx)
            # print(f"Subscription ID: {subscription_id}")
            assign_identity_to_vmss(cmd, nodepool_rg_name, vmss.name, azsecpack_uai_object, subscription_id=subscription_id)
            # assign_identity_to_vmss(cmd.cli_ctx, nodepool_rg_name, vmss.name, azsecpack_uai_object, subscription_id=subscription_id)

            print(f"Identity '{azsecpack_uai}' added to VMSS '{vmss.name}'.")
        else:
            print(f"Identity '{azsecpack_uai}' already exists in VMSS '{vmss.name}'.")

    # from azure.cli.command_modules.identity.custom import identity_assign


def decorate_aks_create(func):
    _WRAPPER_FUNC_NAME = "decorate_aks_create.wrapper"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"{_WRAPPER_FUNC_NAME}: begin")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: args: '{args}'")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: kwargs: '{kwargs}'")

        # add_azsecpack_uai_to_aks_vmss(kwargs["cmd"], kwargs["name"], kwargs["resource_group_name"])

        # print(f"Attempting to add identity to AKS cluster...")

        # print(f"AKS cluster name: {kwargs['name']}")
        # cluster_rg = get_resource_group(kwargs["cmd"].cli_ctx, kwargs["resource_group_name"])
        # location = cluster_rg.location


        # from azext_aks_preview._client_factory import cf_managed_clusters, cf_agent_pools
        # from azext_aks_preview.custom import aks_show, aks_agentpool_list

        # managed_cluster_client = cf_managed_clusters(kwargs["cmd"].cli_ctx)
        # #print(f"Managed Cluster Client: {managed_cluster_client}")

        # managed_cluster_info = aks_show(kwargs["cmd"], managed_cluster_client, kwargs["resource_group_name"], kwargs["name"])
        # # print(f"Result: {managed_cluster_info}")

        # nodepool_rg_name = managed_cluster_info.node_resource_group
        # nodepool_rg_details = get_resource_group(kwargs["cmd"].cli_ctx, nodepool_rg_name)
        # location = nodepool_rg_details.location
        # azsecpack_uai = f"{AZSECPACK_UAI_BASENAME}{location}"
        # print(f"Identity name: {azsecpack_uai}")

        # # get ID of the User Assigned Identity with the name contained in azsecpack_uai
        # azsecpack_uai_object = get_user_assigned_identity(kwargs["cmd"].cli_ctx, AZSECPACK_UAI_RG, azsecpack_uai)
        # azsecpack_uai_id = azsecpack_uai_object.id
        # print(f"\n{azsecpack_uai_id}\n")
        # print(f"UAI object: {azsecpack_uai_object}")

        # vmsses = get_vmss_list(kwargs["cmd"].cli_ctx, nodepool_rg_name)

        # if not vmsses:
        #     raise ValidationError(f"No VMSS found in the managed resource group {nodepool_rg_name}!")

        # vmss_list = list(vmsses)

        # print(f"Found {len(vmss_list)} VMSSes in the managed resource group {nodepool_rg_name}.")

        # for vmss in vmss_list:
        #     print("\n\n")
        #     print(f"VMSS: {vmss.name}")
        #     #print(f"VMSS ID: {vmss.id}")
        #     #print(f"VMSS Tags: {vmss.tags}")

        #     print(f"VMSS Identity: {vmss.identity}\n\n")
        #     print(f"VMSS User Assigned Identities: {vmss.identity.user_assigned_identities}\n\n")

        #     if azsecpack_uai_id.lower() not in [id.lower() for id in vmss.identity.user_assigned_identities.keys()]:
        #         print(f"Adding identity '{azsecpack_uai}' to VMSS '{vmss.name}'...")
        #         from azure.cli.core.commands.client_factory import get_subscription_id
        #         subscription_id = get_subscription_id(kwargs["cmd"].cli_ctx)
        #         print(f"Subscription ID: {subscription_id}")
        #         assign_identity_to_vmss(kwargs["cmd"], nodepool_rg_name, vmss.name, azsecpack_uai_object, subscription_id=subscription_id)
        #         # assign_identity_to_vmss(kwargs["cmd"].cli_ctx, nodepool_rg_name, vmss.name, azsecpack_uai_object, subscription_id=subscription_id)

        #         print(f"Identity '{azsecpack_uai}' added to VMSS '{vmss.name}'.")
        #     else:
        #         print(f"Identity '{azsecpack_uai}' already exists in VMSS '{vmss.name}'.")

        # # from azure.cli.command_modules.identity.custom import identity_assign


        # print("Running the original aks_create function...")

        ret = func(*args, **kwargs)

        while not ret.done():
            print("Waiting for AKS cluster creation to complete...")
            sleep(5)

        add_azsecpack_uai_to_aks_vmss(kwargs["cmd"], kwargs["name"], kwargs["resource_group_name"])

        logger.debug(f"{_WRAPPER_FUNC_NAME}: ret: '{ret}'")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: end")
        return ret

    return wrapper


aks_create = decorate_aks_create(aks_create)


def echo_shipwright(cmd, echo_back):
    print(f"echo: '{echo_back}'")


def create_vm_shipwright(cmd, vm_name):
    print(f"Creating VM '{vm_name}'...")
