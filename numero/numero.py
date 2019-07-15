#!/usr/bin/env python3

"""This version of numero generates a completely new random number to display in
each iteration."""

import os
import random
import shutil
import sys
import time

### Global "Constants" ###

SECS_TO_WAIT = 0.05
SECS_TO_RUN = 3

NUM_DIGITS = 5
DIGIT_SEP = ' '

FINAL_DIGITS = [] # a list of digit characters
FINAL_SLEEP_MULTIPLIER = 1.5
FINALIZE_RANDOMLY = True

### Number Generation ###


def rand_digits():
    return [str(random.randint(0, 9)) for nd in range(NUM_DIGITS)]


### Printing ###


def display(string):
    print(string, end='', flush=True)


def print_number(digits, sleeptime=SECS_TO_WAIT, width=0):
    pause(secs=sleeptime)
    reset_cursor()
    # center apparently appends a newline on windows?
    num = DIGIT_SEP.join(digits).center(width).rstrip('\n')
    display(num)


def reset_cursor():
    # A carriage return to place the cursor at the line start
    display('\r')


def newlines(num):
    display(''.join(['\n'] * num))


def clear_screen():
    os.system('cls' if is_windows() else 'clear')


### Time Functions ###


def pause(secs=SECS_TO_WAIT):
    time.sleep(secs)


### Generating Final Number ###


def finalize(digits, final_digits, width=0):
    indices = list(range(NUM_DIGITS))
    if FINALIZE_RANDOMLY:
        random.shuffle(indices)

    sleeptime = SECS_TO_WAIT
    for ndx in indices:
        digits[ndx] = final_digits[ndx]
        sleeptime *= FINAL_SLEEP_MULTIPLIER
        print_number(digits, sleeptime=sleeptime, width=width)


### Terminal Info ###


def is_windows():
    return sys.platform.startswith('win32')


def cols_lines():
    return shutil.get_terminal_size()


### Main ###


def main():
    # Center the number in the terminal
    cols, lines = cols_lines()
    lines_before = lines // 2
    lines_after = lines - lines_before - 1
    clear_screen()
    newlines(lines_before)

    # Determine the final number to generate
    final_digits = FINAL_DIGITS if FINAL_DIGITS else rand_digits()

    start = time.perf_counter()
    while time.perf_counter() - start < SECS_TO_RUN:
        digits = rand_digits()
        print_number(digits, width=cols)

    # Change current number to final number, one digit at a time
    finalize(digits, final_digits, width=cols)

    # Display the final prompt at the bottom of the screen (this is useful for
    # keeping the console window open until user ready to quit)
    newlines(lines_after)
    response = input('Please press enter when complete . . . ').rstrip('\n')
    clear_screen()
    if response:
        print(f'I told you to hit enter; why\'d you type "{response}"???')


if __name__ == '__main__':
    main()
