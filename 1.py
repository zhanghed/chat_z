import socket
import queue
import threading
import time


class Server_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), 9090))
        self.server.listen(5)
        self.clients = {}
        self.messages = queue.Queue()
        self.send = Send_thread("Send_thread", self.clients,  self.messages)
        self.send.start()

    def run(self):
        while True:
            client, addr = self.server.accept()
            if not str(client) in self.clients:
                recv = Recv_thread("Recv_thread", client,  self.messages)
                recv.start()
                self.clients[client] = {"client": client,
                                        "addr": addr,
                                        "ip": client.getpeername()[0],
                                        "recv": recv}
            time.sleep(1)


class Send_thread(threading.Thread):
    def __init__(self, name,  clients, messages):
        threading.Thread.__init__(self, name=name)
        self.clients = clients
        self.messages = messages

    def run(self):
        while True:
            if not self.messages.empty():
                data = server.messages.get_nowait()
                for client in self.clients:
                    client.send(bytes(str(data).encode('utf-8')))
            time.sleep(1)

class Recv_thread(threading.Thread):
    def __init__(self, name,  client, messages):
        threading.Thread.__init__(self, name=name)
        self.client = client
        self.messages = messages

    def run(self):
        while True:
            data = self.client.recv(1024).decode('utf-8')
            self.messages.put({"client": self.client,
                              "data": data})
            time.sleep(1)


server = Server_thread("Server_thread")
server.start()

n = 1
while True:
    print(
        "--", n, ";",
        "线程:", len(threading.enumerate()), ";"
        "客户端:", len(server.clients), ";"
    )
    # if server.clients:
    #     if not server.messages.empty():
    #         a = server.messages.get_nowait()
    #         print(a)
    n = n+1
    time.sleep(5)
