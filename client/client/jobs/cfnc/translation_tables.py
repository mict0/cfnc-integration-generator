from dagster import job, make_values_resource, multiprocess_executor
from mongodb import mongodb_resource
from sentry import sentry_resource
from shared_resources import secrets_resource

from client.jobs.tags import cfnc_tags
from client.ops.cfnc.translation_tables import (
    cfnc_translation_tables_update_graph,
    tt_job_config,
)
from client.src.secrets_config import get_secrets_config


@job(
    resource_defs={
        "secrets": secrets_resource.configured(get_secrets_config()),
        "mongo": mongodb_resource,
        "sentry": sentry_resource,
        "values": make_values_resource(**{"other_system": str}),
    },
    executor_def=multiprocess_executor,
    config=tt_job_config,
    tags=cfnc_tags,
)
def cfnc_translation_tables_update_job():
    cfnc_translation_tables_update_graph()
