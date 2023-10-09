from typing import Tuple

from dagster import OpExecutionContext, Out, graph, op
from shared_resources import pretty_print
from translator import update_translation_table_in_mongo_op


@op(out={"data_source_items": Out(), "data_source_used": Out()})
def create_genders_translation_table_op(context: OpExecutionContext) -> Tuple[dict, str]:
    translation_table = {
        "Female": "f",
        "Male": "m",
    }
    data_source_used = "data_source.gender"

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table, data_source_used


update_genders_translation_in_mongo_op = update_translation_table_in_mongo_op.alias(
    "update_genders_translation_in_mongo_op"
)


@graph
def sync_genders_translation_table_cfnc():
    translation_table, data_source_used = create_genders_translation_table_op()
    update_genders_translation_in_mongo_op(translation_table, data_source_used)
