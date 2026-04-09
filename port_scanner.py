"""Simple TCP port scanner for localhost or approved test hosts."""

from __future__ import annotations

import argparse
import errno
import select
import socket
import sys
import time
from typing import Dict, List, Tuple

DEFAULT_TIMEOUT = 0.5
MIN_PORT = 1
MAX_PORT = 65535

# Common socket error codes seen on Windows/Linux during scans.
CLOSED_CODES = {getattr(errno, "ECONNREFUSED", 111), 10061}
TIMEOUT_CODES = {getattr(errno, "ETIMEDOUT", 110), 10060}
UNREACHABLE_CODES = {
    getattr(errno, "EHOSTUNREACH", 113),
    getattr(errno, "ENETUNREACH", 101),
    10051,
    10065,
}


def validate_port_range(start_port: int, end_port: int) -> None:
    """Ensure the supplied port range is valid before scanning."""
    if start_port < MIN_PORT or start_port > MAX_PORT or end_port < MIN_PORT or end_port > MAX_PORT:
        raise ValueError(f"Ports must be between {MIN_PORT} and {MAX_PORT}.")
    if start_port > end_port:
        raise ValueError("The start port must be less than or equal to the end port.")


def validate_timeout(timeout: float) -> None:
    """Ensure the socket timeout is a positive number."""
    if timeout <= 0:
        raise ValueError("Timeout must be greater than 0 seconds.")


def resolve_target(host: str) -> str:
    """Resolve a hostname to an IPv4 address and report clear errors."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host '{host}': {exc}") from exc


def scan_port(host: str, port: int, timeout: float) -> Tuple[str, int]:
    """Return a human-readable TCP port status and the associated result code."""
    try:
        # Use a non-blocking connect and wait up to the requested timeout.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            initial_result = sock.connect_ex((host, port))
            if initial_result == 0:
                return "OPEN", 0

            _, writable, exceptional = select.select([], [sock], [sock], timeout)
            if not writable and not exceptional:
                return "CLOSED/FILTERED", getattr(errno, "ETIMEDOUT", 110)

            error_code = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
    except OSError as exc:
        error_code = exc.errno or -1
        if error_code in CLOSED_CODES:
            return "CLOSED", error_code
        if error_code in TIMEOUT_CODES:
            return "CLOSED/FILTERED", error_code
        if error_code in UNREACHABLE_CODES:
            return "UNREACHABLE", error_code
        return "ERROR", error_code

    if error_code == 0:
        return "OPEN", 0
    if error_code in CLOSED_CODES:
        return "CLOSED", error_code
    if error_code in TIMEOUT_CODES:
        return "CLOSED/FILTERED", error_code
    if error_code in UNREACHABLE_CODES:
        return "UNREACHABLE", error_code
    return "ERROR", error_code


def scan_ports(host: str, start_port: int, end_port: int, timeout: float = DEFAULT_TIMEOUT) -> List[int]:
    """Scan a range of TCP ports and return the list of open ones."""
    validate_port_range(start_port, end_port)
    validate_timeout(timeout)
    resolved_ip = resolve_target(host)

    started_at = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scan started: {started_at}")
    print(f"Scanning {host} ({resolved_ip}) from port {start_port} to {end_port}...")

    start_time = time.time()
    open_ports: List[int] = []
    status_counts: Dict[str, int] = {
        "OPEN": 0,
        "CLOSED": 0,
        "CLOSED/FILTERED": 0,
        "UNREACHABLE": 0,
        "ERROR": 0,
    }

    for port in range(start_port, end_port + 1):
        status, code = scan_port(resolved_ip, port, timeout)
        print(f"[{status}] Port {port} (result code: {code})")
        status_counts[status] = status_counts.get(status, 0) + 1

        if status == "OPEN":
            open_ports.append(port)

    elapsed = time.time() - start_time
    finished_at = time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nScan finished: {finished_at}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print("Summary:")
    for status, count in status_counts.items():
        print(f" - {status}: {count}")

    if open_ports:
        print("Open ports found:", ", ".join(str(port) for port in open_ports))
    else:
        print("No open ports were found in the requested range.")

    if not open_ports and status_counts["UNREACHABLE"] + status_counts["CLOSED/FILTERED"] == (end_port - start_port + 1):
        print("Warning: the target did not accept any connections; ports may be closed, filtered, or the host may be unreachable.")

    return open_ports


def build_parser() -> argparse.ArgumentParser:
    """Create a small command-line interface for the scanner."""
    parser = argparse.ArgumentParser(
        description="Scan a range of TCP ports on a target host."
    )
    parser.add_argument("host", help="Hostname or IP address to scan, such as 127.0.0.1 or scanme.nmap.org")
    parser.add_argument("start_port", type=int, help="First port in the range")
    parser.add_argument("end_port", type=int, help="Last port in the range")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Socket timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    return parser


def main() -> int:
    """Parse arguments, run the scan, and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        scan_ports(args.host, args.start_port, args.end_port, args.timeout)
        return 0
    except ValueError as exc:
        print(f"Input error: {exc}")
        return 1
    except KeyboardInterrupt:
        print("\nScan cancelled by user.")
        return 130
    except Exception as exc:  # Defensive catch for unexpected runtime errors.
        print(f"Unexpected error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
