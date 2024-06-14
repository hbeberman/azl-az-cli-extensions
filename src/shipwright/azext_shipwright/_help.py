# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import

# consume help text from az aks create and az vm create so we don't have to duplicate it
from azext_aks_preview._help import helps as aks_preview_helps
from azure.cli.command_modules.vm._help import helps as vm_helps

helps['shipwright'] = """
    type: group
    short-summary: Common dev tasks for the AZL team.
"""

helps['shipwright echo'] = """
    type: command
    short-summary: Proof of concept that we can take parameters and do things.
"""

helps['shipwright create-vm'] = """
    type: command
    short-summary: Create an S360-compliant vm.
"""

# Update help for the shipwright commands to use the same help as the underlying command
helps['shipwright vm create'] = vm_helps['vm create'].replace('az vm', 'az shipwright vm')
helps['shipwright vmss create'] = vm_helps['vmss create'].replace('az vmss', 'az shipwright vmss')

