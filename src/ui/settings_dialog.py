"""Settings dialog module."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QCheckBox,
    QMessageBox,
)
from PyQt6.QtCore import QThread, pyqtSignal
from src.geocoder import geocode_location


class GeocodeThread(QThread):
    """Thread for geocoding operations to prevent UI freezing."""

    geocode_complete = pyqtSignal(float, float)
    geocode_failed = pyqtSignal(str)

    def __init__(self, location_name: str):
        super().__init__()
        self.location_name = location_name

    def run(self):
        """Run the geocoding operation."""
        result = geocode_location(self.location_name)
        if result:
            lat, lon = result
            self.geocode_complete.emit(lat, lon)
        else:
            self.geocode_failed.emit(self.location_name)


class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""

    def __init__(
        self,
        parent=None,
        lat: float = 39.9042,
        lon: float = 116.4074,
        autostart: bool = False,
        refresh_interval: int = 600,
        always_on_top: bool = False,
    ):
        """
        Initialize the settings dialog.

        Args:
            parent: Parent widget
            lat: Current latitude
            lon: Current longitude
            autostart: Current autostart status
            refresh_interval: Current refresh interval in seconds
            always_on_top: Whether window stays on top of other windows
        """
        super().__init__(parent)
        self.lat = lat
        self.lon = lon
        self.autostart = autostart
        self.refresh_interval = refresh_interval
        self.always_on_top = always_on_top
        self.geocode_thread = None
        self.initUI()

    def initUI(self) -> None:
        """Initialize the dialog UI."""
        self.setWindowTitle("设置")
        self.setFixedSize(300, 400)  # Increased height for location search

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Location search
        location_layout = QHBoxLayout()
        location_label = QLabel("地区:")
        location_label.setStyleSheet("color: white; font-size: 14px; min-height: 30px;")
        location_layout.addWidget(location_label)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText(
            "输入地区名称，如：北京、上海市、广州天河区"
        )
        self.location_input.setMinimumHeight(30)
        self.location_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                border: 1px solid rgba(255, 255, 255, 100);
                padding: 8px;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 100);
            }
        """)
        location_layout.addWidget(self.location_input)

        self.search_btn = QPushButton("搜索")
        self.search_btn.setMinimumHeight(30)
        self.search_btn.setFixedWidth(60)
        self.search_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 120, 215, 200);
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 215, 255);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 150);
                color: rgba(255, 255, 255, 100);
            }
        """)
        self.search_btn.clicked.connect(self.search_location)
        location_layout.addWidget(self.search_btn)

        layout.addLayout(location_layout)

        # Latitude input
        lat_layout = QHBoxLayout()
        lat_label = QLabel("纬度:")
        lat_label.setStyleSheet("color: white; font-size: 14px; min-height: 30px;")
        lat_layout.addWidget(lat_label)
        self.lat_input = QLineEdit(str(self.lat))
        self.lat_input.setMinimumHeight(30)
        self.lat_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                border: 1px solid rgba(255, 255, 255, 100);
                padding: 8px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        lat_layout.addWidget(self.lat_input)
        layout.addLayout(lat_layout)

        # Longitude input
        lon_layout = QHBoxLayout()
        lon_label = QLabel("经度:")
        lon_label.setStyleSheet("color: white; font-size: 14px; min-height: 30px;")
        lon_layout.addWidget(lon_label)
        self.lon_input = QLineEdit(str(self.lon))
        self.lon_input.setMinimumHeight(30)
        self.lon_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                border: 1px solid rgba(255, 255, 255, 100);
                padding: 8px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        lon_layout.addWidget(self.lon_input)
        layout.addLayout(lon_layout)

        # Refresh interval input
        refresh_layout = QHBoxLayout()
        refresh_label = QLabel("刷新间隔(分钟):")
        refresh_label.setStyleSheet("color: white; font-size: 14px; min-height: 30px;")
        refresh_layout.addWidget(refresh_label)
        self.refresh_input = QLineEdit(
            str(self.refresh_interval // 60)
        )  # Convert seconds to minutes
        self.refresh_input.setMinimumHeight(30)
        self.refresh_input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                border: 1px solid rgba(255, 255, 255, 100);
                padding: 8px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        refresh_layout.addWidget(self.refresh_input)
        layout.addLayout(refresh_layout)

        # Autostart checkbox
        self.autostart_checkbox = QCheckBox("开机自启")
        self.autostart_checkbox.setChecked(self.autostart)
        self.autostart_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 4px;
                background-color: rgba(0, 0, 0, 150);
            }
            QCheckBox::indicator:checked {
                background-color: rgba(0, 120, 215, 200);
                border-color: rgba(0, 120, 215, 255);
            }
        """)
        layout.addWidget(self.autostart_checkbox)

        # Always on top checkbox
        self.always_on_top_checkbox = QCheckBox("窗口置顶")
        self.always_on_top_checkbox.setChecked(self.always_on_top)
        self.always_on_top_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 4px;
                background-color: rgba(0, 0, 0, 150);
            }
            QCheckBox::indicator:checked {
                background-color: rgba(0, 120, 215, 200);
                border-color: rgba(0, 120, 215, 255);
            }
        """)
        layout.addWidget(self.always_on_top_checkbox)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.save_btn.setMinimumHeight(35)
        self.save_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 120, 215, 200);
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 215, 255);
            }
        """)
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setMinimumHeight(35)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(100, 100, 100, 200);
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(100, 100, 100, 255);
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def search_location(self) -> None:
        """Search for location coordinates."""
        location_name = self.location_input.text().strip()
        if not location_name:
            QMessageBox.warning(self, "提示", "请输入地区名称")
            return

        # Disable search button while searching
        self.search_btn.setEnabled(False)
        self.search_btn.setText("搜索中...")

        # Create and start geocoding thread
        self.geocode_thread = GeocodeThread(location_name)
        self.geocode_thread.geocode_complete.connect(self.on_geocode_complete)
        self.geocode_thread.geocode_failed.connect(self.on_geocode_failed)
        self.geocode_thread.finished.connect(self.on_geocode_finished)
        self.geocode_thread.start()

    def on_geocode_complete(self, lat: float, lon: float) -> None:
        """Handle successful geocoding result."""
        self.lat_input.setText(str(lat))
        self.lon_input.setText(str(lon))

    def on_geocode_failed(self, location_name: str) -> None:
        """Handle failed geocoding."""
        QMessageBox.warning(
            self,
            "搜索失败",
            f"无法找到地区 '{location_name}' 的坐标。\n请检查地区名称是否正确，或尝试更具体的名称。",
        )

    def on_geocode_finished(self) -> None:
        """Clean up after geocoding thread finishes."""
        self.search_btn.setEnabled(True)
        self.search_btn.setText("搜索")
        self.geocode_thread = None

    def save_settings(self) -> None:
        """Validate and save settings."""
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            refresh_minutes = int(self.refresh_input.text())

            # Validate refresh interval (1-120 minutes)
            if refresh_minutes < 1:
                refresh_minutes = 1
            elif refresh_minutes > 120:
                refresh_minutes = 120

            self.lat = lat
            self.lon = lon
            self.refresh_interval = refresh_minutes * 60  # Convert minutes to seconds
            self.autostart = self.autostart_checkbox.isChecked()
            self.always_on_top = self.always_on_top_checkbox.isChecked()
            self.accept()
        except ValueError:
            pass

    def get_settings(self) -> tuple:
        """
        Get the current settings.

        Returns:
            Tuple of (lat, lon, autostart, refresh_interval, always_on_top)
        """
        return (
            self.lat,
            self.lon,
            self.autostart,
            self.refresh_interval,
            self.always_on_top,
        )
