import socket


def GetLocalIPByPrefix():

    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        print(ip)



GetLocalIPByPrefix()
