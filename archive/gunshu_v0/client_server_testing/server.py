import time
import socket
import threading

HOST_IP_ADDRESS = "127.0.0.1"
PORT = 65432

client_counter = 0
active_clients = 0


def handle_client(conn, addr, client_id, server_socket):
    """
    Handle communication with a single client.
    """

    global active_clients

    print(f"Connected by {addr}")

    welcome_message = f"Client {client_id} joined!"
    conn.sendall(welcome_message.encode())  # send welcome message to the client

    while True:

        data = conn.recv(1024)  # receive data from the client
        if not data:  # exit if no data is received
            break

        message = data.decode()
        print(
            f"Received message from Client {client_id} with address {addr}: {message}"
        )

        if message.lower() == ":q":  # exit loop if client types :q
            print(
                f"Client {client_id} with address {addr} requested to quit. Closing connection."
            )
            break

        response = f"Message received from Client {client_id}"

        conn.sendall(response.encode())  # send acknowledgment to the client

    print(f"Closing connection with {addr}.")
    conn.close()  # close the connection with the client

    active_clients -= 1  # decrement active clients when one disconnects

    if active_clients == 0:
        print("No more active clients. Server is shutting down.")
        server_socket.close()  # close the server socket to stop accepting new connections


def start_server():
    """
    Start the server with multi-threading, each client being handled on a separate thread.
    Server will shut down when all clients disconnect.
    """

    global client_counter
    global active_clients

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )  # set socket option to allow address reuse
    server_socket.bind((HOST_IP_ADDRESS, PORT))
    server_socket.listen(6)  # allow up to 6 clients to connect simultaneously

    print(f"Server started on {HOST_IP_ADDRESS}:{PORT}... Waiting for connections.")

    while True:

        conn, addr = server_socket.accept()  # accept client connection
        client_counter += 1  # increment client ID counter
        client_id = client_counter

        active_clients += 1  # increment active clients count when a client connects

        client_thread = threading.Thread(
            target=handle_client, args=(conn, addr, client_id, server_socket)
        )  # start a new thread to handle the client
        client_thread.start()  # start the new thread

        time.sleep(1)  # sleep for a brief moment before checking again


if __name__ == "__main__":
    start_server()
