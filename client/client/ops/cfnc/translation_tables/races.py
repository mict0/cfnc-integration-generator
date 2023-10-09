from typing import Tuple

from dagster import OpExecutionContext, Out, graph, op
from shared_resources import pretty_print
from translator import update_translation_table_in_mongo_op


@op(out={"data_source_items": Out(), "data_source_used": Out()})
def create_races_translation_table_op(context: OpExecutionContext) -> Tuple[dict, str]:
    translation_table = {
        "Black": "Black or African American",
        # "Other": "",
        "AIAN": "American/Alaska Native",
        "ASIAN": "Asian",
        "White": "White",
        # "Yespanic": "",
    }
    data_source_used = "client.data_source.35527"

    context.log.info(f"Created translation table: {pretty_print(translation_table)}")

    return translation_table, data_source_used


update_races_translation_in_mongo_op = update_translation_table_in_mongo_op.alias(
    "update_races_translation_in_mongo_op"
)


@graph
def sync_races_translation_table_cfnc():
    translation_table, data_source_used = create_races_translation_table_op()
    update_races_translation_in_mongo_op(translation_table, data_source_used)
