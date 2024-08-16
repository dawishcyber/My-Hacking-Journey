import socket

def main():
    # Prompt for server IP and port
    server_ip = input("Enter server IP address to bind to (or 0.0.0.0 for all interfaces): ")
    server_port = int(input("Enter server port: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        conn, addr = server_socket.accept()
        print("Connection from:", addr)
        data = conn.recv(1024).decode("utf-8")
        with open("received_logs.txt", "a") as file:
            file.write(data)
        conn.close()

if __name__ == "__main__":
    main()

