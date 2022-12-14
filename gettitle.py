import requests
from bs4 import BeautifulSoup
import queue
import threading
import socket
import socks
import ipaddress
from robot import get_robots

socks.set_default_proxy(socks.SOCKS5,"127.0.0.1", 9050)
socket.socket = socks.socksocket

q = queue.Queue()

def checkrobot(host):
    try:
        host = f"http://{host}"
        r = requests.get(f"{host}/robots.txt", timeout=2)
        print(r.status_code)
        if r.status_code < 300:
            print(host)
            get_robots(host)
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:pass
    except KeyError:
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find(title)
        print(host)
        print("\n")
    except TypeError:
        pass

def worker():
    while (q.not_empty):
        host = q.get()
        scan(host)
        if (q.empty()):
            break
        
def ipblock(host):
    iplist = [str(ip) for ip in ipaddress.IPv4Network(host, False).hosts()]
    return iplist

def scan(host):
    try:
        requests.Timeout(2)
        r = requests.get(f"http://{host}", timeout=4)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("title")
        url = soup.find("meta",  {"property":"og:url"})
        print ( f"server: {r.headers['server']} host: {host}")
        print(title)
        checkrobot(host)
        if len(title) > 100:
            with open("error.log","a") as a:
                a.write(title)
        else:print(title)
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:pass
    except KeyError:
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find(title)
        print(host)
        print("\n")
    except TypeError:
        pass



def readhost():
    with open("hosts.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            host,port = line.split(":")
            q.put(host)

if __name__ == "__main__":
    readhost()
    for i in range(10):
        t = threading.Thread(target=worker)
        t.start()
    for i in range(10):
        t.join()
        