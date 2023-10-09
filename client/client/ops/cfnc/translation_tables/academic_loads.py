from typing import List

from dagster import OpExecutionContext, graph, op
from shared_resources import pretty_print
from translator import (
    get_element_system_data_source_from_mongo_op,
    update_translation_table_in_mongo_op,
)


@op
def create_academic_loads_translation_table_op(
    context: OpExecutionContext, academic_loads: List[dict]
) -> dict:
    translation_table = {
        academic_load["value"]: academic_load["text"].capitalize()
        for academic_load in academic_loads
    }

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table


get_element_academic_loads_op = get_element_system_data_source_from_mongo_op.alias(
    "get_element_academic_loads_op"
)
update_academic_loads_translation_in_mongo_op = (
    update_translation_table_in_mongo_op.alias(
        "update_academic_loads_translation_in_mongo_op"
    )
)


@graph
def sync_academic_loads_translation_table_cfnc():
    element_academic_loads, data_source_used = get_element_academic_loads_op()
    translation_table = create_academic_loads_translation_table_op(element_academic_loads)
    update_academic_loads_translation_in_mongo_op(translation_table, data_source_used)
