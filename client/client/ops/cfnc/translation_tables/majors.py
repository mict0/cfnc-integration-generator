from dagster import OpExecutionContext, graph, op
from shared_resources import pretty_print
from translator import (
    get_element_main_data_source_op,
    update_translation_table_in_mongo_op,
)


@op
def create_majors_translation_table_op(
    context: OpExecutionContext, element_majors: list
) -> dict:
    translation_table = {major["guid"]: major["code"] for major in element_majors}

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table


get_element_majors_op = get_element_main_data_source_op.alias("get_element_majors_op")
update_majors_translation_in_mongo_op = update_translation_table_in_mongo_op.alias(
    "update_majors_translation_in_mongo_op"
)


@graph
def sync_majors_translation_table_cfnc():
    element_majors, data_source_used = get_element_majors_op()
    translation_table = create_majors_translation_table_op(element_majors)
    update_majors_translation_in_mongo_op(translation_table, data_source_used)
