from azure.cli.command_modules.vm._validators import process_vm_create_namespace


def add_azsecpack_tags(namespace):
    print("Adding AzSecPackAutoConfigReady tag to VM tags...")
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

def add_azsecpack_nodepool_tags(namespace):
    print("Adding AzSecPackAutoConfigReady tag to nodepool tags...")
    tags = namespace.nodepool_tags
    print(f"Nodepool Tags: {tags}")
    if not tags:
        tags = []
    if isinstance(tags, str):
        pairs = tags.split()
        tags_d = dict(pair.split('=') for pair in pairs)
    if isinstance(tags, list):
        tags_d = dict(pair.split('=') for pair in tags)

    tags_d['AzSecPackAutoConfigReady'] = 'true'

    tags = [f"{k}={v}" for k, v in tags_d.items()]

    namespace.nodepool_tags = tags
    print(f"Nodepool Tags: {namespace.nodepool_tags}")

def azl_process_vm_create_namespace(cmd, namespace):
    # print("Processing VM create namespace...")
    # print(f"Namespace: {namespace}\n")
    add_azsecpack_tags(namespace)
    process_vm_create_namespace(cmd, namespace)
    # print(f"Namespace: {namespace}\n")

def azl_process_aks_create_namespace(cmd, namespace):
    # print("Processing AKS create namespace...")
    # print(f"Namespace: {namespace}\n")
    add_azsecpack_nodepool_tags(namespace)
    # print(f"Namespace: {namespace}\n")
