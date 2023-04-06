import dht_node

node = dht_node.dht_node(11000)

# instatiation & shut_down works
print(node.server.id)
node.server.shut_down()