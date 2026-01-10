import threading
import customtkinter as ctk
import pythoncom
import os
import eye_mouse_control
import speech_typing

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def run_eye_control():
    eye_mouse_control.main()

def run_speech_typing():
    pythoncom.CoInitialize()
    speech_typing.main()

def start_threads():
    global eye_thread, speech_thread

    if not eye_thread.is_alive():
        eye_thread = threading.Thread(target=run_eye_control, daemon=True)
        eye_thread.start()
        eye_status_label.configure(text="Eye Control: Running", text_color="green")

    if not speech_thread.is_alive():
        speech_thread = threading.Thread(target=run_speech_typing, daemon=True)
        speech_thread.start()
        speech_status_label.configure(text="Speech Control: Running", text_color="green")

def stop_processes():
    os._exit(0)

app = ctk.CTk()
app.title("Multi-Control Panel")
app.geometry("400x300")
app.resizable(False, False)

title_label = ctk.CTkLabel(app, text="Multi-Control Panel", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

eye_status_label = ctk.CTkLabel(app, text="Eye Control: Stopped", text_color="red", font=("Arial", 14))
eye_status_label.pack(pady=5)

speech_status_label = ctk.CTkLabel(app, text="Speech Control: Stopped", text_color="red", font=("Arial", 14))
speech_status_label.pack(pady=5)

start_button = ctk.CTkButton(app, text="Start", command=start_threads, fg_color="green")
start_button.pack(pady=10)

stop_button = ctk.CTkButton(app, text="Stop", command=stop_processes, fg_color="red")
stop_button.pack(pady=10)

eye_thread = threading.Thread(target=run_eye_control, daemon=True)
speech_thread = threading.Thread(target=run_speech_typing, daemon=True)

app.mainloop()
