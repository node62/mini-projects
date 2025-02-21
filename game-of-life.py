#!/usr/bin/env python3
"""A simple Game of Life simulator with random initialization."""
import numpy as np
import time
import os

def main():
    s = int(input("Size: "))
    b = np.random.randint(2, size=(s, s))
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        for r in b:
            print(''.join(['#' if x else '.' for x in r]))
        nb = np.copy(b)
        for i in range(s):
            for j in range(s):
                n = np.sum(b[max(0, i-1):min(s, i+2), max(0, j-1):min(s, j+2)]) - b[i, j]
                if b[i, j] == 1:
                    if n < 2 or n > 3:
                        nb[i, j] = 0
                else:
                    if n == 3:
                        nb[i, j] = 1
        b = nb
        time.sleep(0.5)

if __name__ == '__main__':
    main()
