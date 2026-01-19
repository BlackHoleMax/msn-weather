"""Weather data refresh thread module with timer support."""

from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from src.weather_api import get_weather


class WeatherRefreshThread(QThread):
    """Background thread for fetching weather data with timer-based refresh."""

    weather_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, lat: float, lon: float, refresh_interval: int = 600):
        """
        Initialize the weather refresh thread.

        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            refresh_interval: Refresh interval in seconds (default: 600)
        """
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.refresh_interval = refresh_interval
        self.running = False

    def run(self) -> None:
        """Start the timer-based weather fetching."""
        self.running = True

        # Create timer in the worker thread
        self.timer = QTimer()
        self.timer.timeout.connect(self._fetch_and_schedule)

        # Start the fetch and schedule cycle
        self._fetch_and_schedule()

    def _fetch_and_schedule(self) -> None:
        """Fetch weather data and schedule next fetch."""
        if not self.running:
            return

        try:
            weather_data = get_weather(self.lat, self.lon)
            self.weather_loaded.emit(weather_data)
        except Exception as e:
            self.error_occurred.emit(str(e))

        # Schedule next fetch if still running
        if self.running:
            self.timer.singleShot(
                self.refresh_interval * 1000, self._fetch_and_schedule
            )

    def stop(self) -> None:
        """Stop the timer and thread."""
        self.running = False
        self.quit()
        self.wait()

    def fetch_weather(self) -> None:
        """Fetch weather data immediately (can be called from main thread)."""
        # Schedule immediate fetch in worker thread
        if self.isRunning():
            QTimer.singleShot(0, self._fetch_and_schedule)

    def update_coordinates(self, lat: float, lon: float) -> None:
        """
        Update coordinates and continue fetching.

        Args:
            lat: New latitude
            lon: New longitude
        """
        self.lat = lat
        self.lon = lon

    def update_refresh_interval(self, refresh_interval: int) -> None:
        """
        Update refresh interval.

        Args:
            refresh_interval: New refresh interval in seconds
        """
        self.refresh_interval = refresh_interval
        # No need to restart timer, next schedule will use new interval
