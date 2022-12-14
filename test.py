import socket

with open("interesting.txt", "r") as f:
    for line in f.readlines():
        host,port = line.split(":")
        print(port)
        service = socket.getservbyport(int(port))
        print(service)