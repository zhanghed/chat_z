import socket

def get_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), 8000))
    server.listen(2)
    return server


if __name__ == '__main__':
    try:
        server = get_server()
        print(server)
        client, client_Addr = server.accept()
        while True:
            client_recv = client.recv(1024)
            print("接收：", client_recv.decode('UTF-8'))

            # client_send = input("发送：")
            # client.send(client_send.encode('UTF-8'))

    except Exception as e:
        print(e)
    client.close()
