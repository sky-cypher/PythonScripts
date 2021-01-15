#!/usr/bin/env python3
from colorama import Fore, Style, init
from time import sleep, time
from os import system

sudoku = [ [ y*0 for y in range(9) ] for x in range(9) ]
init(autoreset = True)
start_time = 0
end_time = 0
display_time = 0.0

def check(row, column, value):
    if value in sudoku[row][:]:
        return False
    for i in range(9):
        if value == sudoku[i][column]:
            return False
    blk_row = (row//3)*3
    blk_column = (column//3)*3
    for x in range(blk_row, blk_row + 3):
        for y in range(blk_column, blk_column + 3):
            if sudoku[x][y] == value:
                return False
    return True


def print_sudoku(row = None, column = None, add = None, final = False):
    global display_time
    display_time += delay
    sleep(delay)
    system('clear')
    not final and print('\n' * 6)
    for x in range(9):
        if x % 3 :
            print('\n\t', end = '')
        else:
            print(f'\n\t{"-" * 23}\n\t', end = '')
        for y in range(9):
            if y % 3 :
                s = ""
            else:
                s = "| "
            if (row == x and y == column) or final:
                if add or end_time:
                    print(f"{s}{Fore.GREEN}{sudoku[x][y]} ", end = '')
                else:
                    print(f"{s}{Fore.RED}{sudoku[x][y]} ", end = '')
            else:
                if not sudoku[x][y]:
                    print(f"{s}{Fore.BLUE}{sudoku[x][y]} ", end = '')
                else:
                    print(f"{s}{Fore.YELLOW}{sudoku[x][y]} ", end = '')
    print('\n')

def solve():
    global sudoku
    for row in range(9):
        for column in range(9):
            if not sudoku[row][column]:
                for value in range(1,10):
                    if check(row, column, value):
                        sudoku[row][column] = value
                        print_sudoku(row, column, True)
                        solve()
                        sudoku[row][column] = 0
                        print_sudoku(row, column, False)
                return
    global end_time, start_time
    end_time = time()
    print_sudoku(final = True)
    if 'n' in input("\ncontinue ? : ").lower():
        raise KeyboardInterrupt
    start_time += time() - end_time


def main():
    global delay, sudoku, start_time
    try:
        delay = float(input("Enter delay in seconds : "))
    except ValueError:
        delay = 0.01
    print_sudoku()
    while 'n' in input("Use defined sudoku ? : ").lower():
        for i in range(9):
            sudoku[i] = [int(x) for x in input(f"Enter row {i + 1} : ")]
            while len(sudoku[i]) < 9:
                sudoku[i].append(0)
            while len(sudoku[i]) > 9:
                sudoku[i].pop(-1)
        print_sudoku()
    start_time = time()
    try:
        solve()
    except KeyboardInterrupt:
       print_sudoku(final = True)
        quit()
    finally:
        if end_time:
            tat = abs(end_time - start_time)
            print(f"Time Required = {round(tat,4)} seconds\
                    \nDisplay time = {round(display_time, 4)}\
                    \nNet time = {round(tat - display_time, 4)}\n")


if __name__ == "__main__":
    main()
