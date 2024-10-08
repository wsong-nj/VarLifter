#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:51:59 2024

@author: lyc
"""
from tkinter import Scrollbar
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import subprocess
import threading
import os

stop_analysis = False

def run_analysis():
    global stop_analysis
    stop_analysis = False

    bytecode = entry.get()
    with open('input_bytecode', 'w') as f:
        f.write(bytecode)
    
    analysis_thread = threading.Thread(target=analyze_bytecode)
    analysis_thread.start()

    progress_bar.start()

def analyze_bytecode():
    global stop_analysis

    if stop_analysis:
        progress_bar.stop()
        return

    subprocess.run(['python3', 'run_VarLifter.py'])

    if stop_analysis:
        progress_bar.stop()
        return

    with open('output_VaTy.txt', 'r') as f:
        output = f.read()
        output_text.delete(1.0, tk.END)

        lines = output.splitlines()
        formatted_output = "\n\n".join(lines)
        output_text.insert(tk.END, formatted_output)

    progress_bar.stop()

def stop_analysis_task():
    global stop_analysis
    stop_analysis = True
    progress_bar.stop()

def run_batch_analysis():
    global stop_analysis
    stop_analysis = False

    folder_path = folder_entry.get()
    if not os.path.isdir(folder_path):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Invalid folder path.")
        return
    
    batch_thread = threading.Thread(target=batch_analyze_bytecode, args=(folder_path,))
    batch_thread.start()

    progress_bar.start()

def batch_analyze_bytecode(folder_path):
    global stop_analysis

    output_text.delete(1.0, tk.END)
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            if stop_analysis:
                progress_bar.stop()
                return

            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as f:
                bytecode = f.read()

            with open('input_bytecode', 'w') as f:
                f.write(bytecode)

            subprocess.run(['python3', 'run_VarLifter.py'])

            if stop_analysis:
                progress_bar.stop()
                return

            with open('output_VaTy.txt', 'r') as f:
                output = f.read()
                output_text.insert(tk.END, "\n\n")
                output_text.insert(tk.END, f"Output for {filename}:\n")
                output_text.insert(tk.END, "\n\n")
                lines = output.splitlines()
                formatted_output = "\n\n".join(lines) 
                output_text.insert(tk.END, formatted_output)
                output_text.insert(tk.END, "\n\n" + "="*126 + "\n\n")
                

    progress_bar.stop()

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_selected)

def main():
    global entry, folder_entry, output_text, progress_bar, scrollbar

    app = tk.Tk()
    app.title("VarLifter GUI")

    canvas = tk.Canvas(app, height=600, width=800, bg="#263D42")
    canvas.pack()
    welcome_text = ("VarLifter")
    canvas.create_text(400, 50, text=welcome_text, fill="white", font=("Impact", 36), width=780)

    frame = tk.Frame(app, bg="purple")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    title = tk.Label(frame, text="Welcome to VarLifter! Casting light on what EVM knows but you don't: lifting variables and their types from compiled Solidity smart contracts.", font=("Impact", 12, "bold"), bg="purple", fg="white")
    title.pack(pady=10)

    input_frame = tk.Frame(frame, bg="purple")
    input_frame.pack(pady=10)

    label = tk.Label(input_frame, text="Enter Bytecode:", bg="white")
    label.grid(row=0, column=0, padx=5)

    entry = tk.Entry(input_frame)
    entry.grid(row=0, column=1, padx=5)

    folder_label = tk.Label(input_frame, text="Input Folder Path:", bg="white")
    folder_label.grid(row=1, column=0, padx=5)

    folder_entry = tk.Entry(input_frame)
    folder_entry.grid(row=1, column=1, padx=5)

    select_folder_button = tk.Button(input_frame, text="Select Folder", padx=10, pady=5, fg="white", bg="#263D42", command=select_folder)
    select_folder_button.grid(row=1, column=2, padx=5)

    button_frame = tk.Frame(frame, bg="purple")
    button_frame.pack(pady=10)

    run_button = tk.Button(button_frame, text="Run Analysis", padx=10, pady=5, fg="white", bg="#263D42", command=run_analysis)
    run_button.grid(row=0, column=0, padx=5)

    batch_run_button = tk.Button(button_frame, text="Run Batch Analysis", padx=10, pady=5, fg="white", bg="#263D42", command=run_batch_analysis)
    batch_run_button.grid(row=0, column=1, padx=5)

    stop_button = tk.Button(button_frame, text="Stop Analysis", padx=10, pady=5, fg="white", bg="red", command=stop_analysis_task)
    stop_button.grid(row=0, column=2, padx=5)

    style = ttk.Style()
    style.configure("TProgressbar",
                    thickness=22,            
                    troughcolor='white',    
                    background='#263D42',
                    
                    )

    progress_bar = ttk.Progressbar(button_frame, mode='indeterminate', length=100, style='TProgressbar')
    progress_bar.grid(row=0, column=3, padx=5)

    output_label = tk.Label(frame, text="Output:", bg="white")
    output_label.pack()

    output_text = tk.Text(frame, height=300, width=500)
    output_text.pack()

    scrollbar = Scrollbar(frame, orient="vertical", command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.config(yscrollcommand=scrollbar.set)


    app.mainloop()

if __name__ == "__main__":
    main()


