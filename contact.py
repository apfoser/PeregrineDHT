import socket
import pickle

class Contact:
    
    def __init__(self, ip: str, port: int, sockfd: socket = None):
        self.ip = ip
        self.port = port
        self.sockfd = sockfd

    # create the response that will be sent back to thec client
    # fields of message.body will be set
    # message.body returned
    def create_response(self):
        pass
    
    
    # send serialized message back to client using server.socket
    def send_message(self, sock,  message):
        
        #print(self.port, message)
        data = pickle.dumps(message)

        # If 0 is returned, 0 bytes are sent
        if (sock.sendto(data, (self.ip, self.port)) == 0):
            print("Error transmitting message")


    def send_pong(self, sock):
        
        m = {
            "type" : "pong",
            "data" : ""
        }
        self.send_message(sock, m)
        
    def send_ping(self, sock):
        
        m = {
            "type" : "ping",
            "data" : ""
        }
        self.send_message(sock, m)