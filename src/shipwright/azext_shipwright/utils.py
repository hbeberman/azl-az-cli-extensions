from knack.util import CLIError

def _get_resource_groups_client(cli_ctx, subscription_id=None):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.profiles import ResourceType

    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resource_groups

def get_resource_group(cli_ctx, resource_group_name, subscription_id=None):
    from knack.util import CLIError
    groups = _get_resource_groups_client(cli_ctx, subscription_id=subscription_id)
    # Just do the get, we don't need the result, it will error out if the group doesn't exist.
    rg = groups.get(resource_group_name)
    if rg is None:
        raise CLIError(f"Resource group {resource_group_name} not found.")
    return rg


def get_user_assigned_identity(cli_ctx, resource_group_name, identity_name):

    from azure.cli.command_modules.identity._client_factory import _msi_client_factory
    client = _msi_client_factory(cli_ctx)
    # print(f"Identity Client: {client}")

    try:
        return client.user_assigned_identities.get(resource_group_name, identity_name)
    except Exception as ex:
        raise CLIError(ex)

    # from knack.util import CLIError
    # from azure.cli.core.commands.client_factory import get_mgmt_service_client
    # from azure.cli.core.profiles import ResourceType

    # client = get_mgmt_service_client(cli_ctx, ResourceType.MGMT_MSI_USER_ASSIGNED,
    #                                  subscription_id=subscription_id)
    # try:
    #     return client.user_assigned_identities.get(resource_group_name, identity_name)
    # except Exception as ex:
    #     raise CLIError(ex)

def get_vmss_list(cli_ctx, resource_group_name):
    from azext_aks_preview._client_factory import get_compute_client

    compute_client = get_compute_client(cli_ctx)
    # print(f"Compute Client: {compute_client}")
    try:
        return compute_client.virtual_machine_scale_sets.list(resource_group_name)
    except Exception as ex:
        raise CLIError(ex)

def assign_identity_to_vmss(cmd, resource_group_name, vmss_name, identity_id, subscription_id=None):
    # from azure.cli.command_modules.vm.custom import assign_vmss_identity

    # result = assign_vmss_identity(cmd, resource_group_name, vmss_name, assign_identity=identity_id.id)

    # call az cli on the command line
    import subprocess

    try:
        # Construct the Azure CLI command
        command = [
            'az', 'vmss', 'identity', 'assign',
            '--resource-group', resource_group_name,
            '--name', vmss_name,
            '--identities', identity_id.id
        ]

        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the command output
        print('Output:', result.stdout)
        print('Error:', result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Error output: {e.stderr}")


    # from azure.cli.core.profiles import ResourceType
    # from azure.cli.core.commands.client_factory import get_mgmt_service_client
    # compute_client = get_mgmt_service_client(cli_ctx, ResourceType.MGMT_COMPUTE, subscription_id=subscription_id)
    # print(f"Compute Client: {compute_client}")
    # try:
    #     vmss = compute_client.virtual_machine_scale_sets.get(resource_group_name, vmss_name)
    #     print(f"VMSS: {vmss}")

    #     if not vmss.identity:
    #         vmss.identity = {
    #             "type": "UserAssigned",
    #             "userAssignedIdentities": {identity_id}
    #         }
    #     elif not vmss.identity.user_assigned_identities:

    #         vmss.identity.user_assigned_identities = {identity_id}

    #               #     if identity_name not in vmss.identity.user_assigned_identities.keys():
    # #         vmss.identity.user_assigned_identities[identity_name] = {}
    # #         compute_client.virtual_machine_scale_sets.create_or_update(resource_group_name, vmss_name, vmss)
    # except Exception as ex:
    #     raise CLIError(ex)
