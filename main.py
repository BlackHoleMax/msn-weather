"""MSN Weather Desktop Application - Main Entry Point."""

import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QDialog
from PyQt6.QtGui import QAction
from src.ui import SettingsDialog, TransparentWeatherWindow
from src.config import load_config, save_config
from src.autostart import set_autostart


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create system tray icon
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(
        app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon)  # type: ignore
    )
    tray_icon.setToolTip("MSN 天气")

    # Create tray menu actions
    show_action = QAction("显示窗口", None)
    settings_action = QAction("设置", None)
    quit_action = QAction("退出", None)

    # Create main window
    window = TransparentWeatherWindow(tray_icon)

    def show_window():
        """Show and activate the main window."""
        window.show()
        window.raise_()
        window.activateWindow()

    def open_settings():
        """Open settings dialog."""
        config = load_config()
        dialog = SettingsDialog(
            window,
            config["lat"],
            config["lon"],
            config.get("autostart", False),
            config.get("refresh_interval", 600),
            config.get("always_on_top", False),
        )
        dialog.setStyleSheet("""
            QDialog {
                background-color: rgba(30, 30, 30, 240);
                color: white;
            }
        """)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            lat, lon, autostart, refresh_interval, always_on_top = dialog.get_settings()
            save_config(lat, lon, autostart, refresh_interval, always_on_top)
            set_autostart(autostart)
            window.update_coordinates(lat, lon)
            window.update_refresh_interval(refresh_interval)
            window.set_always_on_top(always_on_top)

    def quit_app():
        """Quit the application."""
        tray_icon.hide()
        app.quit()

    # Connect actions
    show_action.triggered.connect(show_window)
    settings_action.triggered.connect(open_settings)
    quit_action.triggered.connect(quit_app)

    # Create tray menu
    tray_menu = QMenu()
    tray_menu.addAction(show_action)
    tray_menu.addAction(settings_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Show main window
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
