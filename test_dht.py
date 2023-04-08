import dht_node

node = None
while True:
    choice = input("Command: ")
    
    if choice == "start":
        port = int(input("Enter Port Number: "))
        node = dht_node.dht_node(port)

        print(node.server.id)
        print(node.server.ip)
        
    elif choice == "end":
        if node != None:
            node.shut_down()
            break
        
    elif choice == "boot":
        if node != None:
            ip = input("IP: ")
            port = int(input("Port: "))
            node.bootstrap((ip, port))
    
    elif choice == "connections":
        if node != None:
            node.buckets.print_peers()
