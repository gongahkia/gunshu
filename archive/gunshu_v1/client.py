import socket

HOST_IP_ADDRESS = "127.0.0.1"
PORT = 65432

try:
    client_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # create and connect client socket
    client_socket.connect((HOST_IP_ADDRESS, PORT))  # connect to the server

    print(f"Connected to server at {HOST_IP_ADDRESS}:{PORT}")

    while True:
        message = input("Enter a message (or type ':q' to exit): ")
        client_socket.sendall(message.encode())  # send the message to the server

        if message.lower() == ":q":  # exit the client-side if user types :q
            print("Closing connection.")
            break

        data = client_socket.recv(1024)  # receive the response from the server
        print(f"Received from server: {data.decode()}")

except ConnectionError:
    print("Failed to connect to the server. Please try again later.")

finally:
    client_socket.close()
    print("Disconnected from server.")
