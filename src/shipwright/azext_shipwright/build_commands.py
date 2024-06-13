# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.log import get_logger
from typing import OrderedDict
import azext_shipwright.build_pipeline_constants

logger = get_logger(__name__)


class DefinitionPlaceholder:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class BuildPlaceholder:
    def __init__(self, known_pipeline, include_url):
        self.definition = DefinitionPlaceholder(
            known_pipeline.pipeline_id, known_pipeline.pipeline_name
        )

        if include_url:
            self.ui_url = known_pipeline.url


def make_definition_placeholder(known_pipeline, include_url):
    return BuildPlaceholder(known_pipeline, include_url)
    # return {
    #     "definition": {
    #         "id": known_pipeline.pipeline_id,
    #         "name": known_pipeline.pipeline_name,
    #     },
    #     "uiUrl": known_pipeline.url,
    # }


def build_get(cmd, build_id, include_url=False):
    logger.debug(
        f"get_build_status_shipwright: build_id={build_id}, include_url={include_url}"
    )

    runs = []

    build_client = get_devops_build_client()

    # Get the build they requested.
    requested_build = build_client.get_build(
        project=azext_shipwright.build_pipeline_constants.PIPELINE_PROJECT,
        build_id=build_id,
    )
    runs.append(requested_build)

    # See if there are any related pipelines:
    related_pipelines = (
        azext_shipwright.build_pipeline_constants.find_pipeline_set_by_id(
            requested_build.definition.id
        )
    )

    # Now search for all builds with the same build number in the known pipelines
    if related_pipelines:
        runs += build_client.get_builds(
            project="mariner",
            definitions=(
                pipeline.pipeline_id
                for pipeline in related_pipelines
                if pipeline.pipeline_id != requested_build.definition.id
            ),
            build_number=requested_build.build_number,
        )

    # If requested, augment the data with the human-usable URL of the build.
    if include_url:
        from urllib import parse

        for run in runs:
            url = parse.urlunsplit(
                parse.urlsplit(run.url)
                ._replace(
                    path=f"/mariner-org/{run.definition.project.name}/_build/results"
                )
                ._replace(query=parse.urlencode({"buildid": run.id, "view": "results"}))
            )
            setattr(run, "ui_url", url)

    related_builds = OrderedDict(
        (pipeline.pipeline_id, make_definition_placeholder(pipeline, include_url))
        for pipeline in related_pipelines
    )
    for run in runs:
        related_builds[run.definition.id] = run

    return list(related_builds.values())


def get_devops_build_client():
    # Call the devops extension to get build information
    from azure.identity import AzureCliCredential
    from msrest.authentication import BasicAuthentication
    from azure.devops.connection import Connection

    credential = AzureCliCredential()
    auth = BasicAuthentication(
        username="",
        password=credential.get_token("499b84ac-1321-427f-aa17-267ca6975798").token,
    )
    connection = Connection(
        base_url=azext_shipwright.build_pipeline_constants.PIPELINE_ORG, creds=auth
    )
    return connection.clients.get_build_client()


def build_known_pipelines(cmd):
    return azext_shipwright.build_pipeline_constants._KNOWN_PIPELINES


def transform_get_build_status_output(build_results):
    table_output = []
    for build in build_results:
        data = OrderedDict()
        data["Pipeline ID"] = build["definition"]["id"]
        data["Pipeline Name"] = build["definition"]["name"]
        data["Run ID"] = build["id"] if "id" in build else None
        data["Build Number"] = build["buildNumber"] if "buildNumber" in build else None
        data["Status"] = build["status"] if "status" in build else None
        data["Result"] = build["result"] if "result" in build else None
        data["UI Url"] = build["uiUrl"] if "uiUrl" in build else None

        table_output.append(data)

    return table_output
