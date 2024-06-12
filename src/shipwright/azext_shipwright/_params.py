# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType

echo_back_arg_type = CLIArgumentType(
    options_list=('--echo-back', '-e'), help='Echo the input string back.')

vm_name_arg_type = CLIArgumentType(
    options_list=('--vm_name', '-n'), help='Name of the VM to create.')

resource_group_arg_type = CLIArgumentType(
    options_list=('--resource_group_name', '-rg'), help='Name of the resource group that will contain the VM.')

image = CLIArgumentType(
    options_list=('--image'), help='Option to create vm from a specific image.')

admin_username = CLIArgumentType(
    options_list=('--admin_username'), help='Name of admin user for created image.')


def load_arguments(self, _):

    with self.argument_context('shipwright') as c:
        c.argument('echo_back', arg_type=echo_back_arg_type)
        c.argument('vm_name', arg_type=vm_name_arg_type)
        c.argument('resource_group_name', arg_type=resource_group_arg_type)
        c.argument('image', arg_type=image)
        c.argument('admin_username', arg_type=admin_username)
