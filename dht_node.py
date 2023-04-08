from peer_udp import UDP_Server
from buckets import bucket_tree
from contact import Contact
from lookup import lookup
import random
import utils
import time

k = 20
alpha = 3
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
        self.rpcs = {}
        
        if boot_addr != None: self.bootstrap(*boot_addr)
        
    def find_nodes(self, key, boot_peer = None):
        candidates = lookup(k, key)
        candidates.update(self.buckets.nearest_nodes(key, limit = alpha))
        sender = (self.server.ip, self.server.port)
        
        if boot_peer != None:
            rpc_id = random.getrandbits(id_len)
            self.rpcs[rpc_id] = candidates
            boot_peer.find_nodes(self.server.sock, sender, rpc_id, key)
            
        while not candidates.complete() or boot_peer:
            nearest_nodes = candidates.next_iter(alpha)
            for peer in nearest_nodes:
                candidates.mark(peer) #this is the key step that leads to completness
                rpc_id = random.getrandbits(id_len)
                self.rpcs[rpc_id] = candidates
                peer.find_nodes(self.server.sock, sender, rpc_id, key)
            time.sleep(1)
            boot_peer = None
            
        return candidates.results()    
    
    def find_value(self, key):
        pass
    
    def bootstrap(self, address):
        contact = Contact(address[0], address[1], utils.calc_id(*address))
        self.buckets.insert(contact)
        
        # do the bootstrapping (find nodes with key = contact.id)
        neighbors = self.find_nodes(self.server.id, boot_peer = contact)
        
        for n in neighbors:
            self.buckets.insert(n)
    
    def store(self, key):
        
        storage_candidates = self.find_nodes(key)
        
        if storage_candidates:
            for candidate in storage_candidates:
                sender = (self.server.ip, self.server.port)
                candidate.store(self.server.sock, sender, data = key)
                
        else:
            self.data[key] = 1
    
    def get(self, key):
        
        if key in self.data: return self.data[key]
        res = self.find_value(key)

        if res: return res
        raise KeyError        
    
    def shut_down(self):
        self.server.shut_down()
        
        
        