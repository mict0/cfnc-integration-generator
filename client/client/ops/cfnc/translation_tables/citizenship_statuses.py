from typing import List

from dagster import OpExecutionContext, graph, op
from shared_resources import pretty_print
from translator import (
    get_element_system_data_source_from_mongo_op,
    update_translation_table_in_mongo_op,
)


@op
def create_citizenship_statuses_translation_table_op(
    context: OpExecutionContext, citizenship_statuses: List[dict]
) -> dict:
    translation_table = {
        status["short"]: status["name"] for status in citizenship_statuses
    }

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table


get_element_citizenship_statuses_op = get_element_system_data_source_from_mongo_op.alias(
    "get_element_citizenship_statuses_op"
)
update_citizenship_statuses_translation_in_mongo_op = (
    update_translation_table_in_mongo_op.alias(
        "update_citizenship_statuses_translation_in_mongo_op"
    )
)


@graph
def sync_citizenship_statuses_translation_table_cfnc():
    element_citizenship_statuses, data_source_used = get_element_citizenship_statuses_op()
    translation_table = create_citizenship_statuses_translation_table_op(
        element_citizenship_statuses
    )
    update_citizenship_statuses_translation_in_mongo_op(
        translation_table, data_source_used
    )
