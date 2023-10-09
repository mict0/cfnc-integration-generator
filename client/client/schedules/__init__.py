from .cfnc_applications_import import cfnc_load_applications_in_mongo_cron
from .cfnc_documents_import import cfnc_documents_load_and_import_cron
from .cfnc_mongo_to_element_import import cfnc_mongo_to_element_import_cron

schedules = [
    cfnc_documents_load_and_import_cron,
    cfnc_load_applications_in_mongo_cron,
    cfnc_mongo_to_element_import_cron,
]
