@echo off
:: 設定編碼為 UTF-8，避免中文亂碼
chcp 65001 >nul
title 自動投票機器人 - 執行中

:: 切換到此 bat 檔所在的目錄 (關鍵步驟，避免讀不到 .env 或 csv)
cd /d "%~dp0"

echo ======================================================
echo           🚀 正在啟動自動投票機器人...
echo ======================================================
echo.

:: 檢查 main.py 是否存在
if not exist main.py (
    echo [錯誤] 找不到 main.py！
    echo 請確認你的 Python 程式碼檔名是否為 main.py
    echo.
    pause
    exit /b
)

:: 執行 Python 程式
python main.py

echo.
echo ======================================================
echo           🏁 程式執行結束
echo ======================================================
echo.
echo 按任意鍵關閉視窗...
pause >nul