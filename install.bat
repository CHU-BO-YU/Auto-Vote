@echo off
chcp 65001 >nul
title 自動安裝 Python 環境套件

echo ==========================================
echo       正在準備安裝 Python 套件...
echo ==========================================
echo.

:: 檢查是否有安裝 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python！請確認您已安裝 Python 並且有勾選 "Add Python to PATH"。
    pause
    exit /b
)

:: 檢查 pip 是否可用
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 pip！請確認 Python 安裝完整。
    pause
    exit /b
)

echo [1/2] 正在升級 pip (如果需要)...
python -m pip install --upgrade pip

echo.
echo [2/2] 正在安裝 requirements.txt 中的套件...
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo.
        echo ==========================================
        echo           ✅ 所有套件安裝成功！
        echo ==========================================
    ) else (
        echo.
        echo [錯誤] 安裝過程中發生錯誤，請檢查網路連線或錯誤訊息。
    )
) else (
    echo.
    echo [錯誤] 找不到 requirements.txt 檔案！
    echo 請確保此 bat 檔與 requirements.txt 在同一個資料夾內。
)

echo.
echo 按任意鍵關閉視窗...
pause >nul