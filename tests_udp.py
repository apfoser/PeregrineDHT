import peer_udp
import time
import sys

current_port = 14000

def gen_connections_helper(n, peer_list, contact_infos):
    
    global current_port
    
    if len(peer_list) != 0 or len(contact_infos) != 0:
        return False
    
    for i in range(n):
        p = peer_udp.UDP_Server(str(i), current_port)
        info = peer_udp.Contact('fe80::5dca:6908:58c3:c55f', current_port, '')
        current_port += 1
        peer_list.append(p)
        contact_infos.append(info)
    
      
    for i in range(n):
        for j in range(n):
            if (i != j):
                peer_list[i].create_connection(str(j), contact_infos[j])
                
    return True

def connections_test(n):
    
    p_list = []
    gen_connections_helper(n, p_list, [])

    failures = []
    for i in range(len(p_list)):
        p = p_list[i]
        if p.get_num_connections() != n - 1:
            failures.append(("FAIL at peer: " + str(i)))
            
    if not failures:
        return ["ALL PASSED"]
    return failures
   
       
def broadcast_test(n):
    
    peer_list = []
    connections_list = []
    failures = []
    
    gen_connections_helper(n, peer_list, connections_list)
    
    for i in range(n):
        peer_list[i].broadcast(str(i))
        time.sleep(1*(10**(-6)))
        
    for i in range(n):
        num_messages = peer_list[i].get_num_messages()
        
        if num_messages != n - 1:
            failures.append(("NUM_MESSAGE FAIL at peer: " + str(i)))
            
        for j in range(n):
            if i == j: continue
            m = peer_list[i].get_message()
            if not m or not m.body or m.body != str(j):
                failures.append(("BODY MESSAGE FAIL at peer: " + str(i)))
            
    if not failures:
        failures.append('ALL PASSED')
    
    return failures

n = int(sys.argv[1])

start_time = time.time()
print("Connections Test:", str(connections_test(n)))
end_time = time.time()
print("Time (ms)(n = " + str(n) + "):", 1000*(end_time-start_time), "\n")

start_time = time.time()
print("Broadcast Test:", str(broadcast_test(n)))
end_time = time.time()
print("Time(ms)(n = " + str(n) + "):", 1000*(end_time-start_time), "\n")

