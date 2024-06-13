# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm._client_factory import cf_vm
from azure.cli.command_modules.vm._format import transform_vm_create_output
from azure.cli.core.commands.arm import deployment_validate_table_format, handle_template_based_exception

from azure.cli.core.commands import CliCommandType

from azext_shipwright.validators import azl_process_vm_create_namespace

import sys
from azure.cli.core.extension import get_extension_path
sys.path.append(get_extension_path('aks-preview'))


def load_command_table(self, _):

    # import sys
    # from azure.cli.core.extension import get_extension_path

    # print(f"sys.path: {sys.path}")
    # sys.path.append(get_extension_path('aks-preview'))

    # print(f"sys.path: {sys.path}")


    from azext_aks_preview._client_factory import cf_managed_clusters
    from azext_aks_preview.commands import transform_mc_objects_with_custom_cas

    print("lyrydber: load_command_table")

    managed_clusters_sdk = CliCommandType(
        operations_tmpl="azext_aks_preview.vendored_sdks.azure_mgmt_preview_aks."
        "operations._managed_clusters_operations#ManagedClustersOperations.{}",
        operation_group="managed_clusters",
        client_factory=cf_managed_clusters,
    )
    print("lyrydber: managed_clusters_sdk")

    compute_vm_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.compute.operations#VirtualMachinesOperations.{}',
        client_factory=cf_vm
    )
    print("lyrydber: compute_vm_sdk")

    with self.command_group('shipwright') as g:
        g.custom_command('echo', 'echo_shipwright')
    print("lyrydber: shipwright echo")

    with self.command_group('shipwright aks',
        managed_clusters_sdk,
        client_factory=cf_managed_clusters,
        transform=transform_mc_objects_with_custom_cas,
    ) as g:
        g.custom_command('create', 'aks_create', supports_no_wait=False)
        g.custom_command('mycreate', 'shipwright_aks_create', supports_no_wait=False)
    print("lyrydber: shipwright aks")

    with self.command_group('shipwright vm', compute_vm_sdk) as g:
        g.custom_command('create', 'create_vm', transform=transform_vm_create_output, supports_no_wait=True, table_transformer=deployment_validate_table_format, validator=azl_process_vm_create_namespace, exception_handler=handle_template_based_exception)
    print("lyrydber: shipwright vm")
