from azure.cli.command_modules.vm._validators import process_vm_create_namespace


def add_azsecpack_tags(namespace):
    tags = namespace.tags
    print(f"Tags: {tags}")
    if not tags:
        tags = {}
    if isinstance(tags, str):
        pairs = tags.split()
        tags = dict(pair.split('=') for pair in pairs)

    tags['AzSecPackAutoConfigReady'] = 'true'

    # tags = ' '.join([f"{k}={v}" for k, v in tags.items()])
    namespace.tags = tags
    print(f"Tags: {namespace.tags}")

def azl_process_vm_create_namespace(cmd, namespace):
    print("Processing VM create namespace...")
    print(f"Namespace: {namespace}\n")
    add_azsecpack_tags(namespace)
    process_vm_create_namespace(cmd, namespace)
    print(f"Namespace: {namespace}\n")
