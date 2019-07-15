#!/usr/bin/env python3

"""This version of numero ensures that each digit changes to a different digit
in each iteration."""

import os
import random
import shutil
import sys
import time

### Global "Constants" ###

SECS_TO_RUN = 3
SECS_TO_WAIT = 0.05

DIGIT_SEP = ' '
NUM_DIGITS = 5
MIN_NUM_DIGITS = 3
MAX_NUM_DIGITS = 20

ALL_DIGITS = list(map(str, range(0, 10)))

FINAL_DIGITS = [] # a list of digit characters
FINAL_SLEEP_MULTIPLIER = 1.5
FINALIZE_RANDOMLY = True

### Number Generation ###


def rand_digits():
    return [random.choice(ALL_DIGITS) for nd in range(NUM_DIGITS)]


def randomize(digits):
    newdigits = []
    for digit in digits:
        possible_digits = [d for d in ALL_DIGITS if d != digit]
        newdigits.append(random.choice(possible_digits))
    return newdigits


def finalize(digits, final_digits, width=0):
    # Determine the order in which to display the final digits
    indices = list(range(NUM_DIGITS))
    if FINALIZE_RANDOMLY:
        random.shuffle(indices)

    # Ensure that the next digits displayed are different from both the previous
    # digits and the final ones
    prev_digits = digits
    digits = randomize(prev_digits)
    for i, digit in enumerate(digits):
        if digit == final_digits[i]:
            disallowed = (prev_digits[i], final_digits[i])
            choices = [d for d in ALL_DIGITS if d not in disallowed]
            digits[i] = random.choice(choices)

    # Print the initial digits
    print_number(digits, width=width)

    sleeptime = SECS_TO_WAIT
    for ndx in indices:
        digits[ndx] = final_digits[ndx]
        sleeptime *= FINAL_SLEEP_MULTIPLIER
        print_number(digits, sleeptime=sleeptime, width=width)


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


### Terminal & System Info ###


def is_windows():
    return sys.platform.startswith('win32')


def cols_lines():
    return shutil.get_terminal_size()


### Getting Input Values ###


def get_user_settings():
    global NUM_DIGITS, FINAL_DIGITS, FINALIZE_RANDOMLY

    print('\nEnter the number for the option you want:')
    print('\t1. Specify a number of digits to generate')
    print('\t2. Provide a specific number to generate')
    res = input('\nOption: ')
    if res not in '12':
        print('Option not recognized')
        sys.exit(1)

    minnum, maxnum = MIN_NUM_DIGITS, MAX_NUM_DIGITS
    if res == '1':
        prompt = f'\nEnter a number of digits between {minnum} and {maxnum}: '
        numdigits = input(prompt)
        if not (numdigits.isdigit() and minnum <= int(numdigits) <= maxnum):
            raise ValueError('Enter a valid number of digits')
        NUM_DIGITS = int(numdigits)
    elif res == '2':
        prompt = f'\nEnter a number that has between {minnum} and {maxnum} digits: '
        num = input(prompt)
        if not (num.isdigit() and minnum <= len(num) <= maxnum):
            raise ValueError('Enter a valid number')
        FINAL_DIGITS = [digit for digit in num]
        NUM_DIGITS = len(FINAL_DIGITS)

    msg = '\nWould you like to display the final digits in a random order? (y/n) '
    resp = input(msg)
    FINALIZE_RANDOMLY = resp == 'y'


def get_random_settings():
    global NUM_DIGITS, FINAL_DIGITS, FINALIZE_RANDOMLY
    NUM_DIGITS = random.randint(MIN_NUM_DIGITS, MAX_NUM_DIGITS)
    FINALIZE_RANDOMLY = bool(random.randint(0, 1))


### Main ###


def main():
    print('\nNow is the time to resize the console, if you wish.')
    pause(1)

    # Initialize the necessary settings either randomly or from user input
    resp = input('\nUse default random values? (y/n) ')
    if resp == 'y':
        get_random_settings()
    else:
        get_user_settings()

    # Center the number in the terminal
    cols, lines = cols_lines()
    lines_before = lines // 2
    lines_after = lines - lines_before - 1
    clear_screen()
    newlines(lines_before)

    # Generate the initial and final numbers to display
    digits = rand_digits()
    final_digits = FINAL_DIGITS if FINAL_DIGITS else rand_digits()

    start = time.perf_counter()
    while time.perf_counter() - start < SECS_TO_RUN:
        digits = randomize(digits)
        print_number(digits, width=cols)

    # Change current number to final number, one digit at a time
    finalize(digits, final_digits, width=cols)

    # Display the final prompt at the bottom of the screen (this is useful for
    # keeping the console window open until user ready to quit)
    newlines(lines_after)
    response = input('Please press enter when complete . . . ')
    clear_screen()
    if response:
        print(f'\nI told you to hit enter; why\'d you type "{response}"???')


if __name__ == '__main__':
    try:
        main()
    except:
        print('Error :(')
        pass
