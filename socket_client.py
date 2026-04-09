"""Basic TCP client example using Python sockets."""

from __future__ import annotations

import socket

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 10


def run_client(host: str = HOST, port: int = PORT) -> None:
    """Connect to the server, send messages, and print responses."""
    try:
        # Create the socket and connect to the server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(TIMEOUT_SECONDS)
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                message = input("Enter a message ('quit' to exit): ").strip()

                if not message:
                    print("Please enter a non-empty message.")
                    continue

                if message.lower() == "quit":
                    print("Closing client connection.")
                    break

                client_socket.sendall(message.encode("utf-8"))
                response = client_socket.recv(BUFFER_SIZE)

                if not response:
                    print("Server closed the connection.")
                    break

                print(f"Server replied: {response.decode('utf-8')}")

    except ConnectionRefusedError:
        print("Connection refused. Start the server before running the client.")
    except TimeoutError:
        print("Connection timed out.")
    except OSError as exc:
        print(f"Socket error: {exc}")


if __name__ == "__main__":
    run_client()
