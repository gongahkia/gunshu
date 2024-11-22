# REVAMP ALL THIS SERVER CODE TO INTEGRATE WITH THE EXISTING DISPLAY

import socket
import threading
import json

HOST_IP_ADDRESS = "127.0.0.1"
PORT = 65432

PLAYER_STARTING_POSTITION = {"x": 100, "y": 100}

clients = {}
lock = threading.Lock()


def handle_client(conn, addr, client_id, server_socket):
    """
    handle a single client and receive the input, then broadcasting the updated positions
    """

    global clients

    print(f"Client {client_id} connected from {addr}.")

    with lock:
        clients[client_id] = PLAYER_STARTING_POSTITION

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode()
            if message.lower() == ":q":
                print(f"Client {client_id} requested to quit.")
                break

            input_data = json.loads(message)
            with lock:
                clients[client_id]["x"] += input_data["dx"]
                clients[client_id]["y"] += input_data["dy"]

            with lock:
                positions = json.dumps(clients)
            conn.sendall(positions.encode())

    except Exception as e:
        print(f"Error handling client {client_id}: {e}")
    finally:
        with lock:
            del clients[client_id]
        print(f"Client {client_id} disconnected.")
        conn.close()


def start_server():
    """
    start the server to manage clients
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST_IP_ADDRESS, PORT))
    server_socket.listen(6)
    print(f"Server started on {HOST_IP_ADDRESS}:{PORT}...")
    client_counter = 0
    try:
        while True:
            conn, addr = server_socket.accept()
            client_counter += 1
            threading.Thread(
                target=handle_client, args=(conn, addr, client_counter, server_socket)
            ).start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
