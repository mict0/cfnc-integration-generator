from dagster import RunRequest, ScheduleEvaluationContext, schedule

from client.jobs import cfnc_download_and_import_documents_in_element_job, cfnc_tags


@schedule(
    job=cfnc_download_and_import_documents_in_element_job, cron_schedule="30 * * * *"
)
def cfnc_documents_load_and_import_cron(context: ScheduleEvaluationContext):
    scheduled_date = context.scheduled_execution_time.strftime("%Y-%m-%d %H:%M:%S")
    return RunRequest(
        run_config={
            "resources": {
                "values": {
                    "config": {"scheduled_date": scheduled_date, "student_cfnc_ids": []}
                }
            }
        },
        tags={"date": scheduled_date, **cfnc_tags},
    )
