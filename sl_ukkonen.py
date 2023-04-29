import time
from suffix_tree import Tree
from suffix_tree import ukkonen

def runtime(TEXT):
    startTime = time.time()
    suffix_tree = Tree({'A': TEXT}, builder=ukkonen.Builder)
    endTime = time.time()
    
    print(endTime - startTime)