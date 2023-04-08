import hashlib

def calc_key(data):
    key = hashlib.sha256()
    key.update(data.encode())
    
    return key.hexdigest()[:20]

def calc_id(host, port):
    id = hashlib.sha256()
    id.update(host.encode())
    id.update(str(port).encode())
    
    # I think truncation preserves even distribution
    # truncate to 160
    return id.hexdigest()[:20]

# use XOR to find the largest differing bit of the distance
# between the two id's (XOR is kademlia specific)
def largest_differing_bit(id1, id2):
    
    id1 = int(id1, 16)
    id2 = int(id2, 16)
    
    distance = id1 ^ id2
    l = -1
    while distance:
        distance >>= 1
        l += 1
        
    return max(0, l)