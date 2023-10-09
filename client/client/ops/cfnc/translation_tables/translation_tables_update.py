from dagster import graph

from .academic_loads import sync_academic_loads_translation_table_cfnc
from .citizenship_statuses import sync_citizenship_statuses_translation_table_cfnc
from .education_level import sync_educational_level_translation_table_cfnc
from .genders import sync_genders_translation_table_cfnc
from .majors import sync_majors_translation_table_cfnc
from .races import sync_races_translation_table_cfnc
from .student_types import sync_student_types_translation_table_cfnc
from .terms import sync_terms_translation_table_cfnc


@graph()
def cfnc_translation_tables_update_graph():
    sync_genders_translation_table_cfnc()
    sync_majors_translation_table_cfnc()
    sync_races_translation_table_cfnc()
    sync_terms_translation_table_cfnc()
    sync_student_types_translation_table_cfnc()
    sync_academic_loads_translation_table_cfnc()
    sync_citizenship_statuses_translation_table_cfnc()
    # sync_educational_level_translation_table_cfnc()
