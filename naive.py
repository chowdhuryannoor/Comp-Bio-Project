import time

class Node:
    def __init__(self, lab):
        self.lab = lab
        self.out = {}

class Tree:
    def __init__(self,	s):
        self.root = Node(None)
        self.root.out[s[0]]	= Node(s)
        for	i in range(1, len(s)):
            cur	= self.root
            j = i
            while j < len(s):
                if s[j] in cur.out:
                    child =	cur.out[s[j]]
                    lab	= child.lab
                    k =	j + 1
                    while k-j < len(lab) and s[k] == lab[k-j]:
                        k += 1
                    if k-j == len(lab):
                        cur = child
                        j =	k
                    else:
                        cExist,	cNew = lab[k-j], s[k]
                        mid	= Node(lab[:k-j])
                        mid.out[cNew] = Node(s[k:])
                        mid.out[cExist] = child
                        child.lab = lab[k-j:]
                        cur.out[s[j]] =	mid
                else:
                    cur.out[s[j]] = Node(s[j:])

# def printTree(node, level=0):
#     if not node:
#         return
#     label = 'root' if node.lab == None else node.lab
#     print("  " * level + str(label))
#     for child in node.out:
#         printTree(node.out[child], level + 1)

def runtime(TEXT):
    startTime = time.time()
    suffix_tree = Tree(TEXT)
    endTime = time.time()
    
    # printTree(suffix_tree.root)
    return endTime - startTime

# runtime("nonsense$")