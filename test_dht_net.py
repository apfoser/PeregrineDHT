import interface_node
import dht_node
import utils
import time
from threading import Thread

current_node = None
nodes = []

def create_net(n, port):
    print("Setting net up...")
    current_port = port
    
    # create the interface/bootstrap node
    # create in new thread
    t = Thread(target = interface_node.interface_node, args=(current_port,))
    t.start()
    current_port += 1
    
    # create n-1 dht nodes
    for _ in range(n-1):
        n = dht_node.dht_node(current_port)
        nodes.append(n)
        current_port += 1
        
    # bootsrap at first node
    for n in nodes:
        n.bootstrap((n.server.ip, port))
        
    return nodes[-1]

while True:
    choice = input("Command: ")
    
    if choice == "start":
        n, port = input("# port: ").split(" ")
        n = int(n)
        port = int(port)
        current_node = create_net(n, port)
        
        print("Current Node:", (current_node.server.ip, current_node.server.port))
        
    elif choice == "store":
        dat = input("Data: ")
        key = utils.calc_key(dat)
        print("Key:", key)
        
        storage_nodes = current_node.store(key)

        for n in storage_nodes:
            print("Stored At:", n)
            
    elif choice == "get":
        
        key = input("Key: ")
        if current_node.get(key):
            print("Found", key)
        else:
            print("Not Found")
            
    elif choice == "exit":
        for node in nodes:
            node.shut_down()
            
        break