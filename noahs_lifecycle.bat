@echo off
chcp 65001 >nul 2>&1
title 诺亚斯生命周期守护
echo [%date% %time%] 诺亚斯生命周期守护启动...
python "%~dp0noahs_lifecycle.py"
echo [%date% %time%] 诺亚斯生命周期守护已停止，10秒后自动重启...
timeout /t 10 /nobreak >nul
goto :eof
