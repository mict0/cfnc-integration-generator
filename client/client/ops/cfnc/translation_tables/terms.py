from dagster import OpExecutionContext, graph, op
from shared_resources import pretty_print
from translator import (
    get_element_main_data_source_op,
    update_translation_table_in_mongo_op,
)


@op
def create_terms_translation_table_op(
    context: OpExecutionContext, element_terms: list
) -> dict:
    translation_table = {term["guid"]: term["code"] for term in element_terms}

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table


get_element_terms_op = get_element_main_data_source_op.alias("get_element_terms_op")
update_terms_translation_in_mongo_op = update_translation_table_in_mongo_op.alias(
    "update_terms_translation_in_mongo_op"
)


@graph
def sync_terms_translation_table_cfnc():
    element_terms, data_source_used = get_element_terms_op()
    translation_table = create_terms_translation_table_op(element_terms)
    update_terms_translation_in_mongo_op(translation_table, data_source_used)
