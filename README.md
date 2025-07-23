
# 📝 Kast Editor

**Kast Editor** is a lightweight terminal-based text editor built using Python's `curses` library. It offers a simple user interface and basic file editing capabilities directly from your terminal window.

## 🚀 Features

- Simple and clean text interface
- Create or open text files from the terminal
- Basic text navigation: arrow keys, Enter, Backspace
- Prompt to save on exit
- Supports file saving with a prompt if filename is not specified
- Exit using `Ctrl+X`

## 🖥️ Requirements

- Python 3
- A terminal environment (Linux/macOS or WSL on Windows)

## 📦 Installation

No installation is required. Just ensure Python 3 is installed.

```bash
sudo apt install python3
```

Clone or download this script:

```bash
git clone https://github.com/kastx76/curses_basic_CLI_text_editor.git
cd curses_basic_CLI_text_editor
```

## 🧑‍💻 Usage
```bash
chmod +x my_edit.py
```
You can use Kast Editor in two ways:

### 1. Start a new empty buffer:

```bash
./my_edit.py
```

This opens the editor with an empty file. When you exit, you'll be prompted to provide a filename to save.

### 2. Open an existing file:

```bash
./my_edit.py filename.txt
```

This loads the content of the specified file into the editor. You can edit and save it.

### Controls

| Key         | Action                            |
|-------------|-----------------------------------|
| `↑ ↓ ← →`   | Move cursor                       |
| `Backspace` | Delete character                  |
| `Enter`     | Insert new line                   |
| `Ctrl+X`    | Exit and prompt to save changes   |

## 💾 Save on Exit

When you press `Ctrl+X`, you'll be prompted with:

- `Y` to save
- `N` to discard changes and exit 
- `C` to cancel exit

If you choose to save and the file has no name yet, you’ll be asked to enter a filename. If you leave it blank, it defaults to `buffer.txt`.

## ⚠️ Limitations

Kast Editor is intentionally minimal. It has the following limitations:

- ❌ No window resizing support — editor does not handle terminal resizes
- ❌ No syntax highlighting
- ❌ No mouse support
- ❌ No copy-paste support
- ❌ No search or replace
- ❌ No undo/redo
- ❌ No word wrap

It’s ideal for simple editing tasks and learning how terminal-based UIs work in Python.

## 🔮 Possible Improvements

Here are some enhancements that could improve the editor in future versions:

- ✅ Handle terminal resize events
- ✅ Add syntax highlighting
- ✅ Support mouse interactions
- ✅ Add clipboard copy/paste
- ✅ Implement find/replace functionality
- ✅ Provide undo/redo
- ✅ Add word wrapping
- ✅ Support multiple open files or tabs

## 📚 Documentation

Kast Editor was built using Python’s `curses` library.

I created detailed documentation to help others understand how it works, including:
- Window creation and layout
- Pads and scrolling
- Input handling
- Styling and text display

👉 **[Read the full curses documentation here](./curses_documentation.md)**

## 📄 License

MIT License — use it freely for any purpose.

---

Made by Kastx76
