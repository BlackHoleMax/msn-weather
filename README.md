

# MSN 天气桌面小工具

一个基于 Python 和 PyQt5 的轻量级桌面天气小工具，支持系统托盘显示、自动刷新、开机自启动等功能。

## 功能特性

- 🌤️ **实时天气显示** - 获取并展示当前天气状况
- 🔄 **自动刷新** - 可配置刷新间隔（默认 10 分钟）
- 📍 **位置设置** - 支持自定义经纬度坐标
- 🖥️ **透明窗口** - 半透明天气显示窗口，可自由拖动
- ⏱️ **开机自启** - 支持开机自动运行
- 📌 **置顶显示** - 可选择窗口始终置顶
- ⚙️ **简洁设置** - 通过设置对话框轻松配置各项参数

## 技术栈

- **Python 3.x** - 主要开发语言
- **PyQt5** - GUI 图形界面框架
- **QSystemTrayIcon** - 系统托盘图标支持
- **QThread** - 多线程处理，避免界面卡顿
- **Open-Meteo API** - 免费天气数据接口（无需 API Key）

## 项目结构

```
msn-weather/
├── main.py                    # 程序入口
├── requirements.txt           # Python 依赖
├── IFLOW.md                   # 项目流程文档
├── assets/
│   └── icon.ico              # 程序图标
└── src/
    ├── __init__.py
    ├── autostart.py          # 开机自启动管理
    ├── config.py             # 配置文件管理
    ├── weather_api.py        # 天气 API 调用
    ├── weather_thread.py     # 天气数据获取线程
    ├── weather_refresh_thread.py  # 定时刷新线程
    └── ui/
        ├── __init__.py
        ├── settings_dialog.py    # 设置对话框
        └── weather_window.py     # 天气显示窗口
```

## 快速开始

### 环境要求

- Python 3.7+
- Windows/Linux/macOS 操作系统

### 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `PyQt5` - GUI 框架

### 运行应用

```bash
python main.py
```

## 使用说明

### 基本操作

1. **启动程序** - 运行后将在系统托盘显示天气图标
2. **查看天气** - 拖动半透明窗口查看当前天气
3. **右键菜单** - 点击托盘图标可打开设置或退出程序
4. **移动窗口** - 按住鼠标左键拖动天气窗口

### 设置选项

在设置对话框中可以配置以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 纬度 | 所在地区纬度 | 39.9042 (北京) |
| 经度 | 所在地区经度 | 116.4074 (北京) |
| 刷新间隔 | 天气刷新周期（秒） | 600 |
| 开机自启 | 系统启动时自动运行 | 关闭 |
| 窗口置顶 | 天气窗口始终置顶显示 | 关闭 |

### 配置文件

程序会自动在用户目录下创建配置文件 `weather_config.json`，包含以下内容：

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

## 开发指南

### 核心模块说明

#### src/weather_api.py
- `get_weather(lat, lon)` - 调用 Open-Meteo API 获取天气数据

#### src/weather_thread.py
- `WeatherThread` - 单次天气数据获取线程

#### src/weather_refresh_thread.py
- `WeatherRefreshThread` - 定时刷新天气数据的线程
- 支持动态更新刷新间隔和坐标

#### src/ui/weather_window.py
- `TransparentWeatherWindow` - 天气显示主窗口
- 支持透明背景、拖拽移动、置顶显示

#### src/ui/settings_dialog.py
- `SettingsDialog` - 设置对话框
- 提供直观的配置界面

### 添加新功能

1. 在对应模块中实现功能
2. 如需后台处理，使用 `QThread` 避免阻塞 UI
3. 更新设置对话框添加配置选项
4. 在 `config.py` 中添加配置读写逻辑

## 注意事项

- 天气数据来源于 [Open-Meteo API](https://open-meteo.com/)，完全免费无需 API Key
- 首次运行会使用北京坐标，可根据所在位置自行调整
- 窗口位置关闭时会自动保存，下次启动恢复
- 开机自启功能在 Windows 系统上需要管理员权限设置

## 许可证

本项目仅供学习和个人使用。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！