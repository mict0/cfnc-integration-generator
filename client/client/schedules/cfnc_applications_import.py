import json
from datetime import datetime, timedelta

from dagster import RunRequest, ScheduleEvaluationContext, schedule

from client.jobs import (
    cfnc_save_applications_in_mongo_job,
    cfnc_save_ccp_applications_in_mongo_job,
    cfnc_tags,
)


@schedule(job=cfnc_save_applications_in_mongo_job, cron_schedule="0 * * * *")
def cfnc_load_applications_in_mongo_cron(context: ScheduleEvaluationContext):
    scheduled_date = parse_dt_to_string(context.scheduled_execution_time)
    start_date = parse_dt_to_string(
        context.scheduled_execution_time - timedelta(hours=1)
    )
    return RunRequest(
        run_config={
            "resources": {
                "values": {
                    "config": {"start_date": start_date, "end_date": scheduled_date}
                }
            }
        },
        tags={
            "dates": json.dumps({"start": start_date, "end": scheduled_date}),
            **cfnc_tags,
        },
        run_key=None,
    )


@schedule(job=cfnc_save_ccp_applications_in_mongo_job, cron_schedule="0 * * * *")
def cfnc_load_ccp_applications_in_mongo_cron(context: ScheduleEvaluationContext):
    scheduled_date = parse_dt_to_string(context.scheduled_execution_time)
    start_date = parse_dt_to_string(
        context.scheduled_execution_time - timedelta(hours=1)
    )
    return RunRequest(
        run_config={
            "resources": {
                "values": {
                    "config": {"start_date": start_date, "end_date": scheduled_date}
                }
            }
        },
        tags={
            "dates": json.dumps({"start": start_date, "end": scheduled_date}),
            **cfnc_tags,
        },
        run_key=None,
    )


def parse_dt_to_string(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + dt.strftime(".%f")[:4] + "Z"
