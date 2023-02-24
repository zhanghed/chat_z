import socket
import threading
import time


class Send_thread(threading.Thread):
    # 发送线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            msg = input(':')
            if msg == 'exit':
                server.close()
                break
            server.send(bytes(msg.encode('utf-8')))


class Recv_thread(threading.Thread):
    # 接收线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            data = server.recv(1024).decode('utf-8')
            if data != '':
                print(data)


def get_ip():
    # 获取本机ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # 主线程
    ip = get_ip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, 9090))
    print(server)
    Send_thread("Send_thread").start()
    Recv_thread("Recv_thread").start()
