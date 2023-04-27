from pydivsufsort import divsufsort, kasai
import time

def mapToRank(S):
    map = dict()
    for index, char in enumerate(sorted(set(S))):
        map[char] = index + 1

    ranking = []
    for char in S:
        ranking.append(map[char])

    return ranking

def reverse(S):
    n = len(S)
    reverse = [0] * n
    for i in range(n):
        reverse[S[i] - 1] = i + 1

    return reverse
 
def constructSA(text, n):
    text += '$'
    arrays = []
    mappedText = mapToRank(text)
    arrays.append(mappedText)

    k = 1
    while k < n:
        nextValues = [] 
        for i in range(len(mappedText)):
            nextValue = 0
            if i + k < len(mappedText):
                nextValue = mappedText[i + k]
            nextValues.append((mappedText[i], nextValue))
        mappedText = mapToRank(nextValues)
        arrays.append(mappedText)
        k *= 2
        
    return reverse(arrays[-1])

def constructLCP(text, SA):
    text += '$'
    n = len(SA)
    phi = [0] * n
    phi[SA[0] - 1] = SA[-1]
    for i in range(1, n):
        phi[SA[i] - 1] = SA[i - 1]

    l = 0
    PLCP = [0] * n
    for i in range(n):
        p = phi[i] - 1
        while text[i + l] == text[p + l]:
            l = l + 1
        PLCP[i] = l
        l = max(l - 1, 0)

    LCP = [0] * n
    for i in range(1, n):
        LCP[i] = PLCP[SA[i] - 1]

    return LCP

class Node:
    def __init__(self):
        self.label = ''
        self.parent = None
        self.children = []
    
    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def removeChild(self, oldChild):
        self.children = [child for child in self.children if child.label != oldChild.label]

def sdepth(node):
    depth = len(node.label)
    while node.parent != None:
        node = node.parent
        depth += len(node.label)
     
    return depth

def printTree(node, level=0):
    if not node:
        return
    label = 'root' if node.label == '' else node.label
    print("  " * level + str(label))
    for child in node.children:
        printTree(child, level + 1)

def constructST(SA, LCP, text):
    root = Node()
    v = root
    n = len(SA)
    for i in range(n):
        lcp = LCP[i]
        prev = None
        while sdepth(v) > lcp:
            prev = v
            v = v.parent
        if sdepth(v) == lcp:
            child = Node()
            child.label = text[SA[i]:]
            v.addChild(child)
            v = child
        else:
            v.removeChild(prev)
            mainChild = Node()
            start = SA[i - 1] + sdepth(v)
            end = SA[i - 1] + lcp
            mainChild.label = text[start:end]
            v.addChild(mainChild)
            child1 = Node()
            start = SA[i - 1] + lcp
            end = SA[i - 1] + sdepth(prev)
            child1.label = text[start:end]
            mainChild.addChild(child1)
            child2 = Node()
            child2.label = text[(SA[i] + lcp):]
            mainChild.addChild(child2)
            v = child2

    return root

if __name__ == "__main__":
    s = 'banana$'
    SA = divsufsort(s)
    LCP = list(kasai(s, SA))
    LCP = LCP[-1:] + LCP[:-1]
    SA = list(SA)
    print(SA)
    print(LCP)
    print('Suffix Tree:')
    ST = constructST(SA, LCP, s)
    printTree(ST)

