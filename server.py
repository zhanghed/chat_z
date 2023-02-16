import socket

def get_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st.connect(('10.255.255.255', 1))
    ip = st.getsockname()[0]
    st.close()
    return ip


def get_server(ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, 8000))
    server.listen(2)
    return server


if __name__ == '__main__':
    try:
        ip = get_ip()
        server = get_server(ip)
        print(server)
        client, client_Addr = server.accept()
        while True:
            client_recv = client.recv(1024)
            print("接收：", client_recv.decode('UTF-8'))

            client_send = input("发送：")
            client.send(client_send.encode('UTF-8'))

    except Exception as e:
        print(e)
    client.close()
