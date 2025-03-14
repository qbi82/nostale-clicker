import win32api
import win32gui
import win32con
import time
import threading
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

def get_game_windows():
    windows = []
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if "NosTale" in title:
            windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

def send_key_to_window(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, ord(key), 0)
    time.sleep(0.05)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord(key), 0)

def clicking_thread(game_hwnd, times, delay, key):
    global running
    running = True
    clicks = 0
    while running and clicks < times:
        send_key_to_window(game_hwnd, key)
        clicks += 1
        time.sleep(delay)
        if clicks % 10 == 0:
            print(f"Kliknięć: {clicks}")
    print("Zakończono klikanie.")

def start_clicking():
    global click_thread, running
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Błąd", "Wybierz klienta gry!")
        return
    game_hwnd = game_windows[selected[0]][0]
    times = int(times_var.get())
    delay = float(delay_var.get())
    key = key_var.get().upper()
    if len(key) != 1:
        messagebox.showwarning("Błąd", "Wpisz tylko jeden znak dla klawisza!")
        return
    running = True
    click_thread = threading.Thread(target=clicking_thread, args=(game_hwnd, times, delay, key))
    click_thread.start()

def stop_clicking():
    global running
    running = False

def refresh_clients():
    global game_windows
    game_windows = get_game_windows()
    listbox.delete(0, tk.END)
    for hwnd, title in game_windows:
        listbox.insert(tk.END, title)

def on_press(key):
    if key == keyboard.Key.f7:
        stop_clicking()
        return False

# GUI
root = tk.Tk()
root.title("NosTale Bot")

frame = tk.Frame(root)
frame.pack()

left_frame = tk.Frame(frame)
left_frame.pack(side=tk.LEFT, padx=10)

right_frame = tk.Frame(frame)
right_frame.pack(side=tk.BOTTOM, padx=10)

tk.Label(left_frame, text="NosTale Clients:").pack()
listbox = tk.Listbox(left_frame)
listbox.pack()
refresh_clients()

tk.Button(left_frame, text="Refresh", command=refresh_clients).pack()

tk.Label(left_frame, text="Times:").pack()
times_var = tk.StringVar(value="5")
tk.Entry(left_frame, textvariable=times_var).pack()

tk.Label(left_frame, text="Delay (s):").pack()
delay_var = tk.StringVar(value="0.5")
tk.Entry(left_frame, textvariable=delay_var).pack()

tk.Label(left_frame, text="Key to Press:").pack()
key_var = tk.StringVar(value="Q")
tk.Entry(left_frame, textvariable=key_var).pack()

tk.Button(left_frame, text="Start", command=start_clicking).pack()
tk.Button(left_frame, text="Stop", command=stop_clicking).pack()

tk.Label(left_frame, text="Press F7 to stop").pack()

tk.Label(right_frame, text="Made by: Qbi & Daron", font=("Arial", 8, "bold")).pack()

# Listener for ESC
listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
