# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def connect_serialtunnel(cmd, resource_group_name, vm_vmss_name, vmss_instanceid=None):
    print("Connecting to serial tunnel...")