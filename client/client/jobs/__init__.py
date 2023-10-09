from .cfnc import (
    cfnc_download_and_import_documents_in_element_job,
    cfnc_import_applications_from_mongo_job,
    cfnc_save_applications_in_mongo_job,
    cfnc_translation_tables_update_job,
)

jobs = [
    cfnc_import_applications_from_mongo_job,
    cfnc_save_applications_in_mongo_job,
    cfnc_translation_tables_update_job,
    cfnc_download_and_import_documents_in_element_job,
]
from .tags import cfnc_tags, ethos_tags
