#!/usr/bin/env python3
"""
PyInstaller 打包脚本 for MSN Weather 桌面小工具

使用方法:
    python build.py
"""

import os
import sys
import subprocess
import shutil


def main():
    """主打包函数"""
    # 项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))

    # 图标路径
    icon_path = os.path.join(project_root, "assets", "icon.ico")
    if not os.path.exists(icon_path):
        print(f"错误: 图标文件不存在: {icon_path}")
        sys.exit(1)

    # UPX 路径 (用户提供的路径，去掉 @ 符号)
    upx_dir = r"D:\upx-5.0.1-win64"
    if not os.path.exists(upx_dir):
        print(f"警告: UPX 目录不存在: {upx_dir}")
        print("打包将继续进行，但不使用 UPX 压缩")
        upx_dir = None

    # PyInstaller 参数
    args = [
        "pyinstaller",
        "--noconsole",  # 无命令行窗口
        "--onefile",  # 打包成单个可执行文件
        f"--icon={icon_path}",  # 设置图标
        "--name=MSN天气",  # 可执行文件名称
        "--clean",  # 清理临时文件
        f"--paths={os.path.join(project_root, 'src')}",  # 添加src目录到模块搜索路径
    ]

    # 添加 UPX 目录（如果存在）
    if upx_dir:
        args.append(f"--upx-dir={upx_dir}")

    # 添加隐藏导入（如果需要）
    hidden_imports = [
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "xmltodict",
        "requests",
        "urllib3",
        "chardet",
        "idna",
    ]

    for imp in hidden_imports:
        args.append(f"--hidden-import={imp}")

    # 添加数据文件（如果需要）
    # 例如：args.append("--add-data=assets;assets")

    # 添加主程序文件
    main_script = os.path.join(project_root, "main.py")
    args.append(main_script)

    print("开始打包 MSN Weather 桌面小工具...")
    print(f"项目根目录: {project_root}")
    print(f"图标文件: {icon_path}")
    print(f"UPX 目录: {upx_dir if upx_dir else '未使用'}")
    print(f"PyInstaller 命令: {' '.join(args)}")
    print("-" * 50)

    try:
        # 运行 PyInstaller
        subprocess.run(args, check=True, capture_output=True, text=True)
        print("打包成功完成!")
        print("输出文件位置:")
        print(f"  - 可执行文件: {os.path.join(project_root, 'dist', 'MSN天气.exe')}")
        print(f"  - 构建目录: {os.path.join(project_root, 'build')}")

        # 复制配置文件示例（如果需要）
        config_src = os.path.join(project_root, "weather_config.json")
        if os.path.exists(config_src):
            config_dst = os.path.join(project_root, "dist", "weather_config.json")
            shutil.copy2(config_src, config_dst)
            print(f"  - 配置文件已复制: {config_dst}")

    except subprocess.CalledProcessError as e:
        print(f"打包失败! 错误代码: {e.returncode}")
        print(f"标准输出:\n{e.stdout}")
        print(f"标准错误:\n{e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 未找到 PyInstaller，请先安装: pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    main()
