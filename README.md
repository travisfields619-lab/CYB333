# Password Strength Checker

This project is a simple Python-based password strength checker. It evaluates a password entered by the user and labels it as `Weak`, `Moderate`, or `Strong` based on common security rules.

## Project Objectives

The goal of this project is to help users:

- Check whether a password is weak, moderate, or strong
- Understand why a password may be insecure
- Receive suggestions for improving password security

## Features

- Command-line interface for entering passwords
- Strength evaluation based on:
  - Password length
  - Use of uppercase and lowercase letters
  - Use of numbers
  - Use of special characters
  - Detection of common weak passwords
- Helpful feedback and improvement suggestions
- Graceful exit using `Enter`, `Ctrl+C`, or `Ctrl+D`

## File Included

- `password_checker.py` - main password strength checker script

## Prerequisites

- Python 3.10 or later recommended

## Dependencies

This project uses only Python standard library modules:

- `re`

No third-party packages need to be installed.

## How to Set Up

1. Make sure Python is installed on your computer.
2. Open a terminal in the project folder.
3. Verify Python is available:

```bash
python --version
```

## How to Run

Run the script from the terminal:

```bash
python password_checker.py
```

If your system uses `py` on Windows, you can also run:

```powershell
py password_checker.py
```

## How It Works

After running the program:

1. Enter a password when prompted.
2. The program checks the password against several strength rules.
3. It displays:
   - A strength rating
   - Suggestions to make the password stronger
4. Press `Enter` on an empty prompt to exit the program.

## Example

```text
Password Strength Checker
Enter a password to evaluate. Press Enter to quit.
Password: Hello123

Password strength: Moderate
Suggestions:
- Longer passwords (12+ characters) are stronger.
- Add symbols like !, @, #, $, %, or &.
```

## Notes

- Common passwords such as `password` and `123456` are automatically rated poorly.
- Stronger passwords are usually longer and include a mix of letters, numbers, and symbols.
