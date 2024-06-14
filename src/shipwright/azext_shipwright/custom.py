# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import subprocess
import shlex

from azure.cli.command_modules.vm.custom import create_vm
from azure.cli.command_modules.vm.custom import create_vmss
from knack.log import get_logger

logger = get_logger(__name__)

def echo_shipwright(cmd, echo_back):
    print(f"echo: '{echo_back}'")

def create_vm_shipwright(cmd, vm_name, resource_group_name, image, admin_username):

    logger.debug('Create-vm command parameters:  vm_name: %s, resource_group_name: %s, image: %s, admin_username: %s', vm_name, resource_group_name, image, admin_username)
    print(f"Creating VM '{vm_name}'... {resource_group_name}")

    create_vm_command = 'az vm create -n {n} -g {g}  --tag AzSecPackAutoConfigReady=true --image {image_name} --admin-username {username}' \
                .format(n=vm_name, g=resource_group_name, image_name=image, username=admin_username)

    tokenized_command = shlex.split(create_vm_command)
    
    process = subprocess.Popen(tokenized_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    stdout, stderr = process.communicate()

    print(f"stdout: '{stdout}'... stderr: '{stderr}' ")


