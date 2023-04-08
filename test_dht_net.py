import dht_node
import utils
import time

current_node = None
nodes = []

def create_net(n, port):
    print("Setting net up...")
    current_port = port
    for _ in range(n):
        n = dht_node.dht_node(current_port)
        nodes.append(n)
        current_port += 1
        
    for n in nodes[1:]:
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