# Vulnerability Scanner

A simple Python vulnerability scanner that analyzes Python code for common security vulnerabilities.

## Features

- Detects use of dangerous functions like `eval`, `exec`, `os.system`, `pickle.loads`, etc.
- Checks for command injection vulnerabilities in subprocess calls with `shell=True`.
- Uses AST parsing for accurate analysis without executing the code.

## Usage

### As a script

```bash
python vulnerability_scanner.py [file_path]
```

If no file_path is provided, it runs a test scan on sample vulnerable code.

### As a module

```python
from vulnerability_scanner import scan_code, scan_file

# Scan code string
vulnerabilities = scan_code("import os; os.system('ls')")
print(vulnerabilities)

# Scan file
vulnerabilities = scan_file("example.py")
print(vulnerabilities)
```

## Detected Vulnerabilities

- Code execution: `eval`, `exec`
- Command injection: `os.system`, `subprocess` calls with `shell=True`
- Insecure deserialization: `pickle.loads`, `pickle.load`

## Requirements

- Python 3.6+
- Standard library only (uses `ast`)

## Limitations

- Static analysis only; may have false positives/negatives
- Does not detect all possible vulnerabilities (e.g., SQL injection, XSS)
- Only analyzes Python code

## Troubleshooting

- Ensure the file is valid Python code
- For large files, parsing may take time
- Syntax errors in code will be reported

---

## Port Scanner Demonstration (`port_scanner.py`)

A TCP port scanner is included in `port_scanner.py`. Each run prints `Scan started` and `Scan finished` timestamps so your terminal screenshots automatically include verification time.

### Demo setup

1. Start the local test server in **Terminal 1**:

   ```powershell
   C:/Users/travi/anaconda3/envs/vscode-env/python.exe socket_server.py
   ```

2. Run the scanner commands in **Terminal 2** using the examples below.

### Screenshot checklist

| Requirement | Command | Verified result |
| --- | --- | --- |
| Common localhost ports | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py 127.0.0.1 21 23 --timeout 0.2` plus `80 80` and `443 443` | Ports were reported as `CLOSED/FILTERED` |
| Custom localhost range | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py 127.0.0.1 65430 65435 --timeout 0.2` | Port `65432` was `OPEN` |
| `scanme.nmap.org` selected ports | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py scanme.nmap.org 79 81 --timeout 0.5` and `22 22 --timeout 0.5` | Ports `80` and `22` were `OPEN` |
| Invalid port numbers | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py 127.0.0.1 0 80 --timeout 0.2` | `Input error: Ports must be between 1 and 65535.` |
| Unreachable / unresolvable host | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py no-such-host.invalid 80 81 --timeout 0.2` | `Input error: Could not resolve host ...` |
| Performance comparison | `C:/Users/travi/anaconda3/envs/vscode-env/python.exe port_scanner.py 127.0.0.1 1 10 --timeout 0.1` and `1 50 --timeout 0.1` | ~`1.06s` vs ~`5.38s` |

> On this Windows setup, non-open ports often appear as `CLOSED/FILTERED` instead of a pure `CLOSED` state because the connection timed out rather than returning an immediate refusal.

### Verified output excerpts (captured on 2026-04-09)

```text
=== Localhost custom range ===
Scan started: 2026-04-09 11:34:18
Scanning 127.0.0.1 (127.0.0.1) from port 65430 to 65435...
[CLOSED/FILTERED] Port 65430 (result code: 10060)
[OPEN] Port 65432 (result code: 0)
[CLOSED/FILTERED] Port 65435 (result code: 10060)
Open ports found: 65432

=== scanme.nmap.org ===
Scan started: 2026-04-09 11:34:20
Scanning scanme.nmap.org (45.33.32.156) from port 79 to 81...
[CLOSED/FILTERED] Port 79 (result code: 10060)
[OPEN] Port 80 (result code: 0)
[CLOSED/FILTERED] Port 81 (result code: 10060)
Open ports found: 80

Scan started: 2026-04-09 11:34:21
Scanning scanme.nmap.org (45.33.32.156) from port 22 to 22...
[OPEN] Port 22 (result code: 0)
Open ports found: 22

=== Error handling ===
Input error: Ports must be between 1 and 65535.
Input error: Could not resolve host 'no-such-host.invalid': [Errno 11001] getaddrinfo failed

=== Performance comparison ===
1-10 range elapsed time: 1.06 seconds
1-50 range elapsed time: 5.38 seconds
```

Use these commands in the integrated terminal and capture screenshots for each row in the checklist above.
