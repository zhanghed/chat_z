import socket,threading
#客户端想要发消息和收消息同时进行,需要使用多线程达到并发效果

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
s.connect((host, 9090))


def receive():
    while True:
        data = s.recv(1024).decode('utf-8')
        if data!='':
            print(data)
     
    
def send_msg():
    while (True):
        msg = input(':')
        if msg=='exit':
            s.close()
            break
        s.send(bytes(msg.encode('utf-8')))
        
t1 = threading.Thread(target=receive,daemon=True)
t1.start()

send_msg()
