import tkinter as tk
from tkinter import messagebox
import psutil
import os
import ctypes
import time

def find_roblox_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'RobloxPlayerBeta.exe':
            return proc.info['pid']
    return None

def inject_dll(process_id, dll_path):
    try:
        kernel32 = ctypes.windll.kernel32
        h_process = kernel32.OpenProcess(0x1F0FFF, False, process_id)
        
        if not h_process:
            messagebox.showerror("Error", "Failed to open Roblox process.")
            return False

        dll_path_bytes = dll_path.encode('utf-8')
        alloc_address = kernel32.VirtualAllocEx(h_process, None, len(dll_path_bytes), 0x3000, 0x40)
        
        if not alloc_address:
            messagebox.showerror("Error", "Failed to allocate memory in Roblox process.")
            return False

        written = ctypes.c_int(0)
        kernel32.WriteProcessMemory(h_process, alloc_address, dll_path_bytes, len(dll_path_bytes), ctypes.byref(written))
        kernel32.CreateRemoteThread(h_process, None, 0, kernel32.LoadLibraryA, alloc_address, 0, None)

        messagebox.showinfo("Success", "DLL Injected Successfully!")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        return False

def run_gui():
    root = tk.Tk()
    root.title("Redax Executor - Auto DLL Injector")
    root.geometry("400x250")

    def start_injection():
        messagebox.showinfo("Waiting for Roblox...", "Waiting for Roblox to start...")
        while True:
            process_id = find_roblox_process()
            if process_id:
                dll_path = os.path.abspath("../dll/redax.dll")
                if not os.path.exists(dll_path):
                    messagebox.showerror("Error", f"DLL not found at: {dll_path}")
                    return

                inject_dll(process_id, dll_path)
                break
            time.sleep(1) 

    tk.Label(root, text="Redax Executor", font=("Helvetica", 16)).pack(pady=10)
    inject_button = tk.Button(root, text="Start Auto Injection", command=start_injection)
    inject_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
