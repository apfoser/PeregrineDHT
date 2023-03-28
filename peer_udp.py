import socket
import threading
from collections import deque
from contact import Contact

socket_type = socket.SOCK_DGRAM

class Message:
    
    def __init__(self, sender: str, body: str):
        self.sender = sender
        self.body = body
        

class UDP_Server:
    
    def __init__(self, id: str, port: int = 12829):
        
        self.id = id
        
        # threading lock(s) for shared resources
        self.connections_lock = threading.Lock()
        self.messages_lock = threading.Lock()
        
        # starting off with no connections
        self.connections = {};
        
        # starting off with no messages
        self.messages = deque()
        
        # check port validity
        if not (1024 <= port <= 65535):
            self.port = 12829
        else:
            self.port = port
        
        # setup socket server
        self.sock = self.setup_server()
        
        # start server thread
        server_thread = threading.Thread(target = self.run_server)
        server_thread.start()
    
    def get_num_connections(self):
        
        with self.connections_lock:
            num = len(self.connections)
        
        return num
    
    def get_num_messages(self):
        
        with self.messages_lock:
            num = len(self.messages)
        
        return num
    
    def get_message(self):
   
        if self.get_num_messages() > 0:
            with self.messages_lock:
                m = self.messages[0]
                self.messages.popleft()
                
            return m
        
        else:
            return None
    
    def send_message(self, peer_id: str, message: str):
        
        # Contact object containing info for receiving peer
        # field sockfd contains socket
        info = self.connections[peer_id]
        
        # If 0 is returned, 0 bytes are sent
        if (self.sock.sendto(message.encode(), (info.ip, info.port)) == 0):
            print("Error transmitting message")

        
    
    def broadcast(self, message: str):
        
        for peer in self.connections:
            self.send_message(peer, message)
            
    
    def create_connection(self, peer_id: str, contact_info: Contact):
        
        # returns list of tuples of possible connections
        try:
            ret = socket.getaddrinfo(contact_info.ip, contact_info.port, 
                                        family= socket.AF_INET6,
                                        type= socket_type)
        except socket.gaierror:
            print("Error fetching addresses")
            return
        
        addr = ret[0][-1]
        new_contact = Contact(addr[0], addr[1])
        
        # update info of Contact object
        with self.connections_lock:
            self.connections[(addr[0], addr[1])] = new_contact
                    
    def setup_server(self):
        
        local_port = self.port
        
        # returns list of tuples of possible connections
        try:
            ret = socket.getaddrinfo(host = '', port = local_port, 
                                     family = socket.AF_INET6,
                                     type = socket_type)
            
        except socket.gaierror:
            print("Error fetching addresses (server instantiation)")
            return

        addr = ret[0][-1]
        sockfd = socket.socket(socket.AF_INET6, socket_type)
        # allow the port to become availbale after end
        sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sockfd.bind(addr)
    
        return(sockfd)
        
    def run_server(self):
        
        connect_number = 1
        
        while (True):
            
            # create new contact entry
            try:
                client_message, client_addr = self.sock.recvfrom(1024)
            except ConnectionResetError:
                print("Error associated with (ip, port):", "(localhost, " + str(self.port) + ")")
                break
            
            new_contact = Contact(client_addr[0], client_addr[1])
            peer_id = connect_number
            
            m = Message(peer_id, client_message.decode("utf-8"))
            
            with self.connections_lock:
                self.connections[(client_addr[0], client_addr[1])] = new_contact
                
            with self.messages_lock:
                self.messages.append(m)
                
            # resolve request
            self.request_handler(m)
                
            connect_number += 1
            
    def request_handler(self, message: Message):
        
        print(message.body)
            
            
            
        pass