# MSN Weather Desktop Widget

A lightweight desktop weather widget based on Python and PyQt5, featuring system tray display, automatic refresh, startup at boot, and more.

## Features

- 🌤️ **Real-time Weather Display** - Fetches and displays current weather conditions
- 🔄 **Automatic Refresh** - Configurable refresh interval (default: 10 minutes)
- 📍 **Location Settings** - Supports custom latitude and longitude coordinates
- 🖥️ **Transparent Window** - Semi-transparent weather display window that can be freely dragged
- ⏱️ **Startup at Boot** - Supports automatic launch on system startup
- 📌 **Always on Top** - Option to keep the window always on top
- ⚙️ **Simple Settings** - Easily configure all parameters via the settings dialog

## Technology Stack

- **Python 3.x** - Primary development language
- **PyQt5** - GUI framework
- **QSystemTrayIcon** - System tray icon support
- **QThread** - Multithreading to prevent UI freezing
- **Open-Meteo API** - Free weather data API (no API key required)

## Project Structure

```
msn-weather/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── IFLOW.md                   # Project flow documentation
├── assets/
│   └── icon.ico              # Application icon
└── src/
    ├── __init__.py
    ├── autostart.py          # Startup at boot management
    ├── config.py             # Configuration file management
    ├── weather_api.py        # Weather API calls
    ├── weather_thread.py     # Weather data retrieval thread
    ├── weather_refresh_thread.py  # Scheduled refresh thread
    └── ui/
        ├── __init__.py
        ├── settings_dialog.py    # Settings dialog
        └── weather_window.py     # Weather display window
```

## Quick Start

### Prerequisites

- Python 3.7+
- Windows/Linux/macOS operating system

### Install Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `PyQt5` - GUI framework

### Run the Application

```bash
python main.py
```

## Usage Instructions

### Basic Operations

1. **Launch the App** - After launching, a weather icon will appear in the system tray
2. **View Weather** - Drag the semi-transparent window to view current weather
3. **Right-click Menu** - Click the tray icon to open settings or exit the app
4. **Move Window** - Hold and drag the weather window with the left mouse button

### Settings Options

Configure the following parameters in the settings dialog:

| Parameter | Description | Default |
|---------|-------------|---------|
| Latitude | Your location's latitude | 39.9042 (Beijing) |
| Longitude | Your location's longitude | 116.4074 (Beijing) |
| Refresh Interval | Weather refresh cycle (seconds) | 600 |
| Startup at Boot | Automatically run on system startup | Off |
| Always on Top | Keep weather window always on top | Off |

### Configuration File

The application automatically creates a configuration file `weather_config.json` in the user directory with the following content:

```json
{
    "lat": 39.9042,
    "lon": 116.4074,
    "autostart": false,
    "refresh_interval": 600,
    "always_on_top": false,
    "window_x": 100,
    "window_y": 100
}
```

## Development Guide

### Core Module Descriptions

#### src/weather_api.py
- `get_weather(lat, lon)` - Calls the Open-Meteo API to fetch weather data

#### src/weather_thread.py
- `WeatherThread` - Single weather data retrieval thread

#### src/weather_refresh_thread.py
- `WeatherRefreshThread` - Thread for scheduled weather data refresh
- Supports dynamic updates to refresh interval and coordinates

#### src/ui/weather_window.py
- `TransparentWeatherWindow` - Main weather display window
- Supports transparent background, drag-to-move, and always-on-top display

#### src/ui/settings_dialog.py
- `SettingsDialog` - Settings dialog
- Provides an intuitive configuration interface

### Adding New Features

1. Implement the feature in the corresponding module
2. Use `QThread` for background tasks to avoid blocking the UI
3. Update the settings dialog to include new configuration options
4. Add configuration read/write logic in `config.py`

## Notes

- Weather data is sourced from [Open-Meteo API](https://open-meteo.com/), completely free and no API key required
- On first launch, the default location is set to Beijing; adjust to your location as needed
- Window position is automatically saved on exit and restored on next launch
- The startup at boot feature requires administrator privileges on Windows systems

## License

This project is intended solely for learning and personal use.

## Contribution Guide

Issues and Pull Requests are welcome to help improve this project!