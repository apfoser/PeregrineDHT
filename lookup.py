import threading

from contact import Contact

class lookup():
    
    def __init__(self, k, key):
        self.k = k
        self.key = key
        self.list = []
        self.lock = threading.Lock()
        self.completion_value = None
        
    def set_complete(self, value):
        with self.lock:
            self.completion_value = value
            
    def result(self):
        with self.lock : return self.completion_value
        
    def update(self, nodes):
        for n in nodes:
            self.insert(n)
            
    def insert(self, node):
        if node.id == self.id or self.completion_value:
            return
        with self.lock:
            for i in range(len(self.list)):
                each = self.list[i]
                if node.id == each[0][2]: break
            
                if node.id ^ self.key < each[0][2] ^ self.key:
                    self.list.insert(i, (node.astriple(), False))
                    self.list = self.list[:min(self.k, len(self.list))]
                    break
                
                else:
                    if len(self.list) < self.k:
                        self.list.append((node.astriple(), False))
                        
    def mark(self, node):
        for i in range(len(self.list)):
            if node.id == self.list[i][0][2]:
                self.list[i][-1] = True
                
    def complete(self):
        if self.completion_value: return True
        
        with self.lock:
            for node, status in self.list:
                if not status: return False
                
            return True
        
        
    def next_iter(self, alpha):
        if self.completion_value: return []
        next_iter = []
        
        with self.lock:
            for node, status in self.list:
                if not status:
                    next.iter.append(Contact(*node))
                    if len(next_iter) == alpha:
                        break
                    
        return next_iter
    
    def results(self):
        with self.lock:
            return [Contact(*node) for node, status in self.list]