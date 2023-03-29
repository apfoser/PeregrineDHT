import socket
import threading
from collections import deque
from contact import Contact, Message
import pickle

socket_type = socket.SOCK_DGRAM

class UDP_Server:
    
    def __init__(self, id: str, port: int = 12829):
        
        self.id = id
        
        # termination flag
        self.end = 0
        
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
            
        # filled in by setup server
        self.ip = None
        
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
    
    
    def broadcast(self, message: str):
        
        body = {
            "type" : "broadcast",
            "data" : message
            }
        
        for peer in self.connections:
            
            sender = (self.ip, self.port)
            m = Message(sender, body)
            con = self.connections[peer]
            con.send_message(self.sock, m)
            
    
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
        
        # set ip
        self.ip = addr[0]
        
        sockfd = socket.socket(socket.AF_INET6, socket_type)
        # allow the port to become available after end
        sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sockfd.bind(addr)
    
        return(sockfd)
        
    def run_server(self):
    
        while (not self.end):
            
            # create new contact entry
            try:
                client_message, client_addr = self.sock.recvfrom(1024)
            except ConnectionResetError:
                print("Error associated with (ip, port):", "(localhost, " + str(self.port) + ")")
                break
            
            # deserialize
            message = pickle.loads(client_message)
            
            # shudown signal
            if message.body["type"] == "end": break
            
            #print("R:", message.sender, message.body)
            
            client_ip = message.sender[0]
            client_port = message.sender[1]
            
            new_contact = Contact(client_ip, client_port)
            
            with self.connections_lock:
                self.connections[(client_ip, client_port)] = new_contact
                
            # if it is just a connection message, we don't care
            # no need to append to message queue
            if message.body["type"] != "connect":
                with self.messages_lock:
                    self.messages.append(message)
                
            # resolve request
            self.request_handler(message)

        self.sock.close()
            
    def request_handler(self, message: Message):
        
        m_con = self.connections[message.sender]
        m_body = message.body
        m_type = m_body["type"]

        # check message type (message.body)
        # send to appropriate contact (message.sender)
        # contact object responds to client (message.sender)
        match m_type:
            
            # no use for these two right now
            case "connect": 
                return
            case "broadcast": 
                return
            
            # send pong
            case "ping": 
                m_con.send_pong(self.sock, (self.ip, self.port))
            
            # no need to do anything
            case "pong": 
                pass
        
    # just closes socket
    # send termination datagram to server sock
    # close temp sock
    def shut_down(self):
        self.end = 1
        shut_down_sock = socket.socket(socket.AF_INET6, socket_type)
        self_contact = Contact(self.ip, self.port)
        sender = (self.ip, self.port)
        body = {"type": "end", "data": ""}
        self_contact.send_message(shut_down_sock, Message(sender, body))

        shut_down_sock.close()
        print ("Peer " + str(self.id) + " Shutting Down. Cya!")
        