"""Pemuatan konfigurasi."""
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(name):
    """load_config('routing') -> configs/routing.yaml"""
    return load_yaml(CONFIG_DIR / f"{name}.yaml")
