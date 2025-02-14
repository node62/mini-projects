#!/usr/bin/env python3
"""
simple ASCII clock. lol.
"""
import time
import os
from datetime import datetime

digits = {
    "0": [" _ ", "| |", "|_|"],
    "1": ["   ", "  |", "  |"],
    "2": [" _ ", " _|", "|_ "],
    "3": [" _ ", " _|", " _|"],
    "4": ["   ", "|_|", "  |"],
    "5": [" _ ", "|_ ", " _|"],
    "6": [" _ ", "|_ ", "|_|"],
    "7": [" _ ", "  |", "  |"],
    "8": [" _ ", "|_|", "|_|"],
    "9": [" _ ", "|_|", " _|"],
    ":": ["   ", " o ", " o "]
}

def print_time_ascii(current_time):
    lines = ["", "", ""]
    for ch in current_time:
        seg = digits.get(ch, ["   ", "   ", "   "])
        lines[0] += seg[0] + " "
        lines[1] += seg[1] + " "
        lines[2] += seg[2] + " "
    print("\n".join(lines))

if __name__ == "__main__":
    while True:
        os.system('clear')
        now = datetime.now().strftime("%H:%M:%S")
        print_time_ascii(now)
        time.sleep(1)
