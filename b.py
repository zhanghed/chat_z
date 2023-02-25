import ipaddress
import socket

# ['192.168.192.1', '192.168.101.1', '192.168.0.13',"192.1.4.245"]

import os
import re


str_ = os.popen('ipconfig').read()
print(str_)
this_ip = re.search(r'以太网:[\d\D]+?IPv4.*?:\s([\d.]*?)\n',str_).group(1)
print('ip:',this_ip)