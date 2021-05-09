import argparse
from functools import lru_cache
from pathlib import Path
from typing import List

import yaml


@lru_cache(maxsize=None)
def _get_config() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--yaml",
        metavar="PATH/TO/YAML",
        default="config/.recording-config.yml",
        type=str,
        help="Path to YAML file used for configuration. Defaults to config/.recording-config.yml.",
    )
    args = parser.parse_args()

    with open(Path(args.yaml)) as cfg_file:
        config = yaml.safe_load(cfg_file)

    return config


_config = _get_config()

FAUNA_SECRET: str = _config["fauna"]["secret"]
MQTT_USERNAME: str = _config["mqtt"]["username"]
MQTT_PASSWORD: str = _config["mqtt"]["password"]
MQTT_HOST: str = _config["mqtt"]["host"]
MQTT_PORT: int = _config["mqtt"]["port"]

TOPICS: List = _config["topics"]
