import socket
import pickle


class Message:
    
    '''
    Message Body Format,
    {
        "type" : one of ["test", "ping", "pong", "broadcast"]
        "data" : depends on type (data protocol in progress)
        "rpc_id" : id of procedure call by other node
        "key" : key for distance calculations
    }
    '''
    def __init__(self, sender: str, body: str):
        self.sender = sender
        self.body = body
        
        
class Contact:
    
    def __init__(self, ip: str, port: int, id):
        self.ip = ip
        self.port = port
        self.id = id
        
    # revise when ID stuff is figured out
    def astriple(self):
        return (self.ip, self.port, self.id)
    
    # send serialized message back to client using server.socket
    def send_message(self, sock,  message):
        
        data = pickle.dumps(message)

        # If 0 is returned, 0 bytes are sent
        if (sock.sendto(data, (self.ip, self.port)) == 0):
            print("Error transmitting message")

    def send_ping(self, sock, sender):
        
        body = {
            "type" : "ping",
            "data" : ""
        }
        
        m = Message(sender, body)
        self.send_message(sock, m)

    def send_pong(self, sock, sender):
        
        body = {
            "type" : "pong",
            "data" : ""
        }
        
        m = Message(sender,body)
        self.send_message(sock, m)
        
    def send_store(self, sock, sender, data):
        
        body = {
            "type" : "store",
            "data" : data
        }
        
        m = Message(sender,body)
        self.send_message(sock, m)
        
    def find_nodes(self, sock, sender, rpc_id, key):
        
        body = {
            "type" : "find_nodes",
            "data" : "",
            "rpc_id" : rpc_id,
            "key" : key
        }
        
        m = Message(sender,body)
        self.send_message(sock, m)
        
    def found_nodes(self, sock, sender, data, rpc_id, key):
        
        body = {
            "type" : "found_nodes",
            "data" : data,
            "rpc_id" : rpc_id,
            "key" : key
        }
        
        m = Message(sender,body)
        self.send_message(sock, m)
        