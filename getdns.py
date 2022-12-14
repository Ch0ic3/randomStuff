import socket

with open("hosts.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        host,port = line.split(":")
        line = line.strip("\n")
        try:
            name = socket.gethostbyaddr(host)
            print(name)
        except:pass