import time
from pydivsufsort import divsufsort, kasai

class Node:
    def __init__(self):
        self.start = -1
        self.end = -1
        self.parent = None
        self.children = {}
        self.depth = 0
    
    def addChild(self, child, key):
        child.parent = self
        child.depth = (child.end - child.start) + self.depth
        self.children[key] = child

    def removeChild(self, key):
        del self.children[key]

class Tree:
    def __init__(self, SA, LCP, text):
        self.root = Node()
        v = self.root
        n = len(SA)
        for i in range(n):
            lcp = LCP[i]
            prev = None
            while v.depth > lcp:
                prev = v
                v = v.parent
            if v.depth == lcp:
                child = Node()
                child.start = SA[i]
                child.end = len(text)
                v.addChild(child, text[child.start:child.end])
                v = child
            else:
                v.removeChild(text[prev.start:prev.end])
                mainChild = Node()
                start = SA[i - 1] + v.depth
                end = SA[i - 1] + lcp
                mainChild.start = start
                mainChild.end = end
                v.addChild(mainChild, text[mainChild.start:mainChild.end])
                child1 = Node()
                start = SA[i - 1] + lcp
                end = SA[i - 1] + prev.depth
                child1.start = start
                child1.end = end
                mainChild.addChild(child1, text[child1.start:child1.end])
                child2 = Node()
                child2.start = SA[i] + lcp
                child2.end = len(text)
                mainChild.addChild(child2, text[child2.start:child2.end])
                v = child2

def runtime(TEXT):
    startTime = time.time()
    temp_sa= divsufsort(TEXT)
    temp_lcp = list(kasai(TEXT, temp_sa))
    SA = list(temp_sa)
    LCP = temp_lcp[-1:] + temp_lcp[:-1]
    suffix_tree = Tree(SA, LCP, TEXT)
    endTime = time.time()
    
    print(endTime - startTime)