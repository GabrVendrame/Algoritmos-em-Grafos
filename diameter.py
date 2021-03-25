from collections import deque

class grafo:
    def __init__(self, v, adj):
        self.v = v
        self.adj = adj

class vertice:
    def __init__(self, pos, d, pai, cor):
        self.cor = cor
        self.pai = pai
        self.d = d
        self.pos = pos

# insere um vertice s na fila
def enqueue(queue, s):
    queue.append(s)

# remove um vertice s da fila
def dequeue(queue):
    return queue.popleft()

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
       
def diameter(t):
    s = t.v[0]
    a = bfs(t, s)
    b = bfs(t, a)
    return b.d

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco') for i in range(7)]
g.adj = [[g.v[4], g.v[3]], 
        [g.v[6], g.v[2], g.v[5]], 
        [g.v[1]], 
        [g.v[0], g.v[6]], 
        [g.v[0]], 
        [g.v[1]], 
        [g.v[3], g.v[1]]]
assert diameter(g) == 5

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco') for i in range(6)]
g.adj = [[g.v[5]], 
        [g.v[3], g.v[4]], 
        [g.v[5], g.v[3]], 
        [g.v[2], g.v[1]], 
        [g.v[1]], 
        [g.v[0], g.v[2]]] 
assert diameter(g) == 5

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco') for i in range(5)]
g.adj = [[g.v[2], g.v[4]], 
        [g.v[4]], 
        [g.v[0]], 
        [g.v[4]], 
        [g.v[0], g.v[3], g.v[1]]]
assert diameter(g) == 3

g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco') for i in range(10)]
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
g.v = [vertice(i, -float('inf'), None, 'branco') for i in range(8)]
g.adj = [[g.v[6], g.v[3]], 
        [g.v[3], g.v[7]], 
        [g.v[5]], 
        [g.v[0], g.v[1]], 
        [g.v[5]], 
        [g.v[6], g.v[2], g.v[4]], 
        [g.v[0], g.v[5]], 
        [g.v[1]]]
assert diameter(g) == 6