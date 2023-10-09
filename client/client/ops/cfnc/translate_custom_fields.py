from typing import List, cast

from dagster import OpExecutionContext, op
from shared_resources import pretty_print
from translator import Translator

from .custom_client_cfnc_type import ClientCFNC


@op(required_resource_keys={"translator"})
def translate_custom_data_op(
    context: OpExecutionContext, cfnc_applications: List[dict]
) -> List[dict]:
    return [translate_application(context, app) for app in cfnc_applications]


def translate_application(
    context: OpExecutionContext, cfnc_app: ClientCFNC
) -> ClientCFNC:
    translator = cast(Translator, context.resources.translator)
    translation_tables = list(translator.translation_tables.keys())
    context.log.info(
        f"Found {len(translation_tables)} translation tables, and those are: {pretty_print(translation_tables)}"
    )

    if "employment_statuses" in translation_tables and cfnc_app.get(
        "employment_information"
    ):
        try:
            cfnc_app["employment_information"] = translator.translate_for_element(
                "employment_statuses", cfnc_app["employment_information"]
            )
        except:
            cfnc_app["employment_information"] = ""

    if "educational_levels" in translation_tables and cfnc_app.get("educational_level"):
        educational_levels = cfnc_app["educational_level"]
        if educational_levels.get("father"):
            try:
                educational_levels[
                    "father"
                ] = translator.translate_educational_level_for_element(
                    educational_levels["father"]
                )
            except:
                educational_levels["father"] = ""
        if educational_levels.get("mother"):
            try:
                educational_levels[
                    "mother"
                ] = translator.translate_educational_level_for_element(
                    educational_levels["mother"]
                )
            except:
                educational_levels["mother"] = ""
        if educational_levels.get("student"):
            try:
                educational_levels["student"] = translator.translate_for_element(
                    "student_education_levels", educational_levels["student"]
                )
            except:
                educational_levels["student"] = ""
    if "academic_loads" in translation_tables and cfnc_app.get(
        "enrollment_information", {}
    ).get("enrollment_status"):
        try:
            cfnc_app["enrollment_information"][
                "enrollment_status"
            ] = translator.translate_academic_load_for_element(
                cfnc_app["enrollment_information"]["enrollment_status"],
            )
        except:
            cfnc_app["enrollment_information"]["enrollment_status"] = ""

    context.log.info(f"The application: {pretty_print(cfnc_app)}")
    return cfnc_app
