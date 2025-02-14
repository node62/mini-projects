#!/usr/bin/env python3
"""
simple python script to recursively solve the puzzle of moving disks between three rods.
"""
def hanoi(n, source, target, aux):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n-1, source, aux, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n-1, aux, target, source)

if __name__ == "__main__":
    n = int(input("Enter number of disks: "))
    hanoi(n, "A", "C", "B")
