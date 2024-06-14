# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm._client_factory import cf_vm
from azure.cli.command_modules.vm._format import transform_vm_create_output
from azure.cli.core.commands.arm import (
    deployment_validate_table_format,
    handle_template_based_exception,
)
from azext_aks_preview._client_factory import cf_managed_clusters
from azure.cli.core.commands import CliCommandType

from azext_shipwright.validators import azl_process_vm_create_namespace
from azext_aks_preview.commands import transform_mc_objects_with_custom_cas


def load_command_table(self, _):

    compute_vm_sdk = CliCommandType(
        operations_tmpl="azure.mgmt.compute.operations#VirtualMachinesOperations.{}",
        client_factory=cf_vm,
    )

    managed_clusters_sdk = CliCommandType(
        operations_tmpl="azext_aks_preview.vendored_sdks.azure_mgmt_preview_aks."
        "operations._managed_clusters_operations#ManagedClustersOperations.{}",
        operation_group="managed_clusters",
        client_factory=cf_managed_clusters,
    )

    with self.command_group("shipwright") as g:
        g.custom_command("echo", "echo_shipwright")

    with self.command_group("shipwright vm", compute_vm_sdk) as g:
        g.custom_command(
            "create",
            "create_vm",
            transform=transform_vm_create_output,
            supports_no_wait=True,
            table_transformer=deployment_validate_table_format,
            validator=azl_process_vm_create_namespace,
            exception_handler=handle_template_based_exception,
        )

    with self.command_group(
        "shipwright aks",
        managed_clusters_sdk,
        client_factory=cf_managed_clusters,
        transform=transform_mc_objects_with_custom_cas,
    ) as g:
        g.custom_command(
            "create",
            "aks_create",
            supports_no_wait=False,
        )
