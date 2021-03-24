class grafo:
    def __init__(self, v, adj):
        self.v = v
        self.adj = adj

class vertice:
    def __init__(self, cor, pai, d):
        self.cor = cor
        self.pai = pai
        self.d = d

def enqueue(queue, s):
def dequeue(queue):

def bsf(G, s):
    for vertice in G.V:
        v.cor = 'branco'
        v.d = -1
        v.pai = None 
    s.d = 0
    s.cor = 'cinza'
    queue = {}
    enqueue(queue, s)
    while queue != NULL:
        u = dequeue(Q)
        for vertice in G.adj[u]:
            if v.cor == 'branco':
                v.cor = 'cinza'
                v.d = u.d + 1
                v.pai = u
                enqueue(Q, v)
        u.cor = 'preto'


def printcaminho(G, s, v):
    if v == s:
        print(s)
    elif v.pai == None:
        print("nao existe caminho")
    else:
        printcaminho(G, s, v.pai)
        print(v)
