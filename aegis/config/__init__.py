"""Configuration module for AEGIS."""

from aegis.config.loader import load_config, get_config_path
from aegis.config.schema import Config

__all__ = ["Config", "load_config", "get_config_path"]
