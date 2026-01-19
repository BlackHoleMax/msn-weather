"""Configuration management module."""

import json
import os
from typing import Dict, Any


def get_config_path() -> str:
    """
    Get the configuration file path in user's home directory.

    Returns:
        Absolute path to the configuration file.
    """
    # Use user's home directory (AppData on Windows)
    config_dir = os.path.join(os.path.expanduser("~"), ".msn-weather")

    # Create config directory if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return os.path.join(config_dir, "weather_config.json")


CONFIG_FILE = get_config_path()


def load_config() -> Dict[str, Any]:
    """
    Load configuration from JSON file.

    Returns:
        Dictionary with default config if file doesn't exist or is invalid:
        - lat: Default latitude (Beijing)
        - lon: Default longitude (Beijing)
        - autostart: Whether to start on system boot
        - refresh_interval: Weather data refresh interval in seconds (default: 600)
        - window_x: Window x-coordinate position (default: -1 for screen center)
        - window_y: Window y-coordinate position (default: -1 for screen center)
        - always_on_top: Whether window stays on top of other windows (default: False)
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    config = json.loads(content)
                    # Ensure refresh_interval exists in old configs
                    if "refresh_interval" not in config:
                        config["refresh_interval"] = 600  # Default 10 minutes
                    # Ensure window position fields exist in old configs
                    if "window_x" not in config:
                        config["window_x"] = -1  # Default: screen center
                    if "window_y" not in config:
                        config["window_y"] = -1  # Default: screen center
                    # Ensure always_on_top field exists in old configs
                    if "always_on_top" not in config:
                        config["always_on_top"] = False  # Default: not always on top
                    return config
        except (json.JSONDecodeError, IOError):
            pass

    return {
        "lat": 39.9042,
        "lon": 116.4074,
        "autostart": False,
        "refresh_interval": 600,
        "window_x": -1,
        "window_y": -1,
        "always_on_top": False,
    }


def save_config(
    lat: float,
    lon: float,
    autostart: bool = False,
    refresh_interval: int = 600,
    always_on_top: bool = False,
) -> None:
    """
    Save configuration to JSON file.

    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        autostart: Whether to start on system boot
        refresh_interval: Weather data refresh interval in seconds (default: 600)
        always_on_top: Whether window stays on top of other windows (default: False)
    """
    # Load existing config to preserve window position
    existing_config = load_config()
    config = {
        "lat": lat,
        "lon": lon,
        "autostart": autostart,
        "refresh_interval": refresh_interval,
        "always_on_top": always_on_top,
        "window_x": existing_config.get("window_x", -1),
        "window_y": existing_config.get("window_y", -1),
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)


def save_window_position(x: int, y: int) -> None:
    """
    Save window position to configuration file.

    Args:
        x: Window x-coordinate position
        y: Window y-coordinate position
    """
    # Load existing config to preserve other settings
    config = load_config()
    config["window_x"] = x
    config["window_y"] = y
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)
