from cfnc.cfnc_api import cfnc_api_resource, cfnc_ccp_api_resource
from dagster import make_values_resource, multiprocess_executor
from dagster_aws.s3.resources import s3_resource
from dynamodb import dynamodb_resource
from element.resources import webexportapi_resource, webimportapi_resource
from mongodb import mongodb_resource
from sentry import sentry_resource
from shared_resources import custom_s3_io_manager, secrets_resource
from slack import slack_resource
from translator import cfnc_translator_resource

from client.graphs import cfnc_import_applications_from_mongo_graph
from client.jobs.tags import cfnc_tags
from client.src.secrets_config import get_region, get_secrets_config

cfnc_import_applications_from_mongo_job = (
    cfnc_import_applications_from_mongo_graph.to_job(
        name="cfnc_import_applications_from_mongo_job",
        resource_defs={
            "secrets": secrets_resource.configured(get_secrets_config()),
            "s3": s3_resource.configured(get_region()),
            "mongo": mongodb_resource,
            "cfnc_api": cfnc_api_resource,
            "webimportapi": webimportapi_resource,
            "webexportapi": webexportapi_resource,
            "slack": slack_resource,
            "dynamodb": dynamodb_resource,
            "sentry": sentry_resource,
            "translator": cfnc_translator_resource,
            "io_manager": custom_s3_io_manager,
            "values": make_values_resource(cfnc_app_id=str),
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)

cfnc_import_ccp_applications_from_mongo_job = (
    cfnc_import_applications_from_mongo_graph.to_job(
        name="cfnc_import_ccp_applications_in_mongo_job",
        resource_defs={
            "secrets": secrets_resource.configured(get_secrets_config()),
            "s3": s3_resource.configured(get_region()),
            "mongo": mongodb_resource,
            "cfnc_api": cfnc_ccp_api_resource,
            "webimportapi": webimportapi_resource,
            "webexportapi": webexportapi_resource,
            "slack": slack_resource,
            "dynamodb": dynamodb_resource,
            "sentry": sentry_resource,
            "translator": cfnc_translator_resource,
            "io_manager": custom_s3_io_manager,
            "values": make_values_resource(cfnc_app_id=str),
        },
        executor_def=multiprocess_executor,
        tags=cfnc_tags,
    )
)
