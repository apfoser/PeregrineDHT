import peer_udp as peer_udp
import time
import sys
import socket
import contact
from hanging_threads import start_monitoring

current_port = int(sys.argv[2])
n = int(sys.argv[1])

def gen_connections_helper(n, peer_list, contact_infos):
    
    global current_port
    
    if len(peer_list) != 0 or len(contact_infos) != 0:
        return False
    
    for i in range(n):
        p = peer_udp.UDP_Server(current_port)
        info = peer_udp.Contact('fe80::5dca:6908:58c3:c55f', current_port, '')
        current_port += 1
        peer_list.append(p)
        contact_infos.append(info)
    return

def connections_test(n):
    
    peer_list = []
    connections_list = []
    gen_connections_helper(n, peer_list, connections_list)
    
    for i in range(n):
        for j in range(n):
            if (i != j):
                body = {"type" : "connect", "data" : ""}
                sender = (peer_list[i].ip, peer_list[i].port)
                connections_list[j].send_message(peer_list[i].sock, contact.Message(sender, body))
    
    time.sleep(1*10**(-6))

    failures = []
    for i in range(len(peer_list)):
        p = peer_list[i]
        if p.get_num_connections() != n - 1:
            failures.append(("FAIL at peer: " + str(i)))
            
    if not failures:
        failures.append("ALL PASSED")
    
    for p in peer_list:
        p.shut_down()
        
    return failures
   
       
def broadcast_test(n):
    
    peer_list = []
    connections_list = []
    failures = []
    
    gen_connections_helper(n, peer_list, connections_list)
    
    for i in range(len(peer_list)):
        for j in range(len(connections_list)):
            if i != j:
                c = connections_list[j]
                peer_list[i].connections[(c.ip, c.port)] = c

    time.sleep(1*10**(-6))
    
    for i in range(n):
        peer_list[i].broadcast(str(i))
        
    time.sleep(1*10**(-6))
        
    for i in range(n):
        num_messages = peer_list[i].get_num_messages()
        #print([m.body for m in peer_list[i].messages])
        
        if num_messages != n - 1:
            failures.append(("FAIL at peer: " + str(i)))
          
        
        for j in range(n):
            if i == j: continue
            m = peer_list[i].get_message()
            if not m or not m.body or m.body["data"] != str(j):
                failures.append(("BODY MESSAGE FAIL at peer: " + str(i)))
        
         
    if not failures:
        failures.append('ALL PASSED')
        
    for p in peer_list:
        p.shut_down()
        
    return failures


def ping_pong(n):
    
    peer_list = []
    connections_list = []
    failures = []
    
    gen_connections_helper(n, peer_list, connections_list)
    
    for i in range(len(peer_list)):
        for j in range(len(connections_list)):
            if i != j:
                c = connections_list[j]
                peer_list[i].connections[(c.ip, c.port)] = c
    
    time.sleep(1*10**(-6))
    
    peer1 = peer_list[0]
    
    for each in peer1.connections.values():
        each.send_ping(peer1.sock, (peer1.ip, peer1.port))
        
    time.sleep(1*10**(-6))
    
    if peer1.get_num_messages() != n - 1:
        failures.append("FAILED TO COLLECT " + str(n-1) + " PONGS")
        
    if not failures:
        failures.append("ALL PASSED")
        
    for p in peer_list:
        p.shut_down()
        
    return failures

start_time = time.time()
print("Connections Test:", str(connections_test(n)))
end_time = time.time()
print("Time (ms)(n = " + str(n) + "):", 1000*(end_time-start_time), "\n")

time.sleep(1*10**(-6))

start_time = time.time()
print("Broadcast Test:", str(broadcast_test(n)))
end_time = time.time()
print("Time(ms)(n = " + str(n) + "):", 1000*(end_time-start_time), "\n")

time.sleep(1*10**(-6))
        
start_time = time.time()
print("Ping Pong:", str(ping_pong(n)))
end_time = time.time()
print("Time (ms)(n = " + str(n) + "):", 1000*(end_time-start_time), "\n")

