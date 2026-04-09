"""Basic TCP server example using Python sockets."""

from __future__ import annotations

import socket

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def handle_client(connection: socket.socket, address: tuple[str, int]) -> None:
    """Receive data from one client and send back a response."""
    print(f"Connected by {address[0]}:{address[1]}")

    with connection:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                print("Client disconnected.")
                break

            message = data.decode("utf-8")
            print(f"Received: {message}")

            response = f"Server received: {message}"
            connection.sendall(response.encode("utf-8"))


def run_server(host: str = HOST, port: int = PORT) -> None:
    """Start the socket server and listen for incoming connections."""
    try:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen()

            print(f"Server listening on {host}:{port}")
            print("Press Ctrl+C to stop the server.\n")

            while True:
                connection, address = server_socket.accept()
                handle_client(connection, address)

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except OSError as exc:
        print(f"Socket error: {exc}")


if __name__ == "__main__":
    run_server()
