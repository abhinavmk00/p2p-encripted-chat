import socket
import threading
import sys
import time

class Client(threading.Thread): # Client object is type thread so that it can run simultaniously with the server
    def __init__(self, chatApp): # Initialize with a reference to the Chat App
        super(Client, self).__init__()
        self.chatApp = chatApp
        self.isConnected = False # Connection status

    # Start method called by threading module
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create new socket
        self.socket.settimeout(10)

    def conn(self, args):
        if self.chatApp.nickname == "": # Check if a nickname is set and return False if not
            self.chatApp.sysMsg(self.chatApp.lang['nickNotSet'])
            return False
        host = args[0] # IP of peer
        port = int(args[1]) # Port of peer
        self.chatApp.sysMsg(self.chatApp.lang['connectingToPeer'].format(host, port))
        try: # Try to connect and catch error on fail
            self.socket.connect((host, port))
        except socket.error:
            self.chatApp.sysMsg(self.chatApp.lang['failedConnectingTimeout'])
            return False
        self.socket.send("\b/init {0} {1} {2}".format(self.chatApp.nickname, self.chatApp.hostname, self.chatApp.port).encode()) # Exchange initial information (nickname, key, ip, port)
        self.gen_pem()
        self.send_pem()
        self.chatApp.sysMsg(self.chatApp.lang['connected'])
        self.isConnected = True # Set connection status to true
    
    def gen_pem(self):
        with open ("public.pem","wb") as f:
            f.write(self.chatApp.public_key)

    def send_pem(self):
        file = open("public.pem","rb")
        data = file.read()
        self.socket.sendall(data)
        self.socket.send(b"<END>")
        file.close()
        
    # Method called by Chat App to reset client socket
    def stop(self):
        self.socket.close()
        self.socket = None

    # Method to send data to a peer
    def send(self, msg):
        if msg != '':
            try:
                self.socket.send(msg.encode())
                return True
            except socket.error as error:
                self.chatApp.sysMsg(self.chatApp.lang['failedSentData'])
                self.chatApp.sysMsg(error)
                self.isConnected = False
                return False


    


