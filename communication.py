# client.py (Run this on the Mac)
import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the server IP address and port
host = "192.168.137.91"  # Raspberry Pi's IP address
port = 9990

try:
    # Connection to hostname on the port.
    client_socket.connect((host, port))

    # Receive no more than 1024 bytes
    tm = client_socket.recv(1024)
    print(f"The time got from the server is {tm.decode('ascii')}")
finally:
    client_socket.close()
    print("Connection closed.")
