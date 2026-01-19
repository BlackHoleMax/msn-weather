"""Main weather window module."""

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QScreen
from urllib.request import urlopen
from src.weather_refresh_thread import WeatherRefreshThread
from src.config import load_config, save_window_position


class TransparentWeatherWindow(QWidget):
    """Transparent floating window displaying weather information."""

    def __init__(self, tray_icon):
        """
        Initialize the weather window.

        Args:
            tray_icon: System tray icon instance
        """
        super().__init__()
        self.tray_icon = tray_icon
        config = load_config()
        self.lat = config['lat']
        self.lon = config['lon']
        self.refresh_interval = config.get('refresh_interval', 600)
        self.window_x = config.get('window_x', -1)
        self.window_y = config.get('window_y', -1)
        self.always_on_top = config.get('always_on_top', False)
        self.initUI()
        # Apply always on top setting
        self.set_always_on_top(self.always_on_top)
        self.load_weather()
        self.set_initial_position()
        
        # Timer for delayed position saving
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_current_position)
        self.save_delay = 1000  # 1 second delay

    def set_initial_position(self) -> None:
        """Set the initial window position based on saved configuration."""
        if self.window_x == -1 or self.window_y == -1:
            # Center the window on screen
            screen = QApplication.primaryScreen()
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
        else:
            # Use saved position
            self.move(self.window_x, self.window_y)
        
        # Ensure window is within screen bounds
        self.ensure_within_screen()

    def save_current_position(self) -> None:
        """Save current window position to configuration file."""
        x, y = self.x(), self.y()
        try:
            save_window_position(x, y)
        except Exception as e:
            # Log error but don't crash
            print(f"Failed to save window position: {e}")

    def ensure_within_screen(self) -> None:
        """Ensure window is within screen bounds."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        x, y = self.x(), self.y()
        width, height = self.width(), self.height()
        
        # Adjust if window is partially or completely outside screen
        if x < screen_geometry.left():
            x = screen_geometry.left()
        elif x + width > screen_geometry.right():
            x = screen_geometry.right() - width
            
        if y < screen_geometry.top():
            y = screen_geometry.top()
        elif y + height > screen_geometry.bottom():
            y = screen_geometry.bottom() - height
        
        if x != self.x() or y != self.y():
            self.move(x, y)

    def initUI(self) -> None:
        """Initialize the window UI."""
        self.setWindowTitle('MSN 天气')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(280, 160)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Location label
        self.location_label = QLabel('加载中...')
        self.location_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.location_label)

        # Weather info layout
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)

        # Weather icon
        self.weather_icon = QLabel()
        self.weather_icon.setFixedSize(70, 70)
        self.weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.weather_icon)

        # Weather details
        weather_info_layout = QVBoxLayout()
        weather_info_layout.setSpacing(5)

        self.temp_label = QLabel('--℃')
        self.temp_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        weather_info_layout.addWidget(self.temp_label)

        self.weather_label = QLabel('--')
        self.weather_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background-color: transparent;
            }
        """)
        weather_info_layout.addWidget(self.weather_label)

        info_layout.addLayout(weather_info_layout)
        layout.addLayout(info_layout)

        self.setLayout(layout)

    def load_weather(self) -> None:
        """Start background thread to fetch weather data with timer."""
        # Stop existing thread if running
        if hasattr(self, 'weather_thread') and self.weather_thread:
            self.weather_thread.stop()
            self.weather_thread.wait()
            
        self.weather_thread = WeatherRefreshThread(self.lat, self.lon, self.refresh_interval)
        self.weather_thread.weather_loaded.connect(self.update_display)
        self.weather_thread.error_occurred.connect(self.show_error)
        self.weather_thread.start()

    def update_coordinates(self, lat: float, lon: float) -> None:
        """
        Update coordinates and refresh weather data.

        Args:
            lat: New latitude
            lon: New longitude
        """
        self.lat = lat
        self.lon = lon
        if hasattr(self, 'weather_thread') and self.weather_thread:
            self.weather_thread.update_coordinates(lat, lon)
            # Trigger immediate refresh
            self.weather_thread.fetch_weather()

    def update_display(self, data: dict) -> None:
        """
        Update the display with weather data.

        Args:
            data: Weather data dictionary
        """
        self.location_label.setText(data['Location'])
        self.temp_label.setText(data['Temperature'])
        self.weather_label.setText(data['Weather'])

        try:
            response = urlopen(data['ImageURL'])
            image_data = response.read()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            scaled_pixmap = pixmap.scaled(
                70, 70, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.weather_icon.setPixmap(scaled_pixmap)
        except Exception:
            pass

    def show_error(self, error_msg: str) -> None:
        """
        Display error message.

        Args:
            error_msg: Error message to display
        """
        self.location_label.setText('加载失败')
        self.temp_label.setText('--℃')
        self.weather_label.setText(error_msg)

    def mousePressEvent(self, event) -> None:
        """Handle mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release after dragging to save window position."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Save window position after dragging
            self.save_current_position()
        super().mouseReleaseEvent(event)

    def moveEvent(self, event) -> None:
        """Handle window move events to save position with delay."""
        super().moveEvent(event)
        # Restart timer to save position after delay
        self.save_timer.stop()
        self.save_timer.start(self.save_delay)

    def set_always_on_top(self, always_on_top: bool) -> None:
        """
        Set window always on top state.

        Args:
            always_on_top: Whether window should stay on top of other windows
        """
        self.always_on_top = always_on_top
        
        # Get current window flags
        current_flags = self.windowFlags()
        
        if always_on_top:
            # Add WindowStaysOnTopHint flag
            new_flags = current_flags | Qt.WindowType.WindowStaysOnTopHint
        else:
            # Remove WindowStaysOnTopHint flag
            new_flags = current_flags & ~Qt.WindowType.WindowStaysOnTopHint
        
        # Save current window geometry and visibility
        was_visible = self.isVisible()
        window_geometry = self.geometry()
        
        # Apply new window flags
        self.setWindowFlags(new_flags)
        
        # Restore window attributes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Restore window geometry
        self.setGeometry(window_geometry)
        
        # Show window again to apply changes (required after changing window flags)
        if was_visible:
            self.show()
            self.raise_()
            self.activateWindow()
        else:
            # If window was hidden, keep it hidden
            pass

    def update_refresh_interval(self, refresh_interval: int) -> None:
        """
        Update refresh interval and restart weather thread.

        Args:
            refresh_interval: New refresh interval in seconds
        """
        self.refresh_interval = refresh_interval
        if hasattr(self, 'weather_thread') and self.weather_thread:
            self.weather_thread.update_refresh_interval(refresh_interval)

    def closeEvent(self, event) -> None:
        """Handle close event - hide instead of close."""
        # Stop weather thread before closing
        if hasattr(self, 'weather_thread') and self.weather_thread:
            self.weather_thread.stop()
            self.weather_thread.wait()
        event.ignore()
        self.hide()