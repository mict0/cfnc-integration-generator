from dagster import OpExecutionContext, graph, op
from shared_resources import pretty_print
from translator import (
    get_element_regular_data_source_from_mongo_op,
    update_translation_table_in_mongo_op,
)


@op
def create_educational_level_translation_table_op(
    context: OpExecutionContext, educational_level: list
) -> dict:
    translation_table = {
        level["column_1"]: level["column_2"] for level in educational_level
    }

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table


get_element_educational_level_op = get_element_regular_data_source_from_mongo_op.alias(
    "get_element_educational_level_op"
)
update_educational_level_translation_in_mongo_op = (
    update_translation_table_in_mongo_op.alias(
        "update_educational_level_translation_in_mongo_op"
    )
)


@graph
def sync_educational_level_translation_table_cfnc():
    element_educational_level, data_source_used = get_element_educational_level_op()
    translation_table = create_educational_level_translation_table_op(
        element_educational_level
    )
    update_educational_level_translation_in_mongo_op(translation_table, data_source_used)
