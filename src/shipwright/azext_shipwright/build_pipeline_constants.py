PIPELINE_ORG = "https://dev.azure.com/mariner-org"
PIPELINE_PROJECT = "mariner"


class KnownPipeline:
    def __init__(self, moniker, pipeline_id, pipeline_name):
        self.moniker = moniker
        self.pipeline_name = pipeline_name
        self.pipeline_id = pipeline_id
        self.url = f"https://dev.azure.com/mariner-org/mariner/_build?definitionId={self.pipeline_id}"

    def __str__(self):
        return f"['{self.moniker}', '{self.pipeline_name}' '{self.pipeline_id}']"

    def __repr__(self) -> str:
        return self.__str__()


DEV_PREPARE_BUILD = KnownPipeline(
    "dev-prepare-build",
    2064,
    "[NoArch-0-OneBranch]-Dev-PrepareBuild",
)
DEV_AMD_BUILD_TOOL_CHAIN = KnownPipeline(
    "dev-amd-build-tool-chain",
    2118,
    "[AMD64-1-OneBranch]-Dev-BuildToolChain",
)
DEV_ARM_BUILD_TOOL_CHAIN = KnownPipeline(
    "dev-arm-build-tool-chain",
    2119,
    "[ARM-1-OneBranch]-Dev-BuildToolChain",
)
DEV_AMD_BUILD_RPMS = KnownPipeline(
    "dev-amd-build-rpms",
    1225,
    "[AMD64-2-OneBranch]-Dev-BuildRpms",
)
DEV_ARM_BUILD_RPMS = KnownPipeline(
    "dev-arm-build-rpms",
    2090,
    "[ARM-2-OneBranch]-Dev-BuildRpms",
)
DEV_AMD_BUILD_IMAGES = KnownPipeline(
    "dev-amd-build-images",
    2120,
    "[AMD64-3-OneBranch]-Dev-BuildImages",
)
DEV_ARM_BUILD_IMAGES = KnownPipeline(
    "dev-arm-build-images",
    2121,
    "[ARM-3-OneBranch]-Dev-BuildImages",
)
DEV_AMD_BUILD_GOLDEN_CONTAINERS = KnownPipeline(
    "dev-amd-build-golden-containers",
    2733,
    "[AMD64-4-OneBranch]-Dev-BuildGoldenContainers",
)
DEV_ARM_BUILD_GOLDEN_CONTAINERS = KnownPipeline(
    "dev-arm-build-golden-containers",
    2734,
    "[ARM64-OneBranch]-Dev-BuildGoldenContainers",
)

PROD_PREPARE_BUILD = KnownPipeline(
    "prod-prepare-build",
    2062,
    "[NoArch-0-OneBranch]-Prod-PrepareBuild",
)
PROD_AMD_BUILD_TOOL_CHAIN = KnownPipeline(
    "prod-amd-build-tool-chain",
    2114,
    "[AMD64-1-OneBranch]-Prod-BuildToolChain",
)
PROD_ARM_BUILD_TOOL_CHAIN = KnownPipeline(
    "prod-arm-build-tool-chain",
    2115,
    "[ARM-1-OneBranch]-Prod-BuildToolChain",
)
PROD_AMD_BUILD_RPMS = KnownPipeline(
    "prod-amd-build-rpms",
    2037,
    "[AMD64-2-OneBranch]-Prod-BuildRpms",
)
PROD_ARM_BUILD_RPMS = KnownPipeline(
    "prod-arm-build-rpms",
    2094,
    "[ARM-2-OneBranch]-Prod-BuildRpms",
)
PROD_AMD_SECURE_BOOT_SIGN_RPMS = KnownPipeline(
    "prod-amd-secure-boot-signing",
    2065,
    "[AMD64-3-OneBranch]-Prod-SecureBootSignRpms",
)
PROD_ARM_SECURE_BOOT_SIGN_RPMS = KnownPipeline(
    "prod-arm-secure-boot-signing",
    2095,
    "[ARM-3-OneBranch]-Prod-SecureBootSignRpms",
)
PROD_AMD_SECURE_BOOT_BUILD_RPMS = KnownPipeline(
    "prod-amd-secure-boot-build-rpms",
    2080,
    "[AMD64-4-OneBranch]-Prod-SecureBootBuildRpms",
)
PROD_ARM_SECURE_BOOT_BUILD_RPMS = KnownPipeline(
    "prod-arm-secure-boot-build-rpms",
    2096,
    "[ARM64-OneBranch]-Prod-SecureBootBuildRpms",
)
PROD_AMD_SIGN_RPMS = KnownPipeline(
    "prod-amd-sign-rpms",
    2039,
    "[AMD64-5-OneBranch]-Prod-SignRpms",
)
PROD_ARM_SIGN_RPMS = KnownPipeline(
    "prod-arm-sign-rpms",
    2097,
    "[ARM-5-OneBranch]-Prod-SignRpms",
)
PROD_AMD_BUILD_IMAGES = KnownPipeline(
    "prod-amd-build-images",
    2116,
    "[AMD64-6-OneBranch]-Prod-BuildImages",
)
PROD_ARM_BUILD_IMAGES = KnownPipeline(
    "prod-arm-build-images",
    2117,
    "[ARM-6-OneBranch]-Prod-BuildImages",
)
PROD_AMD_BUILD_GOLDEN_CONTAINERS = KnownPipeline(
    "prod-amd-build-golden-containers",
    2902,
    "[AMD64-7-OneBranch]-Prod-BuildGoldenContainers",
)
PROD_ARM_BUILD_GOLDEN_CONTAINERS = KnownPipeline(
    "prod-arm-build-golden-containers",
    2905,
    "[ARM-7-OneBranch]-Prod-BuildGoldenContainers",
)

