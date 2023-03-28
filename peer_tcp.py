import socket
import threading
from collections import deque

socket_type = socket.SOCK_STREAM

class Contact:
    
    def __init__(self, ip: str, port: int, sockfd: socket = None):
        self.ip = ip
        self.port = port
        self.sockfd = sockfd

class Message:
    
    def __init__(self, sender: str, body: str):
        self.sender = sender
        self.body = body


class Peer_server:
    
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
        
        # TODO handle this exception
        if (info.sockfd.sendall(message.encode()) != None):
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
        
        connections = 0
        for possible_connection in ret:
            addr = possible_connection[-1]
            sockfd = socket.socket(socket.AF_INET6, socket_type)
            
            # returns indicator, not exception (like C)
            if sockfd.connect_ex(addr) != 0:
                continue
            connections += 1
            new_contact = Contact(addr[0], addr[1] , sockfd)
            break
            
        if connections == 0:
            print("Failed to connect")
            
        # update info of Contact object
        with self.connections_lock:
            self.connections[peer_id] = new_contact
            
        # TODO, create listener thread
        client_thread = threading.Thread(target=self.receive_loop, args= (sockfd, peer_id))
        client_thread.start()
        
            
            
    def run_server(self):
        
        local_port = self.port
        
        # returns list of tuples of possible connections
        try:
            ret = socket.getaddrinfo(host = '', port = local_port, 
                                     family = socket.AF_INET6,
                                     type= socket_type)
            
        except socket.gaierror:
            print("Error fetching addresses (server instantiation)")
            return

        
        connections = 0
        for possible_connection in ret:
            addr = possible_connection[-1]
            sockfd = socket.socket(socket.AF_INET6, socket_type)
            
            # allow the port to become availbale after end
            sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # bind to (host, port) (ipv6 adds some other stuff to tuple)
            sockfd.bind(addr)
            
            connections += 1
            break
        
        if connections == 0:
            print("Server instantiation failed")
            exit()
            
            
        # allow up to 10 clients
        sockfd.listen(10)
        connect_number = 1
        
        while (True):
            
            # create new contact entry
            client_sockfd, client_addr = sockfd.accept()
            new_contact = Contact(client_addr[0], client_addr[1] , client_sockfd)
            peer_id = connect_number
            connect_number += 1
            
            with self.connections_lock:
                self.connections[peer_id] = new_contact
    
            client_thread = threading.Thread(target=self.receive_loop, args=(client_sockfd, peer_id))
            client_thread.start()
            
 
    def receive_loop(self, sockfd: socket, peer_id: str):
        
        count = 0
        
        while (True):
            
            received = sockfd.recv(100).decode("utf-8")
            if len(received) == 0:
                break
            
            m = Message(peer_id, received)
            
            with self.messages_lock:
                self.messages.append(m)
    