# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType

echo_back_arg_type = CLIArgumentType(
    options_list=('--echo-back', '-e'), help='Echo the input string back.')

def load_arguments(self, _):

    with self.argument_context('shipwright') as c:
        c.argument('echo_back', arg_type=echo_back_arg_type)
