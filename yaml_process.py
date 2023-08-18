import yaml


def read_data():
    with open("data.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def read_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def write_data(data):
    with open("data.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def write_config(config):
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f)
