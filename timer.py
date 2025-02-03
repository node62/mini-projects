#!/usr/bin/env python3

"""
Timer Application

This script provides a simple GUI-based countdown timer and stopwatch using Tkinter.
It allows users to set a task name and time duration, displaying a progress bar and 
color-coded feedback as the timer runs. The program supports daemonization, 
keyboard shortcuts for quick interactions, and a stopwatch mode for counting up.

"""

import os, sys, re, tkinter as tk
from tkinter import ttk

def daemonize():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    os.chdir("/")
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    sys.stdout.flush()
    sys.stderr.flush()
    with open("/dev/null", "rb", 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open("/dev/null", "ab", 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

class TimerApp:
    def __init__(self, root):
        self.root = root
        
        w, h = 250, 100
        x = 0
        y = self.root.winfo_screenheight() - h
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)
        self.root.title("Timer")
        self.paused = False
        self.stopwatch = False  
        self.total_time = 0
        self.remaining_time = 0
        self.elapsed_time = 0
        self.create_input_frame()
        self.create_timer_frame()
        self.show_input()
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("n", lambda e: self.new_timer())
        self.root.bind("r", lambda e: self.restart_timer())
        self.root.bind("q", lambda e: self.root.destroy())

    def create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg="black")
        font = ("Courier", 14)
        self.task_label = tk.Label(self.input_frame, text="Task:", font=font, bg="black", fg="cyan", anchor="w")
        self.task_label.grid(row=0, column=0, padx=(15,5), pady=(15,5), sticky="w")
        self.task_entry = tk.Entry(self.input_frame, font=font, justify="left", bg="black", fg="white",
                                   insertbackground="white", relief="flat")
        self.task_entry.grid(row=0, column=1, padx=(0,15), pady=(15,5), sticky="we")
        self.time_label = tk.Label(self.input_frame, text="Time:", font=font, bg="black", fg="cyan", anchor="w")
        self.time_label.grid(row=1, column=0, padx=(15,5), pady=(5,15), sticky="w")
        self.time_entry = tk.Entry(self.input_frame, font=font, justify="left", bg="black", fg="white",
                                   insertbackground="white", relief="flat")
        self.time_entry.grid(row=1, column=1, padx=(0,15), pady=(5,15), sticky="we")
        self.input_frame.columnconfigure(1, weight=1)
        self.input_frame.bind_all("<Return>", lambda e: self.start_timer())

    def create_timer_frame(self):
        self.timer_frame = tk.Frame(self.root, bg="black")
        font_mono_small = ("Courier", 15)
        font_mono_large = ("Courier", 24)
        self.task_disp = tk.Label(self.timer_frame, text="", font=font_mono_small, bg="black", fg="white")
        self.task_disp.pack(pady=(5,2))
        self.time_disp = tk.Label(self.timer_frame, text="", font=font_mono_large, bg="black", fg="green")
        self.time_disp.pack(pady=(2,2))
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=8, background="green")
        self.progress = ttk.Progressbar(self.timer_frame, orient="horizontal", length=200, mode="determinate",
                                        style="TProgressbar")
        self.progress.pack(pady=(2,2))

    def show_input(self):
        self.timer_frame.pack_forget()
        self.input_frame.pack(expand=True, fill="both")
        self.task_entry.focus_set()

    def show_timer(self):
        self.input_frame.pack_forget()
        self.timer_frame.pack(expand=True, fill="both")

    def parse_time(self, s):
        s = s.strip().lower()
        if any(x in s for x in ['h','m','s']):
            pattern = r'(?:(?P<h>\d+)\s*h)?\s*(?:(?P<m>\d+)\s*m)?\s*(?:(?P<s>\d+)\s*s?)?'
            m = re.fullmatch(pattern, s)
            if m:
                h = int(m.group("h")) if m.group("h") else 0
                m_val = int(m.group("m")) if m.group("m") else 0
                s_val = int(m.group("s")) if m.group("s") else 0
                return h*3600 + m_val*60 + s_val
            return None
        try:
            return int(s) * 60
        except:
            return None

    def format_time(self, sec):
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        if h > 0:
            return f"{h}h {m:02d}m {s:02d}s"
        elif m > 0:
            return f"{m}m {s:02d}s"
        else:
            return f"{s:02d}s"

    def start_timer(self):
        task = self.task_entry.get().strip()
        time_input = self.time_entry.get().strip().lower()
        if not task:
            return

        if time_input == "s":
            
            self.stopwatch = True
            self.elapsed_time = 0
            self.paused = False
            self.task = task
            self.task_disp.config(text=self.task)
            
            self.time_disp.config(font=("Courier", 24), bg="black", fg="cyan")
            self.root.configure(bg="black")
            self.timer_frame.configure(bg="black")
            self.task_disp.configure(bg="black", fg="white")
            
            self.progress.pack_forget()
            self.show_timer()
            self.update_stopwatch()
            return

        t = self.parse_time(time_input)
        if t is None or t <= 0:
            return

        self.stopwatch = False
        self.task = task
        self.total_time = t
        self.remaining_time = t
        self.paused = False
        self.task_disp.config(text=self.task)
        self.progress.config(maximum=self.total_time, value=0)
        self.root.configure(bg="black")
        self.timer_frame.configure(bg="black")
        self.task_disp.configure(bg="black", fg="white")
        self.time_disp.configure(bg="black", fg="green")
        
        self.progress.pack(pady=(2,2))
        self.show_timer()
        self.update_timer()

    def update_timer(self):
        
        if not self.paused and self.remaining_time > 0:
            self.remaining_time -= 1
            self.progress["value"] = self.total_time - self.remaining_time

        
        perc = self.remaining_time / self.total_time if self.total_time else 0
        if perc < 0.1:
            col = "red"
        elif perc < 0.5:
            col = "orange"
        else:
            col = "green"

        if self.paused:
            self.root.configure(bg=col)
            self.timer_frame.configure(bg=col)
            self.task_disp.configure(bg=col, fg="black")
            self.time_disp.configure(bg=col, fg="black")
        else:
            self.root.configure(bg="black")
            self.timer_frame.configure(bg="black")
            self.task_disp.configure(bg="black", fg="white")
            self.time_disp.configure(bg="black", fg=col)

        self.time_disp.config(text=self.format_time(max(int(self.remaining_time), 0)))
        if self.remaining_time > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.time_disp.config(text="Time's up!")

    def update_stopwatch(self):
        
        if not self.paused:
            self.elapsed_time += 1

        
        if self.paused:
            self.root.configure(bg="cyan")
            self.timer_frame.configure(bg="cyan")
            self.task_disp.configure(bg="cyan", fg="black")
            self.time_disp.configure(bg="cyan", fg="black")
        else:
            self.root.configure(bg="black")
            self.timer_frame.configure(bg="black")
            self.task_disp.configure(bg="black", fg="white")
            self.time_disp.configure(bg="black", fg="cyan")

        self.time_disp.config(text=self.format_time(self.elapsed_time))
        self.root.after(1000, self.update_stopwatch)

    def toggle_pause(self, event):
        self.paused = not self.paused

    def new_timer(self):
        self.paused = False
        self.show_input()

    def restart_timer(self):
        self.paused = False
        if self.stopwatch:
            self.elapsed_time = 0
            self.time_disp.config(text=self.format_time(self.elapsed_time))
        else:
            self.remaining_time = self.total_time
            self.progress["value"] = 0

if __name__ == '__main__':
    daemonize()
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
