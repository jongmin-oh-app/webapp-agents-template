from functools import lru_cache
from pathlib import Path

import boto3
import yaml

_config_path = Path(__file__).resolve().parents[1] / "config.yml"
_ssm = boto3.client("ssm")


def _load_yaml() -> dict:
    with open(_config_path) as f:
        return yaml.safe_load(f)


def _get_param(name: str) -> str:
    resp = _ssm.get_parameter(Name=name, WithDecryption=True)
    return resp["Parameter"]["Value"]


@lru_cache
def get_config() -> dict:
    cfg = _load_yaml()
    return {
        key: _get_param(path)
        for key, path in cfg["params"].items()
    }
