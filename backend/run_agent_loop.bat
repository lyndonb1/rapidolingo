@echo off
:loop
echo Starting agent worker...
python working_agent.py
echo Agent crashed, restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto loop
