# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm.custom import create_vm

def echo_shipwright(cmd, echo_back):
    print(f"echo: '{echo_back}'")

def create_vm_shipwright(cmd, vm_name):
    print(f"Creating VM '{vm_name}'...")
