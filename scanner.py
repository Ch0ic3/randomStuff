import socket
import requests
import socks
import threading
import queue
import random
import ipaddress
from ipaddress import ip_address

DEBUG = False

q = queue.Queue()

#generates ips with a start ip and a end one
def ips(start, end):
    '''Return IPs in IPv4 range, inclusive.'''
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]

#gets a banner with the help of making a socket connection and waiting for a resp back
def bannergrab(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((host,port))
    if result == 0:
        banner = s.recv(1024)
        print(banner)

#gens a iplist from a block
def ipblock(host):
    iplist = [str(ip) for ip in ipaddress.IPv4Network(host, False).hosts()]
    return iplist

#generates 100k random ip's to scan
def ip_gen():
    for i in range(100000):
        ip1 = random.randint(1,255)
        ip2 = random.randint(1,255)
        ip3 = random.randint(1, 255)
        ip4 = random.randint(1, 255)
        ip = f"{ip1}.{ip2}.{ip3}.{ip4}"
        iplist.append(ip)
    return iplist

##patching sockets to work with Tor socks5 proxy
socks.set_default_proxy(socks.SOCKS5,"127.0.0.1", 9050)
socket.socket = socks.socksocket

#worker for threads
def worker():
    while q.not_empty:
        host,port = q.get().split(":")
        portscan(host,int(port))
        if DEBUG == True:
            print(host)
        if(q.empty()):
            break

#socket port scan.
def portscan(host,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        conn = sock.connect_ex((host, port))
        if conn == 0:
            if port == 80:
                print(f"Host: {host} open on Port: {port}")
                with open("hosts.txt", "a+") as f:
                    f.write(f"{host}:{port}\n")
                try:
                    host = socket.gethostbyaddr(host)
                    print(host[0])
                except:pass
            else:
                with open("interesting.txt", "a") as f:
                    print(f"Host: {host} open on Port: {port}")
                    f.write(f"{host}:{port}\n")
                    try:
                        print(f"Host:{host} Service: {socket.getservbyport(port)}")
                    except:
                        pass
        try:
            bannergrab(host, port)
        except Exception as err:
            print(err, type(err))

    except socks.SOCKS5Error as err:
        pass
    except TimeoutError:
        pass
    except Exception as err:
        print(err, type(err))

if __name__ == "__main__":
        #Theres 3 methods here to generate an iprange to scan. A little modding is needed on
        #1'st with a start ip and second from a ip netblock using the ipaddress module
        #Third are a "stich" together random ip generation appending to a list
    #for ip in ips(start, end):
        #q.put(ip)
    #for ip in ipblock("2.128.0.0/14"):
        #q.put(ip)
    for i in ip_gen():
        for port in [21,22,23,25,80,8080,8081,135,137,139,445,1433,1434,3306,3389]:
            hostinfo = f"{i}:{port}"
            q.put(hostinfo)
    for i in range(100):
        t = threading.Thread(target=worker)
        t.start()
    for i in range(100):
        t.join()
    
    