import socket
import queue
import threading
import time


class Server_thread(threading.Thread):
    # 服务线程
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), 9090))
        self.server.listen(5)
        print("启动：", self.server)
        # 连接池
        self.clients = {}
        # 消息池
        self.publics = {}

    def run(self):
        while True:
            # 监控连接
            client, addr = self.server.accept()
            if not str(client) in self.clients:
                # 创建接收消息线程
                recv = Recv_thread(
                    name="Recv_thread", client=client,  publics=self.publics)
                recv.start()
                # 加入连接池
                self.clients[client] = {"client": client,
                                        "addr": addr,
                                        "ip": client.getpeername()[0],
                                        "recv": recv}
                print("接入：", self.clients[client])
            time.sleep(1)


class Recv_thread(threading.Thread):
    # 接收消息线程
    def __init__(self, name,  client, publics):
        threading.Thread.__init__(self, name=name)
        self.client = client
        self.publics = publics

    def run(self):
        while True:
            # 创建消息队列
            public=self.publics[self.client] = queue.Queue()
            data=self.client.recv(1024).decode('utf-8')
            # 加入消息池
            print(data)
            public.put(data)
            time.sleep(1)


server = Server_thread(name="Server_thread")
server.start()

while True:
    # print("clients", len(server.clients), "publics", len(server.publics))
    # print(len(threading.enumerate()), threading.enumerate())
    # for k,v in server.publics.items():
    #     print(k,v)

    time.sleep(5)

# # 转发消息(非/阻塞)
# def broadcast():
#     while True:
#         if len(clients) > 1:
#             public_message_clone = [
#                 i for i in public_message]  # 解决字典迭代中操作报错的问题
#             for client in clients:
#                 for i in public_message_clone:
#                     if i != client and public_message[i].empty() == False:
#                         data = public_message[i].get_nowait()  # 注意
#                         if data != '':
#                             client.send(bytes(data.encode('utf-8')))
#                             print('服务器转发了消息')
