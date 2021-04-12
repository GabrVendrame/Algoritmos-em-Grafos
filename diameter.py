# ALUNO: Gabriel de Souza Vendrame RA: 112681
from collections import deque
import random

class grafo:
    def __init__(self, v, adj):
        self.v = v
        self.adj = adj

class vertice:
    def __init__(self, pos, d, pai, cor, visitado):
        self.cor = cor
        self.pai = pai
        self.d = d
        self.pos = pos
        self.visitado = visitado

# insere um vertice s na fila
def enqueue(queue, s):
    queue.append(s)

# remove um vertice s da fila
def dequeue(queue):
    return queue.popleft() # a funcao popleft, diferentemente da pop, tem tempo de execucao O(1)
                           # entao o tempo de execucao original O(V + E) se mantem

# verifica a distancia minima de um vertice s ate os vertices acessiveis a partir de s
def bfs(G, s):
    for v in G.v:
        v.cor = 'branco'
        v.d = 0
        v.pai = None 
    s.d = 0
    s.cor = 'cinza'
    queue = deque([])
    enqueue(queue, s)
    max = s
    while queue != deque([]):
        u = dequeue(queue)
        for v in G.adj[u.pos]:
            if v.cor == 'branco':
                v.cor = 'cinza'
                v.d = u.d + 1
                v.pai = u
                if v.d > max.d:
                    max = v
                enqueue(queue, v)
        u.cor = 'preto'        
    return max
       
# calcula o diametro de uma arvore T, ou seja, o maior caminho em T
def diameter(t):
    s = t.v[0]
    a = bfs(t, s)
    b = bfs(t, a)
    return b.d

def random_tree_walk(n):
    g = grafo([], [])
    g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(n)]
    u = g.v[0]
    u.visitado = True
    tam = 0
    g.adj = [[] for i in range(n)]
    while tam < n-1:
        v = g.v[random.randint(0, n-1)]
        if v.visitado == False:
            g.adj[u.pos].append(v)
            g.adj[v.pos].append(u)
            tam += 1
            v.visitado = True
        u = v
    return g

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(7)]
g.adj = [[g.v[4], g.v[3]], 
        [g.v[6], g.v[2], g.v[5]], 
        [g.v[1]], 
        [g.v[0], g.v[6]], 
        [g.v[0]], 
        [g.v[1]], 
        [g.v[3], g.v[1]]]
assert diameter(g) == 5

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(6)]
g.adj = [[g.v[5]], 
        [g.v[3], g.v[4]], 
        [g.v[5], g.v[3]], 
        [g.v[2], g.v[1]], 
        [g.v[1]], 
        [g.v[0], g.v[2]]] 
assert diameter(g) == 5

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(5)]
g.adj = [[g.v[2], g.v[4]], 
        [g.v[4]], 
        [g.v[0]], 
        [g.v[4]], 
        [g.v[0], g.v[3], g.v[1]]]
assert diameter(g) == 3

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(10)]
g.adj = [[g.v[1], g.v[2]], 
        [g.v[0], g.v[3]], 
        [g.v[0], g.v[5]], 
        [g.v[1], g.v[8]], 
        [g.v[8], g.v[9]], 
        [g.v[2], g.v[7]], 
        [g.v[9]], 
        [g.v[5]], 
        [g.v[3], g.v[4]], 
        [g.v[4], g.v[6]]]
assert diameter(g) == 9

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(8)]
g.adj = [[g.v[6], g.v[3]], 
        [g.v[3], g.v[7]], 
        [g.v[5]], 
        [g.v[0], g.v[1]], 
        [g.v[5]], 
        [g.v[6], g.v[2], g.v[4]], 
        [g.v[0], g.v[5]], 
        [g.v[1]]]
assert diameter(g) == 6

def dfs(g, n):
    global tempo
    for u in g.v:
        u.cor = 'branco'
    u = g.v[0]
    tempo = 0
    if dfs_visit(g, u) == True and (tempo/2) == n:
        return True
    else:
        return False 
    
def dfs_visit(g, u):
    global tempo
    tempo += 1
    u.cor = 'cinza'
    res = True
    for v in g.adj[u.pos]:
        if v.cor == 'branco':
            res = dfs_visit(g, v)
        elif v.cor == 'preto':
            return False
    tempo += 1
    return res

def main():
    arquivo = open("random-walk.txt", "w")
    for n in range (250, 2001, 250):
        d = 0
        for i in range(500):
            g = random_tree_walk(n)
            assert dfs(g, n) == True
            d = d + diameter(g)
        d = d / 500
        arquivo.write("{} {}\n".format(n, d))
 
if __name__ == '__main__':
    main()