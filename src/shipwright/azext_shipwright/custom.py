# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.command_modules.vm.custom import create_vm
import azure.cli.command_modules.vm.custom
import functools
from knack.log import get_logger
from azext_aks_preview.custom import aks_create

logger = get_logger(__name__)


def decorate_aks_create(func):
    _WRAPPER_FUNC_NAME = "decorate_aks_create.wrapper"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"{_WRAPPER_FUNC_NAME}: begin")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: args: '{args}'")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: kwargs: '{kwargs}'")
        ret = func(*args, **kwargs)
        logger.debug(f"{_WRAPPER_FUNC_NAME}: ret: '{ret}'")
        logger.debug(f"{_WRAPPER_FUNC_NAME}: end")
        return ret

    return wrapper


aks_create = decorate_aks_create(aks_create)


def echo_shipwright(cmd, echo_back):
    print(f"echo: '{echo_back}'")


def create_vm_shipwright(cmd, vm_name):
    print(f"Creating VM '{vm_name}'...")
