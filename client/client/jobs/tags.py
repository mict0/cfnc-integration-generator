from dagster import MAX_RUNTIME_SECONDS_TAG

subdom = "client"
max_runtime_seconds_tag_value = 600

ethos_tags = {
    "subdom": subdom,
    "integration": "ethos",
    MAX_RUNTIME_SECONDS_TAG: max_runtime_seconds_tag_value,
}
cfnc_tags = {
    "subdom": subdom,
    "integration": "cfnc",
    MAX_RUNTIME_SECONDS_TAG: max_runtime_seconds_tag_value,
}
