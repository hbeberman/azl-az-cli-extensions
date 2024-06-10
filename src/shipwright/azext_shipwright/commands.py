# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def load_command_table(self, _):

    with self.command_group('shipwright') as g:
        g.custom_command('echo', 'echo_shipwright')

    with self.command_group('shipwright') as c:
        c.custom_command('create-vm', 'create_vm_shipwright')
