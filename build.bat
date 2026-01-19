@echo off
REM MSN Weather 桌面小工具打包脚本
REM 使用方法: 双击此文件或命令行中运行 build.bat

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
  echo 错误: 未找到Python，请确保Python已安装并添加到PATH
  pause
  exit /b 1
)

echo 正在检查PyInstaller...
python -c "import pyinstaller" >nul 2>&1
if errorlevel 1 (
  echo 未找到PyInstaller，正在安装...
  pip install pyinstaller
  if errorlevel 1 (
    echo 错误: PyInstaller安装失败
    pause
    exit /b 1
  )
  echo PyInstaller安装成功
)

echo 开始打包MSN Weather桌面小工具...
python build.py

if errorlevel 1 (
  echo 打包失败!
  pause
  exit /b 1
  ) else (
  echo 打包成功完成!
  echo 可执行文件位于: dist\MSN天气.exe
)

pause
