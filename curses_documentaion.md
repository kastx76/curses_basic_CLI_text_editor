# 📚 Python `curses` Documentation
This guide explains how to use the `curses` module to build rich, text-based UIs in a terminal — covering windows, pads, colors, input, and more.
## 📚 Table of Contents
- [❓What is curses?](#-what-is-curses)
- [🐍 The Python `curses` module](#-the-python-curses-module-)
- [🚀 Starting and 🛑 Ending a curses App](#-starting-and--ending-a-curses-application)
- [📦 Curses Objects](#-curses-objects)
  - [1️⃣ Windows](#1%EF%B8%8F%E2%83%A3--windows)
  - [2️⃣ Pad](#2%EF%B8%8F%E2%83%A3-pad)
  - [3️⃣ Common Methods](#3️⃣-common-methods-for-windows-and-pads)
  - [4️⃣ `curses.textpad` Module ](#4%EF%B8%8F%E2%83%A3-cursestextpad-module)
  - [5️⃣ Module-Level `curses` Constants and Functions](#5️⃣-module-level-curses-constants-and-functions)
	 - [🔢 Constants](#-constants)
	- [🧩Functions](#-functions)
- [📎 Extra Resources](#-extra-resources)

---
## ❓ What is `curses`?
The **`curses`** library provides a **terminal-independent way to draw text-based UIs** and handle keyboard input in terminal environments. It abstracts complex terminal control codes (like cursor movement, screen clearing, etc.) behind a consistent API.

Even though text-based UIs are considered old, `curses` is still useful for:

- Minimal or embedded systems without graphical support
- Boot-time tools like installers or kernel config menus

It allows creating multiple text windows, writing/erasing text, and changing appearance (e.g., colors, styles). However, it **doesn’t include GUI elements** like buttons — libraries like **Urwid** are needed for that.

Originally built for BSD Unix, modern systems use **ncurses**, a free and extended version based on AT&T’s System V curses.

> 📌 Note: The standard Python `curses` module is not available on Windows, but you can use ports like **UniCurses**.

## 🐍 The Python curses module ?
The Python `curses` module is a **high-level wrapper** around the lower-level C `curses` functions. One of the biggest benefits is that it **combines multiple related C functions into a single, more flexible Python method**.

> **example** :  different C functions such as `addstr()`, `mvaddstr()`, and `mvwaddstr()` into a single `addstr()` method

## 🚀 Starting and 🛑 Ending a `curses` Application
Before doing anything with `curses`, the environment **must be initialized**. This is done by :
- Call `curses.initscr()` to:
  - Determine the terminal type
  - Send setup codes to the terminal
  - Allocate internal `curses` data structures
  - Return the main screen window — usually stored as `stdscr`
```python
import curses
stdscr = curses.initscr()
```

>**Note** :- `stdscr` represents the **entire screen**, just like the `stdscr` variable in C.
>**(Standard Screen Object)**

But it's more complex — you also need to handle many things, which makes running a curses app more complicated.

To avoid that, Python offers a safer and simpler option: instead of manually setting everything up and tearing it down, you can use `curses.wrapper()`.

```python
from curses import wrapper

def main(stdscr): 
    ... # note : every code bellow this is writen inside this block
    
wrapper(main)

```

The `wrapper()` function simplifies running a `curses` application by handling all the necessary setup and cleanup for you.

- It **initializes the curses environment**, including setting up the screen and color support (if available).
- It **creates the main screen window (`stdscr`)** and passes it to your main function.
- Your function runs inside a **`try…except` block**: if an error occurs, `wrapper()` catches the exception, **restores the terminal** to its original state, and then **re-raises** the exception so you can still see the traceback.
- Once your function exits normally, the terminal is cleaned up automatically.

> ✅ In short: `wrapper()` protects your terminal and makes your `curses` app safer and easier to write. 

## 📦 Curses Objects 

### 1️⃣  Windows 
In `curses`, a **window** is the core abstraction for working with screen regions. A window represents a **rectangular area** of the terminal and provides methods to:

- Display or erase text    
- Move the cursor
- Handle user input
- Control formatting or attributes
#### 🖥️ `stdscr` — The Default Window
When you initialize `curses` (via `initscr()` or `wrapper()`), you receive a special window object called `stdscr`, which covers the **entire screen**. For many simple applications, `stdscr` is enough.
#### ➕ Creating Custom Windows with `newwin()`
To divide the screen into **independent sections** (e.g. a header, footer, or pop-up box), you can create your own windows using:

```python
`win = curses.newwin(height, width, begin_y, begin_x)`
```
- `height`, `width` → size of the window
- `begin_y`, `begin_x` → position of the top-left corner of the window

**Example:**
```python
begin_y = 7
begin_x = 20
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
```

>**Note:** Each window can be drawn, updated, and cleared **independently** from others.
#### ⚠️ Coordinate Convention: `y, x` (Not `x, y`)

Be aware: unlike most graphics libraries, `curses` uses the coordinate order **`y, x`** — meaning:
```python
win.addstr(y, x, "Text")
```
This is because the terminal rows (y-axis) come first, followed by columns (x-axis). The top-left corner of any window is always `(0, 0)`.

> 📝 While this may feel backward at first (compared to the usual `x, y`), it’s a long-standing design in `curses`.

```SCSS
(0,0) ───────────────► x →
   │
   │
   ▼
   y (downward)
```
##### 🖼️ Terminal Screen Layout (Conceptual)
```lua
+-----------------------------------------------+
|                                               |
|                  stdscr                       |
|     (covers the entire terminal screen)       |
|                                               |
|   +----------------------------+              |
|   |                            |              |
|   |         newwin()           |              |
|   |    (custom sub-window)     |              |
|   |                            |              |
|   +----------------------------+              |
|                                               |
+-----------------------------------------------+
```
>**⚠️Warning :** When you call a method to display or erase text, the effect doesn’t immediately show up on the display. Instead you must call the `refresh()` method of window objects to update the screen.

### 2️⃣ `Pad` 
A pad is a special case of a window; it can be larger than the actual display screen, and only a portion of the pad displayed at a time. Creating a pad requires the pad’s height and width, while refreshing a pad requires giving the coordinates of the on-screen area where a subsection of the pad will be displayed.
#### ➕ Creating Custom Pads with `newpad()
A **pad** is like a window, but it can be **larger than the screen** and supports **scrolling**. Use it when you need to display a lot of content in a small area (e.g., logs, long text blocks)
```python
pad = curses.newpad(height, width)
```
- `height`, `width` → total size of the pad (can be much larger than the visible screen)

**Example:**
```python
pad = curses.newpad(100, 100)  # A 100×100 off-screen buffer
```

>**Note:**  ✅ Pads are ideal for scrollable views, long forms, or large editable text areas.
#### 📜 Pad vs Screen (Conceptual)
```
PAD (off-screen buffer)
+--------------------------------------------------------------+
| Line 0: Welcome to the application.                          |
| Line 1: Use arrow keys to navigate through content.          |
| Line 2: This is an example of a scrollable pad area.         |
| Line 3: Pads are useful for displaying large data blocks.    |
| Line 4: Only a portion is shown at any one time.             |
| Line 5: The rest remains off-screen until scrolled into view.|
| Line 6: You control what's visible using pad.refresh().      |
| ...                                                          |
| Line 999: [more content continues here...]                   |
+--------------------------------------------------------------+

            ▲
            │
        Only this region is displayed
            │

SCREEN VIEWPORT (drawn using pad.refresh())
+----------------------------------------------------+
| Line 3: Pads are useful for displaying large...    |
| Line 4: Only a portion is shown at any one time.   |
| Line 5: The rest remains off-screen until...       |
| Line 6: You control what's visible using...        |
+----------------------------------------------------+
```
###### example of pad :
```python
pad = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, 99):
    for x in range(0, 99):
        pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

# Displays a section of the pad in the middle of the screen.
# (0,0) : coordinate of upper-left corner of pad area to display.
# (5,5) : coordinate of upper-left corner of window area to be filled
#         with pad content.
# (20, 75) : coordinate of lower-right corner of window area to be
#          : filled with pad content.
pad.refresh( 0,0, 5,5, 20,75)
```
The `refresh()` call displays a section of the pad in the rectangle extending from coordinate (5,5) to coordinate (20,75) on the screen; the upper left corner of the displayed section is coordinate (0,0) on the pad. Beyond that difference, pads are exactly like ordinary windows and support the same methods.
### 3️⃣ Common Methods for Windows and Pads

Windows and pads in `curses` share most of the same interface. The methods below apply to all `window`-like objects, including `stdscr`, `newwin()` windows, and `newpad()` pads.

#### 🎨 1. **Styling and Visual Setup**

#####  `erase()`
  Clear the window.
  
```python
win.erase() # window or stdscr or pad , same for bellow
```
---
#####  `refresh()`
  Update the display immediately (sync actual screen with previous drawing/deleting methods). So , Used after adding text to show changes.
  for window doesn't need argument but for pad requires 6 argument 
  `refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)`
  
Displays a **specific rectangular region** of the pad on the physical screen.
This is what makes **scrolling** possible — you’re telling curses _which part of the pad_ to show and _where_ to show it on screen.
 
```python
win.refresh()
#for pad
pad.refresh(10, 0, 1, 0, 20, 75)# This means
# From the pad, show lines starting at row 10, column 0
# Display that region at screen row 1, column 0
# Stop drawing at screen row 20, column 75
```
---
#####  `clear()`
Like `erase()`, but also cause the whole window to be repainted upon next call to `refresh()`.
  
```python
win.clear()
```
---
#### 🖋️ 2. **Displaying Text and Drawing to the Screen**
#####   `addstr(y, x, string, attr=0)`
  Adds a string at position `(y, x)`. You can skip y , x and it write the string in the latest cursor position . 
  attributes are used for style displaying and text color and they are optional .
   
```python
win.addstr(1, 5, "Hello", curses.A_BOLD)#  Best practice
# or
win.addstr(str,curses.A_BOLD)
# or
win.addstr(str)
```
>**to display only a chat you can use `addch` same logic as `addstr` **

---
##### `border()`
   Draw a border around the edges of the window. It has some parameters ,Each one specifies the character to use for a specific part of the border.
   [For more details.](https://docs.python.org/3/library/curses.html)
 
```python
win.border()
```
---
#####  `box([vertch, horch])` 
Similar to [`border()`](https://docs.python.org/3/library/curses.html#curses.window.border "curses.window.border") , But with specifications
```python
win.box() # and you can add arguments
```
---
#####  `bkgd(ch, attr)`
  Set the background property of the window to the character **ch**, with attributes **attr**. The change is then applied to every character position in that window:

- The attribute of every character in the window is changed to the new background attribute.
- Wherever the former background character appears, it is changed to the new background character.
  
```python
win.bkgd(' ', curses.A_REVERSE)
```
---
#####  `attron(attr) / attroff(attr)
  Add / Remove attribute **attr** from the “background” set applied to all writes to the current window.
  
```python
win.attron(curses.A_BOLD)
win.addstr(2, 4, "Bold text")
win.attroff(curses.A_BOLD)
```
---
#####  `hline(y,x,ch, n) / vline(y,x,ch, n)`
  Display a horizontal / vertical line starting at `(y, x)` with length _n_ consisting of the character **ch** .
  
```python
win.hline(1, 0, '-', 40)  # Horizontal at y=1, from x=0, 40 chars
win.vline(0, 20, '|', 10)  # Vertical at x=20, from y=0, 10 chars
```
---
#### ✏️3. **Cursor Positioning and Movement**
#####  `getyx()`
Return a tuple `(y, x)` of current cursor position relative to the window’s upper-left corner.
  
```python
y, x = win.getyx()
```
---
#####  `getmaxyx()`
Return a tuple `(y, x)` of the height and width of the window.
  
```python
height, width = win.getmaxyx()
```
---
#####  `getbegyx()`
Returns the starting coordinates ( upper-left corner ) `(y, x)` of the window on the screen.
  
```python
start_y, start_x = win.getbegyx()
```
---
#####  `move(new_y,new_x)`
Move cursor to `(new_y, new_x)`.
  
```python
win.move(3, 10)
```
---
#### ⌨️4. **Keyboard Input Handling**
#####  `getch()`
Get a character.
- Returns an **int**: ASCII code (e.g. `97` for `'a'`) or **special key constant** like `curses.KEY_LEFT`.
- **Blocking by default** (waits for user input).
```python
ch = win.getch()
```
---
#####  `getkey()`
Get a character, returning a string instead of an integer, as `getch()` does.
- `"a"`, `"ENTER"`, `"KEY_UP"` — string version of the key
-  Handles Unicode and special keys
  
```python
key = win.getkey()
```
---
#####  `keypad(flag)`
Enables or disables special key support (like arrow keys and F1–F12).
- When   is`flag == True`:  
    Curses will **automatically recognize** special keys like arrows, Home, Delete, etc., and return **named constants** like `KEY_UP`, `KEY_F1`, etc.
- When `False`:  
    These keys will just send weird-looking escape sequences (like `\x1b[A`), and you’ll have to manually handle them — which is **hard and messy**.

```python
win.keypad(True)
```
---
#####  `nodelay(flag)`
Controls whether `getch()` (or `getkey()`) **waits for user input** or not.
###### ✅ When `flag = True`:
- `getch()` or `getkey()` becomes **non-blocking**
- It returns **immediately** — even if **no key** was pressed.
- If no input is available, it returns:
    - `-1` for `getch()`
    - Raises `curses.error` for `getkey()`
###### ❌ When `flag = False` _(default)_:
- The program **waits** (blocks) until the user presses a key.
  
```python
win.nodelay()
```
---
#####  `timeout(delay) `
This method controls **how long** the program will wait for a key press.
The value you pass changes how `getch()` (or `getkey()`) behaves:
###### ⏸️ If `delay < 0` (negative):
- **Blocking mode** (default)
- The program **waits forever** until the user presses a key.
###### ⚡ If `delay = 0`:
- **Non-blocking mode**
- `getch()` returns **right away**.
- If no key is pressed, it gives back `-1`.
###### ⏱️ If `delay > 0` (positive number):
- **Timed blocking**
- `getch()` waits **up to that many milliseconds**.
- If the user presses a key → it returns it.
- If not → returns `-1` when the time runs out.
  
```python
win.timeout(1000)  # wait 1 second
```
---
#####  `getstr(y,x,n)`
Reads an **entire line of user input** from a specific position on the screen — just like Python’s built-in `input()`, but inside a `curses` window.
###### 🔧 How it works:
- Moves the cursor to position `(y, x)`
- Waits for the user to type
- Accepts up to `n` characters
- Stops reading when the user presses **Enter**
- Returns a **`bytes` object**, not a normal `str`
  
```python
text = win.getstr(1, 2, 20).decode("utf-8")  # Since it returns bytes, we usually use decode() to convert it to a string
```
---
### 4️⃣ `curses.textpad` Module  
The `curses.textpad` module adds higher-level tools to your terminal UI — especially for **text input** and **visual framing**.
It gives you:
- A **`Textbox` class** for creating editable text input areas.
- A **`rectangle()` function** to draw clean borders around boxes or sections.
#### 🧾 `Textbox`
The `Textbox` lets you create a simple text editor inside a window.  
It supports **basic editing**: backspace, arrow keys, word movement, and more — similar to the keybindings in Emacs or other classic editors like BBEdit or Netscape Navigator.

**✅ How to Create One:**
```python 
from curses.textpad import Textbox
box = Textbox(win) # Create the textbox in a window
```
---
**⌨️ Editing Input: ( edit(`[validator]` ) )**
```python
`text = box.edit()
```
- Starts interactive editing (until  Ctrl-G)
- Returns the user’s input as a string 
> **Note** : there is some other commands like Ctrl-G .
 [See more.](https://docs.python.org/3/library/curses.html#curses.textpad.Textbox)

**🧪 `validator` (Optional)**
You can restrict what keys are allowed by passing a **validator function**:
```python
def only_letters(c):
    return c if chr(c).isalpha() else 0

text = box.edit(only_letters)
```
---
**📥 `gather()`**
Return the window contents as a string; whether blanks in the window are included is affected by the `stripspaces` member.
```python
text = box.gather()
```
---
**⚙️ `stripspaces` (Attribute)**
This attribute is a flag which controls the interpretation of blanks in the window.
```python
box.stripspaces = False  # Keep spaces at end of lines
```
- `True` (default): strips trailing blanks
- `False`: preserves all spaces
---
#### `rectangle(win, uly, ulx, lry, lrx)`
Draw a rectangle. The first argument must be a window object; the remaining arguments are coordinates relative to that window. The second and third arguments are the y and x coordinates of the upper left hand corner of the rectangle to be drawn; the fourth and fifth arguments are the y and x coordinates of the lower right hand corner.
```python
from curses.textpad import rectangle

# Upper-left corner of the rectangle at row 2, column 4
# Lower-right corner of the rectangle at row 6, column 30

rectangle(win, 2, 4, 6, 30)#win represent:  window or pad or stdscrn
```
### 5️⃣ Module-Level `curses` Constants and Functions
These are **global functions and constants** provided by the `curses` module.  
They aren't tied to a specific window — instead, they help with **initial setup**, **terminal capabilities**, **colors**, and **input handling**.
#### 🔢 Constants
These constants help you check terminal support and configuration.

| Constant             | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `curses.LINES`       | Number of rows on the screen                             |
| `curses.COLS`        | Number of columns on the screen                          |
| `curses.COLORS`      | Number of colors supported (after `start_color()`)       |
| `curses.COLOR_PAIRS` | Max number of color pairs you can define                 |
| `curses.A_BOLD`      | Attribute for **bold** text                              |
| `curses.A_UNDERLINE` | Attribute for **underlined** text                        |
| `curses.A_REVERSE`   | Invert foreground and background                         |
| `curses.A_DIM`       | Dim text                                                 |
| `curses.A_STANDOUT`  | Highlighted / standout text                              |
| `curses.KEY_*`       | Special key constants (e.g. `KEY_UP`, `KEY_ENTER`, etc.) |
> 📌 **Note:**  
> 1. For a full list of attributes, key codes, and terminal capabilities, see the official Python documentation:  
> 👉 https://docs.python.org/3/library/curses.html#constants
> 2. 📝 You can combine visual attributes using `|`.
   
**example**
```python 
win.addstr(0, 0, "Bold + Underline", curses.A_BOLD | curses.A_UNDERLINE)  
# Writes text at (0, 0) with both bold and underline attributes applied
```
#### 🧩 Functions
##### 🎨 **Color & Styling Functions**
#####  `start_color()`
Must be called if the programmer wants to use colors, and before any other color manipulation routine is called.

`start_color()` initializes eight basic colors (black, red, green, yellow, blue, magenta, cyan, and white), and two global variables in the `curses` module, `COLORS` and `COLOR_PAIRS`, containing the maximum number of colors and color-pairs the terminal can support. It also restores the colors on the terminal to the values they had when the terminal was just turned on.
  
```python
curses.start_color()
```
---
#####  `init_pair(pair_number ,fg, bg)`
  Defines or updates a **color pair** used in text styling.
- `pair_number`: Must be **between 1 and COLOR_PAIRS - 1**  
    (⚠️ pair 0 is reserved: white on black by default) 
- `fg`, `bg`: Foreground and background color codes (0 to COLORS - 1)  

> ✅ If the color pair was already used on-screen, calling this again **updates all text** using it.
  
```python
# 🧶 Define a color pair: pair #1 → RED text on BLACK background
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
```
---
#####  `color_pair()`
  Return the attribute value for displaying text in the specified color pair. Only the first 256 color pairs are supported. This attribute value can be combined with `A_STANDOUT`, `A_REVERSE`, and the other `A_*` attributes.
  
```python
    stdscr.addstr(2, 4, "This is red text!", curses.color_pair(1))
    # or combined with A_BOLD ,A_REVERSE ...
    stdscr.addstr(2, 4, "This is red and bold text!", curses.color_pair(1) | curses.A_BOLD)
```
---
#####  🔔 **Terminal Alerts**
#####  `beep()`
Emit a short attention sound.
  
```python
curses.beep() 
```
---
#####  `flash()`
  Flash the screen. That is, change it to reverse-video and then change it back in a short interval. Some people prefer such as ‘visible bell’ to the audible attention signal produced by `beep()` .
  
```python
curses.flash()
```
---
#####  🎧 **Input Echo Settings**
###### `echo()`
  Enter echo mode. In echo mode, each character input is echoed to the screen as it is entered.
  
```python
curses.echo() 
```
---
#####  `noecho()`
  Leave echo mode. Echoing of input characters is turned off.
  
```python
curses.noecho()
```
---

## 📎 Extra Resources

Here are some helpful links to go further:

- 🧠 [Official Python `curses` documentation](https://docs.python.org/3/library/curses.html)
- 📺 YouTube Tutorial: [Python curses Tutorial](https://youtu.be/Db4oc8qc9RU?si=ex_OVFx_doaI9pex)
- 💻 GitHub Examples: [Python curses example](https://gist.github.com/claymcleod/b670285f334acd56ad1c))

> 📝 These links explain advanced topics like game loops, real-time input, mouse handling, coloring ...
