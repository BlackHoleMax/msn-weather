"""Windows autostart management module."""

import sys
import os
import winreg


def set_autostart(enable: bool) -> None:
    """
    Enable or disable application autostart on Windows boot.

    Args:
        enable: True to enable autostart, False to disable
    """
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "MSN天气"

    if getattr(sys, "frozen", False):
        # Running as compiled executable
        app_path = sys.executable
        command = f'"{app_path}"'
    else:
        # Running as script
        app_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "main.py")
        )
        python_exe = sys.executable
        command = f'"{python_exe}" "{app_path}"'

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
        ) as key:
            if enable:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, command)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass
    except Exception as e:
        print(f"设置开机自启失败: {e}")
