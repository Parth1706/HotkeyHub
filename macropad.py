import os
import serial
import webbrowser
import subprocess
import time
import tkinter as tk
from tkinter import messagebox, Menu
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import json
import threading

# Serial setup
arduino_port = 'COM5'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

# Audio control setup for Windows
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Preset directory
preset_dir = "presets"
os.makedirs(preset_dir, exist_ok=True)

# Default actions
actions = {
    "Button 1": {"mode": "Website", "value": "https://www.youtube.com"},
    "Button 2": {"mode": "Website", "value": "https://www.wikipedia.org"},
    "Button 3": {"mode": "Website", "value": "https://www.apple.com"}
}

# Function to save and load presets
def save_preset():
    preset_name = preset_entry.get().strip()
    if not preset_name:
        messagebox.showerror("Error", "Preset name cannot be empty!")
        return
    preset_path = os.path.join(preset_dir, f"{preset_name}.json")
    try:
        with open(preset_path, "w") as file:
            json.dump(actions, file, indent=4)
        messagebox.showinfo("Success", f"Preset '{preset_name}' saved successfully!")
        update_preset_dropdown()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save preset: {str(e)}")

def load_preset():
    preset_name = preset_var.get()
    if not preset_name or preset_name == "Select a preset":
        messagebox.showerror("Error", "Please select a preset to load!")
        return
    preset_path = os.path.join(preset_dir, f"{preset_name}.json")
    try:
        with open(preset_path, "r") as file:
            global actions
            actions = json.load(file)
        update_gui_from_actions()
        messagebox.showinfo("Success", f"Preset '{preset_name}' loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load preset: {str(e)}")

def update_gui_from_actions():
    mode_var1.set(actions["Button 1"]["mode"])
    entry1.delete(0, tk.END)
    entry1.insert(0, actions["Button 1"]["value"])

    mode_var2.set(actions["Button 2"]["mode"])
    entry2.delete(0, tk.END)
    entry2.insert(0, actions["Button 2"]["value"])

    mode_var3.set(actions["Button 3"]["mode"])
    entry3.delete(0, tk.END)
    entry3.insert(0, actions["Button 3"]["value"])

def update_preset_dropdown():
    presets = [f[:-5] for f in os.listdir(preset_dir) if f.endswith(".json")]
    preset_dropdown["menu"].delete(0, "end")
    for preset in presets:
        preset_dropdown["menu"].add_command(label=preset, command=tk._setit(preset_var, preset))
    preset_var.set("Select a preset")

def update_actions():
    actions["Button 1"]["mode"] = mode_var1.get()
    actions["Button 1"]["value"] = entry1.get() or actions["Button 1"]["value"]
    actions["Button 2"]["mode"] = mode_var2.get()
    actions["Button 2"]["value"] = entry2.get() or actions["Button 2"]["value"]
    actions["Button 3"]["mode"] = mode_var3.get()
    actions["Button 3"]["value"] = entry3.get() or actions["Button 3"]["value"]
    messagebox.showinfo("Success", "Actions updated successfully!")

# Handle Arduino inputs in a thread
def handle_arduino_input():
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data.isdigit():
                pot_value = int(data)
                volume_level = pot_value / 1023 * 100
                volume.SetMasterVolumeLevelScalar(volume_level / 100, None)
                print(f"Setting volume to {int(volume_level)}%")
            elif data == "Button 1 pressed":
                perform_action("Button 1")
            elif data == "Button 2 pressed":
                perform_action("Button 2")
            elif data == "Button 3 pressed":
                perform_action("Button 3")
        except Exception as e:
            print(f"Error reading from Arduino: {e}")

def perform_action(button):
    action = actions[button]
    if action["mode"] == "Website":
        webbrowser.open(action["value"])
        print(f"{button} pressed. Opening website: {action['value']}")
    elif action["mode"] == "App":
        subprocess.Popen([action["value"]])
        print(f"{button} pressed. Launching app: {action['value']}")

# GUI Setup
root = tk.Tk()
root.title("HOTKEYHUB - A Reprogrammable Keyboard")
root.geometry("800x500")
root.configure(bg='#1E1E1E')

# Menu Bar
menu_bar = Menu(root, bg='#2E2E2E', fg='white')
root.config(menu=menu_bar)

frame = tk.Frame(root, bg='#1E1E1E')
frame.pack(pady=20, padx=20, fill='both', expand=True)

tk.Label(frame, text="MACROPAD - A Reprogrammable Keyboard", bg='#1E1E1E', fg='#FFFFFF', font=('Inter', 24)).grid(row=0, column=0, columnspan=3, pady=10)

modes = ["Website", "App"]

mode_var1 = tk.StringVar(value=actions["Button 1"]["mode"])
tk.OptionMenu(frame, mode_var1, *modes).grid(row=1, column=0, padx=10, pady=10)
entry1 = tk.Entry(frame, width=50, bg='#2E2E2E', fg='#FFFFFF', font=('Inter', 14))
entry1.insert(0, actions["Button 1"]["value"])
entry1.grid(row=1, column=1, padx=10, pady=10)

mode_var2 = tk.StringVar(value=actions["Button 2"]["mode"])
tk.OptionMenu(frame, mode_var2, *modes).grid(row=2, column=0, padx=10, pady=10)
entry2 = tk.Entry(frame, width=50, bg='#2E2E2E', fg='#FFFFFF', font=('Inter', 14))
entry2.insert(0, actions["Button 2"]["value"])
entry2.grid(row=2, column=1, padx=10, pady=10)

mode_var3 = tk.StringVar(value=actions["Button 3"]["mode"])
tk.OptionMenu(frame, mode_var3, *modes).grid(row=3, column=0, padx=10, pady=10)
entry3 = tk.Entry(frame, width=50, bg='#2E2E2E', fg='#FFFFFF', font=('Inter', 14))
entry3.insert(0, actions["Button 3"]["value"])
entry3.grid(row=3, column=1, padx=10, pady=10)

update_button = tk.Button(frame, text="Update Actions", command=update_actions, bg='#4CAF50', fg='white', font=('Inter', 16))
update_button.grid(row=4, columnspan=2, pady=20)

preset_frame = tk.Frame(frame, bg='#1E1E1E')
preset_frame.grid(row=5, columnspan=2, pady=10)

preset_var = tk.StringVar(value="Select a preset")
preset_dropdown = tk.OptionMenu(preset_frame, preset_var, "Select a preset")
preset_dropdown.config(width=20)
preset_dropdown.grid(row=0, column=0, padx=5)

preset_entry = tk.Entry(preset_frame, width=20, bg='#2E2E2E', fg='#FFFFFF', font=('Inter', 14))
preset_entry.grid(row=0, column=1, padx=5)

save_button = tk.Button(preset_frame, text="Save Preset", command=save_preset, bg='#2196F3', fg='white', font=('Inter', 12))
save_button.grid(row=0, column=2, padx=5)

load_button = tk.Button(preset_frame, text="Load Preset", command=load_preset, bg='#FF5722', fg='white', font=('Inter', 12))
load_button.grid(row=0, column=3, padx=5)

update_preset_dropdown()

# Start Arduino handler thread
threading.Thread(target=handle_arduino_input, daemon=True).start()

root.mainloop()
