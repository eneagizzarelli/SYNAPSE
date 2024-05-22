import socket

if __name__ == "__main__":
    mysql_interceptor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysql_interceptor_socket.bind('0.0.0.0', 3307)
    mysql_interceptor_socket.listen(5)

    print(f'Server listening on 0.0.0.0:3307')

    while True:
        client_socket, client_address = mysql_interceptor_socket.accept()
        print(f'Connection from {client_address}')
        client_socket.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
        client_socket.sendall(b'You have connected to a fake MySQL server!\r\n')
        client_socket.close()
