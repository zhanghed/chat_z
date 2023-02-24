import subprocess
import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]
s.close()


cmd = subprocess.run(["arp", "-a"], capture_output=True,
                     universal_newlines=True)
a = str(cmd).split(",")
b = a[3].replace("stdout='", "").replace("\\n", "\n")
c = b.split("接口:")

for i in c:
    if i.find(str(ip))>0:
        temp=re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',i)
        print(temp)
        