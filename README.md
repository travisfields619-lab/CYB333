# Tkinter App

A simple desktop GUI built with Python's `tkinter` library.

The app opens a small window with:

- An input box for typing text
- A button to submit the text
- A result area that displays the submitted value on screen

## File

- `tkinter_app.py` - the main GUI application

## How It Works

When you type text into the input field and click `Show Result`, the window updates the label below the button.

- If text is entered, the app shows: `You entered: <your text>`
- If the input is empty, the app shows: `Please enter some text.`

## Run The App

Use your local Python interpreter to start the program:

```bash
python tkinter_app.py
```

If `python` is not on your PATH in Windows, use the interpreter you normally run from VS Code, for example:

```powershell
C:/path/to/python.exe tkinter_app.py
```

## Requirements

- Python 3.x
- `tkinter` available in your Python installation

## Example

1. Launch the app
2. Type `Hello`
3. Click `Show Result`
4. The window displays `You entered: Hello`

## Other Files In This Workspace

This workspace also contains a few separate Python utilities such as:

- `vulnerability_scanner.py`
- `port_scanner.py`
- `password_checker.py`
- `socket_client.py`
- `socket_server.py`

Those scripts are independent from the Tkinter app.
