# ⌨ Auto Typer — Desktop Application

A professional, modern auto-typing desktop app for Windows built with Python and CustomTkinter.

---

## Features

- **Modern dark UI** using CustomTkinter
- **Start / Pause / Resume / Stop / Reset / Restart** controls
- **Human-like typing** with random keystroke delays
- **Adjustable speed slider** (Very Slow → Very Fast)
- **Start delay** — gives you time to switch to the target window
- **Live text highlighting** — shows typed progress in the text box
- **Progress bar** with percentage
- **Global hotkeys** — work even when app is minimised
- **Completion notification** (Windows toast) + sound
- **Thread-safe** — no crashes or double-typing issues

---

## Hotkeys

| Shortcut         | Action                    |
|------------------|---------------------------|
| `Ctrl+Alt+S`     | Start / Pause / Resume    |
| `Ctrl+Alt+X`     | Stop                      |
| `Ctrl+Alt+R`     | Reset (clear everything)  |
| `Ctrl+Alt+T`     | Restart from beginning    |

---

## Installation

### 1. Requirements
- Python 3.10 or higher (Windows)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python main.py
```

---

## Build as Windows .exe

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --name "AutoTyper" main.py
```

The executable will be at `dist/AutoTyper.exe`.

---

## Usage Guide

1. **Paste or type** your text in the text area
2. Set a **Start Delay** (e.g. `3` seconds) so you have time to click into Notepad/Word/etc.
3. Click **▶ Start** (or press `Ctrl+Alt+S`)
4. Switch to your target application — typing will begin after the delay
5. Use **⏸ Pause** / **▶ Resume** to control mid-way
6. **↺ Restart** starts over from the beginning; **⟳ Reset** clears everything

---

## Notes

- `winsound` is Windows-only (built-in, no install needed)
- `plyer` notifications require Windows 10+
- Run as administrator if hotkeys don't respond in elevated windows (e.g. Task Manager)
