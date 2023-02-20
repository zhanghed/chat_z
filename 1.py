import socket
import queue
import threading
import time


# 存放已连接的对象
clients = []
# 存放公共消息的容器
public_message = dict()


class Server_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), 9090))
        self.server.listen(5)
        print(self.server)
        self.clients = {}

    def run(self):
        while True:
            client, addr = self.server.accept()
            if not str(client) in self.clients:
                self.clients[client] = {"client": client,
                                        "addr": addr,
                                        "ip": client.getpeername()[0]}
            threading.Thread(target=recv_thread, args=(client,)).start()
            time.sleep(1)


class Recv_thread(threading.Thread):
    def __init__(self,client,name):
        threading.Thread.__init__(self, name=name)
        
    def run(self):
        while True:
            if client in clients:
                data = client.recv(1024).decode('utf-8')
                if data != '':
                    print(data)
                    public_message[client] = queue.Queue()
                    public_message[client].put(data)
                else:
                    if client in clients:
                        print("用户优雅的退出了")
                        clients.remove(client)
            time.sleep(1)


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


Server_thread(name="Server_thread").start()
# t2 = threading.Thread(target=broadcast)

# t2.start()

# 主线程监听在线人数
while (True):
    print("当前在线人数为:%d" % (len(clients)))
    time.sleep(5)
