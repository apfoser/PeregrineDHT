import hashlib

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
    distance = id1 ^ id2
    l = -1
    while distance:
        distance >>= 1
        length += 1
        
    return max(0, length)