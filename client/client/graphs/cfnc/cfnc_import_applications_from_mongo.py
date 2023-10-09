from cfnc.ops.import_to_element import (
    get_cfnc_applications_from_mongo_op,
    import_prepared_applications_op,
    merge_import_parts_op,
    prepare_common_import_parts_op,
    translate_applications_data_op,
)
from cfnc.ops.read_config import read_cfnc_configuration_op
from dagster import graph

from client.ops.cfnc import (
    extract_cfnc_applications_data_op,
    prepare_custom_import_parts_op,
    translate_custom_data_op,
)


@graph
def cfnc_import_applications_from_mongo_graph():
    client_config = read_cfnc_configuration_op()
    cfnc_applications = get_cfnc_applications_from_mongo_op(client_config)
    extract_applications_data = extract_cfnc_applications_data_op(cfnc_applications)
    translated_applications_data = translate_applications_data_op(
        extract_applications_data
    )
    translated_custom_data = translate_custom_data_op(translated_applications_data)
    common_import_parts = prepare_common_import_parts_op(
        translated_custom_data, client_config
    )
    custom_import_parts = prepare_custom_import_parts_op(translated_custom_data)
    prepared_import = merge_import_parts_op(common_import_parts, custom_import_parts)
    import_prepared_applications_op(prepared_import)
