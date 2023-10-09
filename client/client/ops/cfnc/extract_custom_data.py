from typing import List

from cfnc.cfnc_type import safely_get
from cfnc.extract_data import extract_application_data, merge_cfnc_applications
from dagster import OpExecutionContext, op
from element.api.element_type import remove_none_values
from shared_resources import pretty_print

from .custom_client_cfnc_type import ClientCFNC


@op
def extract_cfnc_applications_data_op(
    context: OpExecutionContext, cfnc_applications: list
) -> List[dict]:
    custom_apps = [
        override_custom_cfnc_applications_data(app) for app in cfnc_applications
    ]
    context.log.info(
        f"After extracting custom data, applications:{pretty_print(custom_apps)}"
    )
    return custom_apps


def extract_custom_application_data(cfnc_application: dict) -> dict:
    """Extracts the data from applications specific to the Forsythtech"""
    app_data = cfnc_application.get("applicationResponse")
    user_data = cfnc_application.get("user")
    custom_data = ClientCFNC()
    custom_data["identities"] = {"cfnc_id": user_data.get("cfncUserId")}
    get_educational_goal(custom_data, app_data)
    get_employment_information(custom_data, app_data)
    get_educational_levels(custom_data, app_data)
    get_enrollment_information(custom_data, app_data)
    get_financial_aid(custom_data, app_data)
    get_drivers_license(custom_data, app_data)
    custom_data["homeless_individual"] = app_data.get("homelessIndividual", "")
    custom_data["foster_care"] = app_data.get("fosterCare", "")
    custom_data["migrant_farmworker"] = app_data.get("migrantFarmworker", "")
    custom_data["hs_track"] = app_data.get("nccchsTrack", "")
    custom_data["residency_status"] = app_data.get("residencyIndicator", "")

    remove_none_values(custom_data)
    return custom_data


def override_custom_cfnc_applications_data(cfnc_application: dict) -> dict:
    default_data = extract_application_data(cfnc_application)
    custom_data = extract_custom_application_data(cfnc_application)
    return merge_cfnc_applications(default_data, custom_data)


def get_educational_goal(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["educational_goal"] = app_data.get("educationGoals", "")


def get_employment_information(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["employment_information"] = app_data.get("ncccEmploymentStatus", "")


def get_educational_levels(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["educational_level"] = {
        "student": app_data.get("studentHighestEducationalLvl", ""),
        "father": app_data.get("parent1EducationLevel", ""),
        "mother": app_data.get("parent2EducationLevel", ""),
    }


def get_enrollment_information(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["enrollment_information"] = {
        "enrollment_status": app_data.get("enrollmentStatus", ""),
        "suspended_or_expelled": safely_get(app_data, "ynSuspendedExpelled"),
    }


def get_financial_aid(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["applying_for_fin_aid"] = safely_get(
        app_data, "ynApplyingForFinancialAid"
    )


def get_drivers_license(custom_data: ClientCFNC, app_data: dict) -> None:
    custom_data["drivers_license"] = {
        "have_license": safely_get(app_data, "ynHaveDriversLicense"),
        "state": app_data.get("driverLicenseState", ""),
        "number": app_data.get("driverLicenseNumber", ""),
    }