BUDDY_BUILD = KnownPipeline(
    "buddy-build",
    2190,
    "[OneBranch]-Unified-Buddy-Build",
)

PIPELINE_SETS = {
    "dev-official-builds": [
        DEV_PREPARE_BUILD,
        DEV_AMD_BUILD_TOOL_CHAIN,
        DEV_ARM_BUILD_TOOL_CHAIN,
        DEV_AMD_BUILD_RPMS,
        DEV_ARM_BUILD_RPMS,
        DEV_AMD_BUILD_IMAGES,
        DEV_ARM_BUILD_IMAGES,
        DEV_AMD_BUILD_GOLDEN_CONTAINERS,
        DEV_ARM_BUILD_GOLDEN_CONTAINERS,
    ],
    "prod-official-builds": [
        PROD_PREPARE_BUILD,
        PROD_AMD_BUILD_TOOL_CHAIN,
        PROD_ARM_BUILD_TOOL_CHAIN,
        PROD_AMD_BUILD_RPMS,
        PROD_ARM_BUILD_RPMS,
        PROD_AMD_SECURE_BOOT_SIGN_RPMS,
        PROD_ARM_SECURE_BOOT_SIGN_RPMS,
        PROD_AMD_SECURE_BOOT_BUILD_RPMS,
        PROD_ARM_SECURE_BOOT_BUILD_RPMS,
        PROD_AMD_SIGN_RPMS,
        PROD_ARM_SIGN_RPMS,
        PROD_AMD_BUILD_IMAGES,
        PROD_ARM_BUILD_IMAGES,
        PROD_AMD_BUILD_GOLDEN_CONTAINERS,
        PROD_ARM_BUILD_GOLDEN_CONTAINERS,
    ],
    "buddy": [BUDDY_BUILD],
}

# _KNOWN_PIPELINES is a list of all known pipelines, as determined by the pipeline sets
_KNOWN_PIPELINES = [
    pipeline for pipeline_set in PIPELINE_SETS.values() for pipeline in pipeline_set
]


def find_pipeline_set_by_id(pipeline_id):
    known_pipeline = find_known_pipeline_by_id(pipeline_id)
    if not known_pipeline:
        return []

    for pipeline_set in PIPELINE_SETS.values():
        accum = []
        found = False
        for pipeline in pipeline_set:
            if pipeline.pipeline_id == pipeline_id:
                found = True

            accum.append(pipeline)

        if found:
            return accum

    return []


def find_known_pipeline_by_moniker(moniker):
    return _find_known_pipeline(lambda pipeline: pipeline.moniker == moniker)


def find_known_pipeline_by_id(pipeline_id):
    return _find_known_pipeline(lambda pipeline: pipeline.pipeline_id == pipeline_id)


def _find_known_pipeline(test):
    return next((pipeline for pipeline in _KNOWN_PIPELINES if test(pipeline)), None)
