import socket
import threading
import subprocess
import os
import re


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
    # 获取服务ip
    s= os.popen('ipconfig').read()
    ip = re.search(r'以太网:[\d\D]+?IPv4.*?:\s([\d.]*?)\n',s).group(1)

    cmd = subprocess.run(["arp", "-a"], capture_output=True,
                         universal_newlines=True)
    a = str(cmd).split(",")
    b = a[3].replace("stdout='", "").replace("\\n", "\n")
    c = b.split("接口:")

    for i in c:
        if i.find(str(ip)) > 0:
            temp = re.findall(
                r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', i)
            return temp


if __name__ == "__main__":
    # 主线程
    ips = get_ip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in ips:
        try:
            server.connect((i, 9090))
            print(server)
            Send_thread("Send_thread").start()
            Recv_thread("Recv_thread").start()
            break
        except Exception as e:
            print(e)
            continue
