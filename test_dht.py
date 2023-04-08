import dht_node
import utils
import time


port = 11000

nodes = []

start = time.time()

for _ in range(10):
    n = dht_node.dht_node(port=port)
    nodes.append(n)
    port += 1
    
for i in range(1, len(nodes)):
    n = nodes[i]
    
    n.bootstrap((n.server.ip, 11000))
    #print("\n")
    
print('Time (Bootstrap)(ms): ', 1000* (time.time() - start))

dat = input("Data: ")
key = utils.calc_key(dat)
print("Key:", key)

node = nodes[-1]
storage_nodes = node.store(key)

for n in storage_nodes:
    print("Stored At: ", n)
    
if node.get(key):
    print("\n" + "Found", key)
else:
    print("Not Found")

for i in range(len(nodes)):
    nodes[i].server.shut_down()