import socket

class Contact:
    
    def __init__(self, ip: str, port: int, sockfd: socket = None):
        self.ip = ip
        self.port = port
        self.sockfd = sockfd
        
    def send_message(self):
        pass
