from typing import List, Optional

from cfnc.ops.import_to_element.prepare_common_import import value_to_yn

from .custom_client_cfnc_type import ClientCFNC


def prepare_custom_columns(
    cfnc_application: ClientCFNC, custom_columns: Optional[List[dict]] = None
) -> List[dict]:
    if custom_columns is None:
        custom_columns = []
    add_educational_goal(custom_columns, cfnc_application)
    add_employment_information(custom_columns, cfnc_application)
    add_education_level(custom_columns, cfnc_application)
    add_enrollment_information(custom_columns, cfnc_application)
    add_financial_aid(custom_columns, cfnc_application)
    add_additional_information(custom_columns, cfnc_application)

    return custom_columns


def add_educational_goal(
    custom_columns: List[dict], cfnc_application: ClientCFNC
) -> None:
    if "educational_goal" in cfnc_application:
        custom_columns.append(
            {
                "field": "educational_goal",
                "slug": "user-custom-client-education-goal",
                "mode": "slug",
                "value": cfnc_application["educational_goal"],
            }
        )


def add_employment_information(
    custom_columns: List[dict], cfnc_application: ClientCFNC
) -> None:
    if "employment_information" in cfnc_application:
        custom_columns.append(
            {
                "field": "employment_status",
                "slug": "user-custom-client-employment-status",
                "mode": "slug",
                "value": cfnc_application["employment_information"],
            }
        )


def add_education_level(
    custom_columns: List[dict], cfnc_application: ClientCFNC
) -> None:
    if "educational_level" in cfnc_application:
        education_levels = cfnc_application["educational_level"]
        custom_columns.extend(
            [
                {
                    "field": "fathersed",
                    "slug": "user-custom-client-ccp-father-ed",
                    "mode": "slug",
                    "value": education_levels.get("father"),
                },
                {
                    "field": "mothersed",
                    "slug": "user-custom-client-cc-mother-ed",
                    "mode": "slug",
                    "value": education_levels.get("mother"),
                },
                {
                    "field": "studentsed",
                    "slug": "user-custom-client-education-level",
                    "mode": "slug",
                    "value": education_levels.get("student"),
                },
            ]
        )


def add_enrollment_information(
    custom_columns: List[dict], cfnc_application: ClientCFNC
) -> None:
    if "enrollment_information" in cfnc_application:
        enrollment_info = cfnc_application["enrollment_information"]
        custom_columns.extend(
            [
                {
                    "field": "suspended_expelled",
                    "slug": "user-custom-client-expelled-status",
                    "mode": "slug",
                    "value": value_to_yn(
                        enrollment_info.get("suspended_or_expelled", "")
                    ),
                },
                {
                    "field": "enrollment_status",
                    "slug": "user-education-academic-load",
                    "mode": "slug",
                    "value": enrollment_info.get("enrollment_status", ""),
                },
            ]
        )


def add_financial_aid(custom_columns: List[dict], cfnc_application: ClientCFNC) -> None:
    if "applying_for_fin_aid" in cfnc_application:
        custom_columns.append(
            {
                "field": "applying_for_fin_aid",
                "slug": "user-custom-client-financial-aid",
                "mode": "slug",
                "value": value_to_yn(cfnc_application["applying_for_fin_aid"]),
            }
        )


def add_additional_information(
    custom_columns: List[dict], cfnc_application: ClientCFNC
) -> None:
    custom_columns.extend(
        [
            {
                "field": "homeless_individual",
                "slug": "user-custom-client-homeless",
                "mode": "slug",
                "value": value_to_yn(cfnc_application.get("homeless_individual", "")),
            },
            {
                "field": "foster_care",
                "slug": "user-custom-client-foster-care",
                "mode": "slug",
                "value": value_to_yn(cfnc_application.get("foster_care", "")),
            },
            {
                "field": "migrant_farmworker",
                "slug": "user-custom-client-migrant-farmworker",
                "mode": "slug",
                "value": value_to_yn(cfnc_application.get("migrant_farmworker", "")),
            },
        ]
    )
