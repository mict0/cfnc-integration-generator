from cfnc.cfnc_api import cfnc_api_resource
from cfnc.graphs import cfnc_save_applications_in_mongo_graph
from dagster import make_values_resource, multiprocess_executor
from dagster_aws.s3.resources import s3_resource
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

cfnc_save_applications_in_mongo_job = cfnc_save_applications_in_mongo_graph.to_job(
    name="cfnc_save_applications_in_mongo_job",
    resource_defs={
        "secrets": secrets_resource.configured(get_secrets_config()),
        "s3": s3_resource.configured(get_region()),
        "mongo": mongodb_resource,
        "cfnc_api": cfnc_api_resource,
        "webimportapi": webimportapi_resource,
        "webexportapi": webexportapi_resource,
        "taskapi": taskapi_resource,
        "slack": slack_resource,
        "dynamodb": dynamodb_resource,
        "sentry": sentry_resource,
        "values": make_values_resource(**{"start_date": str, "end_date": str}),
        "io_manager": custom_s3_io_manager,
    },
    executor_def=multiprocess_executor,
    tags=cfnc_tags,
)

cfnc_save_ccp_applications_in_mongo_job = cfnc_save_applications_in_mongo_graph.to_job(
    name="cfnc_save_ccp_applications_in_mongo_job",
    resource_defs={
        "secrets": secrets_resource.configured(get_secrets_config()),
        "s3": s3_resource.configured(get_region()),
        "mongo": mongodb_resource,
        "cfnc_api": cfnc_ccp_api_resource,
        "webimportapi": webimportapi_resource,
        "webexportapi": webexportapi_resource,
        "taskapi": taskapi_resource,
        "slack": slack_resource,
        "dynamodb": dynamodb_resource,
        "sentry": sentry_resource,
        "values": make_values_resource(**{"start_date": str, "end_date": str}),
        "io_manager": custom_s3_io_manager,
    },
    executor_def=multiprocess_executor,
    tags=cfnc_tags,
)
