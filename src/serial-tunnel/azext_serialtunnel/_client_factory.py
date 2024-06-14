# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.profiles import ResourceType

def cf_serialconsole(cli_ctx, **kwargs):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azext_serialconsole.vendored_sdks.serialconsole import MicrosoftSerialConsoleClient
    return get_mgmt_service_client(cli_ctx,
                                   MicrosoftSerialConsoleClient, **kwargs)

def cf_serial_port(cli_ctx, **kwargs):
    return cf_serialconsole(cli_ctx, **kwargs).serial_ports