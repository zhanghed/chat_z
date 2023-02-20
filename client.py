import socket


def get_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st.connect(('10.255.255.255', 1))
    ip = st.getsockname()[0]
    print(ip)
    st.close()
    return ip


def get_client(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 8000))
    return client


if __name__ == '__main__':
    try:
        ip = get_ip()
        client = get_client(ip)
        print(client)
        while True:
            client_send = input("发送：")
            client.send(client_send.encode('UTF-8'))

            client_recv = client.recv(1024)
            print("接收：",client_recv.decode('UTF-8'))

    except Exception as e:
        print(e)
    client.close()
