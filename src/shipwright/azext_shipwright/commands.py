# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm._client_factory import cf_vm, cf_vmss
from azure.cli.command_modules.vm._format import transform_vm_create_output
from azure.cli.core.commands.arm import (
    deployment_validate_table_format,
    handle_template_based_exception,
)

from azure.cli.core.commands import DeploymentOutputLongRunningOperation, CliCommandType
from azext_shipwright.validators import azl_process_vm_create_namespace

def load_command_table(self, _):

    compute_vm_sdk = CliCommandType(
        operations_tmpl="azure.mgmt.compute.operations#VirtualMachinesOperations.{}",
        client_factory=cf_vm,
    )

    compute_vmss_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.compute.operations#VirtualMachineScaleSetsOperations.{}',
        client_factory=cf_vmss,
        operation_group='virtual_machine_scale_sets'
    )

    with self.command_group('shipwright') as g:
        g.custom_command('echo', 'echo_shipwright')

    # Maybe A quick cmd for set a S360 VM 
    with self.command_group('shipwright') as c:
        c.custom_command('create-vm', 'create_vm_shipwright')

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

    with self.command_group('shipwright vmss', compute_vmss_sdk, operation_group='virtual_machine_scale_sets') as g:
        g.custom_command(
            'create', 
            'create_vmss', 
            transform=DeploymentOutputLongRunningOperation(self.cli_ctx, 'Starting vmss create'), 
            supports_no_wait=True, 
            table_transformer=deployment_validate_table_format, 
            validator=azl_process_vm_create_namespace, 
            exception_handler=handle_template_based_exception)