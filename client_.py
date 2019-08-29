import socket
import argparse

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.utils import *

import time


class myServer(QMainWindow):
    def __init__(self,parent=None):
        super(myServer,self).__init__(parent)

        self.bConnect = False
        self.client = None

        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.statusBar =  QStatusBar(self)
        self.setStatusBar(self.statusBar)

        layout = QGridLayout(widget)

        # self.list_client = QListWidget(self)
        # self.list_client.addItem("client")
        self.box_chat = QListWidget(self)

        chat = QLabel("Chat ",self)
        self.line = QLineEdit(self)
        self.line.setFocus(Qt.FocusReason())

        host = QLabel("Host",self)
        port = QLabel("Port",self)
        user = QLabel("User",self)
        self.host = QLineEdit("localhost",self)
        self.port = QLineEdit("8003",self)
        self.user = QLineEdit("user",self)
        self.but_connect = QToolButton(self)
        self.action_connect = newAction(self,"Connect",slot=self.connect,icon="power.png")
        self.action_disconnect = newAction(self,"Disconnect",slot=self.disconnect,icon="off.png")
        self.but_connect.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.but_connect.setDefaultAction(self.action_connect)
        self.but_connect.setToolTip("Connect")

        # layout.addWidget(self.list_client,0,0,1,5)
        layout.addWidget(self.box_chat,1,0,1,6)
        layout.addWidget(chat,2,0)
        layout.addWidget(self.line,2,1,1,5)

        layout.addWidget(host,0,0)
        layout.addWidget(port,0,2)
        layout.addWidget(user,0,4)
        layout.addWidget(self.host,0,1)
        layout.addWidget(self.port,0,3)
        layout.addWidget(self.user,0,5)
        layout.addWidget(self.but_connect,0,6)

        widget.setLayout(layout)

    def loopChat(self,s):
        while self.bConnect:
            data = s.recv(1024) # Đọc dữ liệu server trả về
            strdata = data.decode("utf-8")
            self.box_chat.addItem(strdata)
            # print("Maybe disconnect to Server")
              # s.close()

    def connect(self):
        HOST = self.host.text()
        PORT = self.port.text()
        if PORT == "" or PORT == "":
            return
        PORT = int(PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cấu hình socket
        # tiến hành kết nối đến server
        try:
            self.client.connect((HOST, PORT))
            self.bConnect = True
            dt = "@"+self.user.text()
            self.client.sendall(bytes(dt, 'utf-8'))
            self.statusBar.showMessage("Connected")
            runThread(target=self.loopChat,args=(self.client,))
        except:
            self.bConnect = False
        
        self.but_connect.setDefaultAction(self.action_disconnect)
        self.but_connect.setToolTip("Connect")

    def disconnect(self):
        try:
            self.client.close()
            self.bConnect = False
            self.statusBar.showMessage("Disconnect")
            self.but_connect.setDefaultAction(self.action_connect)
            self.but_connect.setToolTip("Connect")
        except:
            print("Err when close client")

    def keyPressEvent(self,ev):
        if ev.key() == Qt.Key_Return:
            dt = self.line.text()
            self.box_chat.addItem(time.strftime("%H:%M:%S ")+"me : \n"+dt)
            self.client.sendall(bytes(dt, 'utf-8')) # Gửi dữ liệu lên server 

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    server = myServer()
    server.show()
    app.exec_()
