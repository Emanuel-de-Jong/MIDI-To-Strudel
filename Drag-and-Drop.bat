@echo off
set "MIDI_PATH=%~1"

where python >nul 2>&1
if %errorlevel%==0 (
    python "%~dp0Midi-to-Strudel.py" --midi "%MIDI_PATH%"
) else (
    where python3 >nul 2>&1
    if %errorlevel%==0 (
        python3 "%~dp0Midi-to-Strudel.py" --midi "%MIDI_PATH%"
    ) else (
        echo Python is not installed or not set in the PATH environment variable.
    )
)

pause
