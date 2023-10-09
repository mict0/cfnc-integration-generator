secret_name = {"secret_name": "dagster/client/stage"}
region_name = {"region_name": "us-east-1"}


def get_secrets_config():
    return {**secret_name, **region_name}


def get_region():
    return region_name
