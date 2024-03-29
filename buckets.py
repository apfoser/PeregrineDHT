from contact import Contact
import threading
import heapq
import utils

class bucket_tree():
    
    def __init__(self, id, bucket_size, buckets):
        self.id = id
        self.bucket_size = bucket_size
        self.buckets = [[] for _ in range(buckets)]
        self.lock = threading.Lock()
    
    def insert(self, contact: Contact):
        
        # don't need to insert ourselves in our bucket set
        if contact.id == self.id: return
        
        bucket_num = utils.largest_differing_bit(self.id, contact.id)
        contact_triple = contact.astriple()
        
        with self.lock:
            bucket = self.buckets[bucket_num]
            if contact_triple in bucket: 
                bucket.pop(bucket.index(contact_triple))
            elif len(bucket) >= self.bucket_size:
                bucket.pop(0)
            bucket.append(contact_triple)
    
    def nearest_nodes(self, key, limit = None):
        num_results = min(limit, self.bucket_size) if limit else self.bucket_size
        with self.lock:
            def distance(peer):
                #print("peer", key, peer[2])
                return int(key, 16) ^ int(peer[2], 16)

            peers = []
            for bucket in self.buckets:
                for p in bucket:
                    peers.append(p)
                    
            best_peers = heapq.nsmallest(num_results, peers, distance)
            return [Contact(*peer) for peer in best_peers]
        
    def print_peers(self):
        for bucket in self.buckets:
                for p in bucket:
                    print(p)