import socket
import queue
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
ip = socket.gethostbyname(socket.gethostname())
print(ip)
server.bind((ip, 9090))
server.listen(5)

#存放已连接的对象
clients = []
#存放公共消息的容器
public_message = dict()

#接收新的对象
def init():
    while True:    
        client,addr = server.accept()  #阻塞线程
        if client in clients:
            print('老用户')
        else:
            print('新的用户加入:',end='')
            print(client.getpeername()[0])
            client.send(bytes('欢迎来到聊天室(匿名)!'.encode('utf-8')))
            clients.append(client)
            r = threading.Thread(target=receive_msg,args=(client,))
            r.start()
        

#接收消息
def receive_msg(client):
    while True:
        time.sleep(1)
        try:
            if client in clients:
                data = client.recv(1024).decode('utf-8')
                if data!='':
                    print(data)
                    public_message[client] = queue.Queue()
                    public_message[client].put(data)
                else:
                    if client in clients:
                        print("用户优雅的退出了")
                        clients.remove(client)
           
        except BaseException as error:

            print('用户强制中断了一个连接')
            # print('错误:',error)
            if client in clients:
                clients.remove(client)


#转发消息(非/阻塞)
def broadcast():
    while True:
        if len(clients)>1:
            public_message_clone = [i for i in public_message]   #解决字典迭代中操作报错的问题
            for client in clients:
                for i in public_message_clone:
                    if i!=client and public_message[i].empty()==False:
                        data = public_message[i].get_nowait()  #注意
                        if data !='':
                            client.send(bytes(data.encode('utf-8')))
                            print('服务器转发了消息')
         
                    
t1 = threading.Thread(target=init)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()


#主线程监听在线人数
while (True):
    print("当前在线人数为:%d"%(len(clients)))
    time.sleep(5)


