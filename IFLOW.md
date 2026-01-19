# MSN 天气桌面小工具

## 项目概述

这是一个基于 PyQt6 开发的 Windows 桌面天气小工具，使用 MSN Weather API 获取实时天气信息。应用以透明悬浮窗口的形式显示天气，支持系统托盘图标、开机自启、位置设置等功能。

### 主要技术栈

- **Python 3.13+**
- **PyQt6** - GUI 框架
- **xmltodict** - XML 解析
- **Windows 注册表操作** - 开机自启功能

### 核心功能

- 实时天气显示（位置、温度、天气状况、天气图标）
- 透明悬浮窗口，可拖拽移动
- 系统托盘图标集成
- 位置设置（经纬度配置）
- 开机自启选项
- 配置持久化（JSON 文件）

## 构建和运行

### 依赖安装

```bash
pip install PyQt6 xmltodict
```

### 运行应用

```bash
python main.py
```

### 配置文件

配置文件自动生成在应用目录下：`weather_config.json`

默认配置（北京）：
```json
{
  "lat": 39.9042,
  "lon": 116.4074,
  "autostart": false
}
```

## 开发规范

### 项目结构

```
msn-weather/
├── main.py                    # 主程序文件
├── weather_config.json        # 配置文件（运行时生成）
└── IFLOW.md                   # 项目说明文档
```

### 核心类说明

- **`WeatherThread`** - 异步获取天气数据的线程类
- **`SettingsDialog`** - 设置对话框，用于配置经纬度和开机自启
- **`TransparentWeatherWindow`** - 主窗口类，透明悬浮窗，显示天气信息

### 关键函数

- **`getWeather(lat, lon)`** - 从 MSN Weather API 获取天气数据
- **`load_config()`** - 加载配置文件
- **`save_config(lat, lon, autostart)`** - 保存配置文件
- **`set_autostart(enable)`** - 设置/取消 Windows 开机自启

### API 说明

使用 MSN Weather LiveTile API：
- 端点：`http://api.msn.com/weather/LiveTile/front`
- 参数：`locale`, `lat`, `lon`, `apiKey`
- 返回：XML 格式的天气数据，解析为字典

### 样式约定

- 使用 PyQt6 样式表（QSS）进行界面美化
- 主题色：半透明深色背景 (`rgba(30, 30, 30, 240)`)
- 强调色：蓝色 (`rgba(0, 120, 215, 200)`)
- 所有文本使用白色，背景半透明

### 系统要求

- Windows 操作系统（依赖 Windows 注册表 API）
- Python 3.13+
- PyQt6

### 注意事项

- 应用使用 MSN Weather API，需要网络连接
- 开机自启功能仅在 Windows 上可用
- 窗口默认固定大小为 280x160 像素