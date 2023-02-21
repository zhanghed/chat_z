import socket
import queue
import threading
import time


class Send_thread(threading.Thread):
    # 发送线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        while True:
            if not messages.empty():
                data = messages.get_nowait()
                for client in clients:
                    client.send(bytes(str(data).encode('utf-8')))
            time.sleep(1)


class Recv_thread(threading.Thread):
    # 接收线程
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
            time.sleep(1)


class State_thread(threading.Thread):
    # 状态线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.n = 1

    def run(self):
        while True:
            print("***", self.n,
                  "客户端：", len(clients),
                  "线程：", len(threading.enumerate()),
                  threading.enumerate())
            self.n = self.n+1
            time.sleep(5)


def get_ip():
    temp = socket.gethostbyname_ex(socket.gethostname())[2]
    arr = [i for i in temp]
    print(arr)


if __name__ == "__main__":
    # 主线程
    ip = get_ip()
    clients = {}
    messages = queue.Queue()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ip, 9090)
    server.listen(10)
    print(server)
    Send_thread("Send_thread").start()
    State_thread("State_thread").start()
    while True:
        client, addr = server.accept()
        if not str(client) in clients:
            recv = Recv_thread("Recv_thread", client)
            recv.start()
            clients[client] = {"client": client, "recv": recv}
        time.sleep(1)
