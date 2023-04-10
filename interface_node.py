import dht_node
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class interface_server(BaseHTTPRequestHandler):
    def do_GET(self):
        
        key = self.path[1:]
        print(key)
        
        if key != "favicon.ico":
            res = self.server.node.get(key)
        else:
            res = "Invalid"
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(res, encoding="utf-8"))
        
class interface_node():
    
    def __init__(self, port):
        self.dht_node = dht_node.dht_node(port)
        self.web_server = ThreadedHTTPServer(('localhost', 10000), interface_server)
        self.web_server.node = self
        
        self.run_server()
        
    def get(self, key):
        res = self.dht_node.get(key)
        if not res: return "Not Found"
        else: return "Found " + key
        
    def run_server(self):
        try:
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            pass