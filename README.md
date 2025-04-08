# Macropad – Arduino-Powered Desktop Action Launcher

A Python-based GUI tool that listens to an Arduino-powered macropad (with buttons + potentiometer)
and performs user-defined actions like opening websites, launching apps, or adjusting volume.

### ⚙️ Features
- Custom action mapping for each button (Website or App)
- Realtime volume control using Arduino potentiometer
- GUI interface for setting + saving presets
- Auto-load preset from dropdown
- Uses Pycaw for Windows volume, Tkinter for UI, Serial for Arduino

### 🛠 Requirements

```bash
pip install pycaw pyserial comtypes
