"""Weather data fetching thread module."""

from PyQt6.QtCore import QThread, pyqtSignal
from src.weather_api import get_weather


class WeatherThread(QThread):
    """Background thread for fetching weather data."""

    weather_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, lat: float, lon: float):
        """
        Initialize the weather thread.

        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
        """
        super().__init__()
        self.lat = lat
        self.lon = lon

    def run(self) -> None:
        """Fetch weather data and emit signals."""
        try:
            weather_data = get_weather(self.lat, self.lon)
            self.weather_loaded.emit(weather_data)
        except Exception as e:
            self.error_occurred.emit(str(e))
