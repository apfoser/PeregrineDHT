import socket
import pickle


class Message:
    
    '''
    Message Body Format,
    {
        "type" : one of ["test", "ping", "pong", "broadcast"]
        "data" : depends on type (data protocol in progress)
    }
    '''
    def __init__(self, sender: str, body: str):
        self.sender = sender
        self.body = body
        
        
class Contact:
    
    def __init__(self, ip: str, port: int, sockfd: socket = None):
        self.ip = ip
        self.port = port
        self.sockfd = sockfd
    
    # send serialized message back to client using server.socket
    def send_message(self, sock,  message):
        
        data = pickle.dumps(message)

        # If 0 is returned, 0 bytes are sent
        if (sock.sendto(data, (self.ip, self.port)) == 0):
            print("Error transmitting message")

    def send_pong(self, sock, sender):
        
        body = {
            "type" : "pong",
            "data" : ""
        }
        
        m = Message(sender,body)
        self.send_message(sock, m)
        
    def send_ping(self, sock, sender):
        
        body = {
            "type" : "ping",
            "data" : ""
        }
        
        m = Message(sender, body)
        self.send_message(sock, m)