"""Settings dialog module."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QCheckBox,
)
from PyQt6.QtCore import Qt


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
        self.initUI()

    def initUI(self) -> None:
        """Initialize the dialog UI."""
        self.setWindowTitle("设置")
        self.setFixedSize(300, 350)  # Increased height for new checkbox

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

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
        self.refresh_input = QLineEdit(str(self.refresh_interval // 60))  # Convert seconds to minutes
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
        return self.lat, self.lon, self.autostart, self.refresh_interval, self.always_on_top
