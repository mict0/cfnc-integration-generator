from datetime import datetime

from dagster import (
    DefaultSensorStatus,
    RunRequest,
    SensorEvaluationContext,
    SkipReason,
    build_resources,
    sensor,
)
from dynamodb import Attr, Key, dynamodb_resource
from shared_resources import secrets_resource

from client.jobs import cfnc_transcripts_decide_api_to_use_job
from client.src.integration_start_date import INTEGRATION_START_DATE
from client.src.secrets_config import get_secrets_config


@sensor(
    job=cfnc_transcripts_decide_api_to_use_job,
    minimum_interval_seconds=60,
    default_status=DefaultSensorStatus.STOPPED,
)
def cfnc_transcripts_decide_api_to_use_sensor(context: SensorEvaluationContext):
    """Sensor to decide which API to use for CFNC Transcripts Import"""

    def _deduplicate_event_users(items, fiter_field="user_id"):
        """
        Returns List[dict], filtered by filter field
        """
        return list({item[fiter_field]: item for item in items}.values())

    last_timestamp = (
        context.cursor
        if context.cursor
        else datetime.fromtimestamp(INTEGRATION_START_DATE).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    )
    max_timestamp = last_timestamp

    with build_resources(
        {
            "secrets": secrets_resource.configured(get_secrets_config()),
            "dynamo": dynamodb_resource,
        }
    ) as resources:
        subdom = resources.secrets.get("subdom")
        events_table = resources.secrets.get("dynamodb_events_table")
        dynamo_index = resources.secrets.get("dynamodb_events_index")

        query_table = resources.dynamo.db.Table(events_table).query(
            IndexName=dynamo_index,
            KeyConditionExpression=Key("timestamp").gt(dt_query_format(last_timestamp))
            & Key("subdom").eq(subdom),
            FilterExpression=Attr("event_type").eq("cfnc_transcript_import"),
        )
        students = _deduplicate_event_users(query_table["Items"])

    if len(students) == 0:
        return SkipReason(skip_message="No new students found.")

    element_ids = [student["user_id"] for student in students]
    max_timestamp = get_max_timestamp_students(students)
    run_config = {
        "resources": {
            "values": {
                "config": {
                    "element_ids": element_ids,
                    "scheduled_date": convert_to_scheduled_format(max_timestamp),
                }
            }
        },
    }
    yield RunRequest(
        run_key=None,
        run_config=run_config,
        tags={"cfnc": subdom, "timestamp": f"{last_timestamp}-{max_timestamp}"},
    )

    context.update_cursor(max_timestamp)


def get_max_timestamp_students(students):
    max_ts = "1970-01-01T00:00:00.000Z"
    for student in students:
        max_ts = get_max_timestamp(max_ts, student["timestamp"])
    return max_ts


def get_max_timestamp(ts1, ts2) -> str:
    """
    Takes two arguments and returns the maximum timestamp
    """

    def _convert_to_dt(str_timestamp):
        try:
            return datetime.strptime(str_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            return datetime.min

    max_ts = max(_convert_to_dt(ts1), _convert_to_dt(ts2))
    return max_ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def dt_query_format(dt_str) -> str:
    date_object = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"


def convert_to_scheduled_format(dt_str):
    date_object = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.strftime("%Y-%m-%d %H:%M:%S")
