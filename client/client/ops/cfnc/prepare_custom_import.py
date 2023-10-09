from typing import List

from dagster import OpExecutionContext, op
from element.api.webimportapi import WebImportBody
from shared_resources import pretty_print

from .handle_custom_columns import prepare_custom_columns


@op
def prepare_custom_import_parts_op(
    context: OpExecutionContext,
    applications: List[dict],
) -> List[WebImportBody]:
    """Prepares custom fields from the cfnc application"""
    processed_applications: List[WebImportBody] = []
    for i, cfnc_application in enumerate(applications, start=1):
        try:
            import_body = WebImportBody(action="upsert", options={"keyBy": "field"})
            context.log.info(f"Processing application [{i}/{len(applications)}]")
            custom_columns = prepare_custom_columns(cfnc_application)
            import_body.add_columns(custom_columns)
            import_body.generate_body()
            import_body.cfnc_id = cfnc_application["identities"]["cfnc_id"]
            import_body.cfnc_app_id = cfnc_application["applications"][0]["external_id"]

            processed_applications.append(import_body)

        except Exception as e:
            context.log.exception(
                f"Something went wrong during processing: {e}\nFailed application: {pretty_print(cfnc_application)}"
            )
            continue

    return processed_applications
