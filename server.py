import socket
import queue
import threading
import time
import os
import re


class Send_thread(threading.Thread):  # 发送线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            if not messages.empty():
                data = messages.get_nowait()
                for client in clients:
                    client.send(bytes(str(data).encode('utf-8')))


class Recv_thread(threading.Thread):  # 接收线程
    def __init__(self, name, client):
        threading.Thread.__init__(self, name=name)
        self.client = client

    def run(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                messages.put({"client": self.client, "data": data})
            except Exception as e:
                print(e, self.client)
                self.client.close()
                clients.pop(self.client)
                break


class Connect_thread(threading.Thread):  # 连接线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            client, addr = server.accept()
            if not str(client) in clients:
                recv = Recv_thread("Recv_thread", client)
                recv.start()
                clients[client] = {"client": client, "recv": recv}


def get_server():  # 获取服务
    s = os.popen('ipconfig').read()
    ip = re.search(r'以太网:[\d\D]+?IPv4.*?:\s([\d.]*?)\n', s).group(1)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, 9090))
    server.listen(20)
    print(server)
    return server


if __name__ == "__main__":  # 主线程
    clients = {}
    messages = queue.Queue()
    server = get_server()
    Connect_thread("Connect_thread").start()
    Send_thread("Send_thread").start()
    while True:
        print("客户端：", len(clients), ";",
              "线程：", len(threading.enumerate()), ";",
              threading.enumerate())
        time.sleep(5)
