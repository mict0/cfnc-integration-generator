from cfnc.cfnc_api import cfnc_api_resource, cfnc_ccp_api_resource
from cfnc.graphs import (
    cfnc_download_and_import_transcripts_graph,
    cfnc_transcripts_filter_student_by_app_type_graph,
)
from dagster import make_values_resource, multiprocess_executor
from dagster_aws.s3 import s3_resource
from dynamodb import dynamodb_resource
from element.resources import (
    taskapi_resource,
    webexportapi_resource,
    webimportapi_resource,
)
from mongodb import mongodb_resource
from sentry import sentry_resource
from shared_resources import (
    custom_s3_io_manager,
    dagster_cloud_graphql_resource,
    secrets_resource,
)
from slack import slack_resource

from client.jobs.tags import cfnc_tags
from client.src import get_region, get_secrets_config

cfnc_download_and_import_transcripts_job = (
    cfnc_download_and_import_transcripts_graph.to_job(
        name="cfnc_download_and_import_transcripts_job",
        resource_defs={
            "secrets": secrets_resource.configured(get_secrets_config()),
            "s3": s3_resource.configured(get_region()),
            "cfnc_api": cfnc_api_resource,
            "mongo": mongodb_resource,
            "webimportapi": webimportapi_resource,
            "webexportapi": webexportapi_resource,
            "taskapi": taskapi_resource,
            "slack": slack_resource,
            "dynamodb": dynamodb_resource,
            "sentry": sentry_resource,
            "values": make_values_resource(
                **{"element_ids": list, "scheduled_date": str}
            ),
            "io_manager": custom_s3_io_manager,
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)
cfnc_download_and_import_ccp_transcripts_job = (
    cfnc_download_and_import_transcripts_graph.to_job(
        name="cfnc_download_and_import_ccp_transcripts_job",
        resource_defs={
            "secrets": secrets_resource.configured(get_secrets_config()),
            "s3": s3_resource.configured(get_region()),
            "cfnc_api": cfnc_ccp_api_resource,
            "mongo": mongodb_resource,
            "webimportapi": webimportapi_resource,
            "webexportapi": webexportapi_resource,
            "taskapi": taskapi_resource,
            "slack": slack_resource,
            "dynamodb": dynamodb_resource,
            "sentry": sentry_resource,
            "values": make_values_resource(
                **{"element_ids": list, "scheduled_date": str}
            ),
            "io_manager": custom_s3_io_manager,
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)

cfnc_transcripts_decide_api_to_use_job = (
    cfnc_transcripts_filter_student_by_app_type_graph.to_job(
        name="cfnc_transcripts_filter_student_by_app_type_job",
        resource_defs={
            "secrets": secrets_resource.configured(get_secrets_config()),
            "s3": s3_resource.configured(get_region()),
            "mongo": mongodb_resource,
            "dagster_cloud_graphql": dagster_cloud_graphql_resource,
            "slack": slack_resource,
            "dynamodb": dynamodb_resource,
            "cfnc_api": cfnc_api_resource,
            "sentry": sentry_resource,
            "values": make_values_resource(
                **{"element_ids": list, "scheduled_date": str}
            ),
            "io_manager": custom_s3_io_manager,
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)
