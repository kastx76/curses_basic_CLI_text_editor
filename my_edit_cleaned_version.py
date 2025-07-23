#!/bin/python3
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import sys
import signal


def head_init(stdscr, maxX):
    head = curses.newwin(1, maxX, 0, 0)
    head.bkgd(' ', curses.A_REVERSE)
    head.addstr(0, maxX // 2 - 7, 'Kast Editor')
    head.refresh()
    return head


def foot_display(foot, maxX):
    foot.addstr(1, maxX // 2 - 4, '^X', curses.A_REVERSE)
    foot.addstr(' Exit')
    foot.refresh()


def to_exit(stdscr, text_window, foot, buffer, filename):
    maxY, maxX = stdscr.getmaxyx()
    
    foot.clear()
    foot.addstr(1, 0, ' Y', curses.A_REVERSE)
    foot.addstr(' YES')
    foot.addstr(2, 0, ' N', curses.A_REVERSE)
    foot.addstr(' NO')
    foot.addstr(1, maxX // 2, ' C', curses.A_REVERSE)
    foot.addstr(' Cancel')
    foot.addstr(0, 0, 'Do you want to save this buffer ? ')
    foot.refresh()

    while True:
        key = chr(stdscr.getch())

        if key in ('N', 'n'):
            exit()

        elif key in ('C', 'c'):
            y, x = text_window.getyx()
            foot.clear()
            foot_display(foot, maxX)
            text_window.move(y, x)
            break

        elif key in ('Y', 'y'):
            if filename == '':
                curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
                curses.echo()
                stdscr.clear()
                stdscr.refresh()

                height = 7
                width = maxX - 4
                start_y = maxY // 2 - height // 2
                start_x = 2
                win = curses.newwin(height, width, start_y, start_x)
                win.box()

                rect_top = 1
                rect_left = 2
                rect_bottom = height - 2
                rect_right = width - 3
                rectangle(win, rect_top, rect_left, rect_bottom, rect_right)

                prompt = "Enter the file name: "
                prompt_y = rect_top + 2
                prompt_x = maxX // 4
                if prompt_x + len(prompt) + 20 > rect_right:
                    prompt_x = rect_right - len(prompt) - 20

                win.addstr(prompt_y, prompt_x, prompt)
                win.attron(curses.color_pair(1))
                win.refresh()

                filename = win.getstr(24).decode()
                if filename == '':
                    filename = 'buffer.txt'

            with open(filename, 'w') as f:
                f.write(buffer)
            exit()


def main(stdscr):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    stdscr.clear()
    stdscr.refresh()
    maxY, maxX = stdscr.getmaxyx()

    head = head_init(stdscr, maxX)
    foot = curses.newwin(3, maxX, maxY - 3, 0)
    foot_display(foot, maxX)

    text_window = curses.newpad(1000, 300)  # lines, cols

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        try:
            with open(sys.argv[1], 'r') as f:
                lines = f.readlines()
            if lines == []:
                lines = ['']
        except:
            filename = sys.argv[1]
            lines = ['']
    else:
        filename = ''
        lines = ['']

    buffer = ''.join(lines)
    text_window.addstr(0, 0, buffer)
    text_window.clear()
    text_window.refresh(0, 0, 1, 0, maxY - 4, maxX - 1)

    y, x = text_window.getyx()

    # Main loop
    while True:
        text_window.clear()
        text_window.addstr(0, 0, buffer)
        text_window.move(y, x)

        scroll_offset = y - maxY + 5
        scroll_offset = scroll_offset if scroll_offset > 0 else 0
        horiz_offset = maxX if x > maxX - 1 else 0

        text_window.refresh(scroll_offset, horiz_offset, 1, 0, maxY - 4, maxX - 1)
        key = stdscr.getch()

        # Navigation
        if key == curses.KEY_UP:
            if y > 0:
                y -= 1
                line = lines[y]
                x = min(x, len(line.rstrip('\n')))

        elif key == curses.KEY_DOWN:
            if y + 1 < len(lines):
                y += 1
                line = lines[y]
                x = min(x, len(line.rstrip('\n')))

        elif key == curses.KEY_LEFT:
            if x > 0:
                x -= 1
            elif y != 0:
                y -= 1
                x = len(lines[y].rstrip('\n'))

        elif key == curses.KEY_RIGHT:
            line = lines[y]
            line_limit = len(line.rstrip('\n'))
            if x < line_limit:
                x += 1
            elif y + 1 < len(lines):
                y += 1
                x = 0

        # Backspace
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if x == 0:
                if y > 0:
                    next_line = lines.pop(y)
                    prev_line = lines[y - 1]
                    x = len(prev_line) - 1
                    lines[y - 1] = prev_line[:-1] + next_line
                    y -= 1
            else:
                curr_line = lines[y]
                lines[y] = curr_line[:x - 1] + curr_line[x:]
                x -= 1

        # Enter key (newline)
        elif key in (10, 13, curses.KEY_ENTER):
            current = lines[y]
            lines[y] = current[:x] + '\n'
            new_line = current[x:]
            y, x = y + 1, 0
            lines.insert(y, new_line)

        # Exit prompt
        elif key == 24:
            to_exit(stdscr, text_window, foot, buffer, filename)

        # Printable characters
        elif 32 <= key <= 126:
            if y < len(lines):
                line = lines[y]
                lines[y] = line[:x] + chr(key) + line[x:]
                x += 1

        buffer = ''.join(lines)

    stdscr.getch()


wrapper(main)
