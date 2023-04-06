from peer_udp import UDP_Server
from buckets import bucket_tree
from contact import Contact
import utils

k = 20
id_len = 160

class dht_node():
    
    def __init__(self, port = 12829, boot_addr = None):
        
        # starts server in separate thread
        self.server = UDP_Server(port)
        self.server.dht = self
        
        # necessary kademlia structures
        self.contact = Contact(self.server.ip, self.server.port, self.server.id)
        self.buckets = bucket_tree(self.server.id, k, id_len)
        
        self.data = {}
        self.rcps = {}
        
        if boot_addr: self.bootstrap(*boot_addr)
        
        
    def bootstrap(self, address):
        contact = Contact(address[0], address[1], utils.calc_id(*address))
        
        # do the bootstrapping
        
    def find_nodes(self):
        pass
    
    def find_value(self):
        pass
    
    def store(self):
        pass
    
    def get(self):
        pass