from dagster import RunRequest, ScheduleEvaluationContext, schedule

from client.jobs import cfnc_import_applications_from_mongo_job, cfnc_tags


@schedule(
    job=cfnc_import_applications_from_mongo_job,
    cron_schedule="10 * * * *",
    execution_timezone="US/Eastern",
)
def cfnc_mongo_to_element_import_cron(context: ScheduleEvaluationContext):
    return RunRequest(
        run_config={"resources": {"values": {"config": {"cfnc_app_id": ""}}}},
        tags=cfnc_tags,
        run_key=None,
    )
