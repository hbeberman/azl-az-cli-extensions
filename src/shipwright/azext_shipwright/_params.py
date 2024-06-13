# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


echo_back_arg_type = CLIArgumentType(
    options_list=("--echo-back", "-e"), help="Echo the input string back."
)

vm_name_arg_type = CLIArgumentType(
    options_list=("--vm-name", "-n"), help="Name of the VM to create."
)

build_id_arg_type = CLIArgumentType(
    options_list=("--build-id", "-b"), help="ID of the build to get status for."
)

build_include_url_arg_type = CLIArgumentType(
    options_list=("--include-url", "-i"),
    help="Include the URL of the build in the output.",
    action="store_true",
)


def load_arguments(self, cmd):

    self.aks_preview_loader.skip_applicability = True
    self.aks_preview_loader.load_arguments(cmd)
    # print(vars(self.aks_preview_loader))

    # print()
    # print(self.aks_preview_loader.argument_registry.arguments["aks create"])
    # print()

    # print(self.aks_preview_loader.argument_registry.arguments.get("aks"))
    # print(self.aks_preview_loader.extra_argument_registry.keys())

    with self.argument_context("shipwright") as c:
        c.argument("echo_back", arg_type=echo_back_arg_type)
        c.argument("vm_name", arg_type=vm_name_arg_type)
        c.argument("build_id", arg_type=build_id_arg_type)

    self.argument_registry.arguments["shipwright aks create"] = (
        self.aks_preview_loader.argument_registry.arguments["aks create"]
    )
    # print(self.argument_registry.arguments.keys())
