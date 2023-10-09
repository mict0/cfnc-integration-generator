from cfnc.cfnc_api import cfnc_api_resource
from cfnc.graphs import cfnc_download_and_import_documents_in_element_graph
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
from shared_resources import custom_s3_io_manager, secrets_resource
from slack import slack_resource

from client.jobs.tags import cfnc_tags
from client.src import get_region, get_secrets_config

cfnc_download_and_import_documents_in_element_job = (
    cfnc_download_and_import_documents_in_element_graph.to_job(
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
                **{"student_cfnc_ids": list, "scheduled_date": str}
            ),
            "io_manager": custom_s3_io_manager,
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)
