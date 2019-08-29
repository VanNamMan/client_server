import socket
import threading
from libs.utils import *
import time

def client_thread(conn,addr):
    name = ""
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            if "@" in data.decode("utf-8"):
                name = data.decode("utf-8")[1:]
            else:
                msg = bytes(time.strftime("%H:%M:%S ")+name+":\n","utf-8") + data
                for c in conns:
                    if c != conn:
                        c.sendall(msg)
        except:
            conns.remove(conn)
            break

    # conn.close()

HOST = 'localhost' # Thiết lập địa chỉ address
PORT = 8021# Thiết lập post lắng nghe
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cấu hình kết nối
# for p in PORT:
s.bind((HOST, PORT)) # lắng nghe
s.listen(3) # thiết lập tối ta 1 kết nối đồng thời
conns = []
names = []

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    print(conn)
    conns.append(conn)
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    runThread(client_thread, (conn,addr))

s.close() # đóng socket


