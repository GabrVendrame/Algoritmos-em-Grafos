# ALUNO: Gabriel de Souza Vendrame RA: 112681
from collections import deque
import random
import time

# construtor de um grafo com vertice e lista de adjacencia
class grafo:
    def __init__(self, v, adj):
        self.v = v
        self.adj = adj

# construtor de vertice com posição, distancia, pai, cor e se foi visitado
class vertice:
    def __init__(self, pos, d, p, cor, visitado):
        self.pos = pos
        self.d = d
        self.p = p
        self.cor = cor
        self.visitado = visitado

# construtor de um grafo com vertice, matriz de adjacencia e aresta
class grafoC:
    def __init__(self, v, adj, aresta):
        self.v = v
        self.adj = adj
        self.aresta = aresta

# construtor de vertice com posicao, distancia, pai e rank
class verticeC:
    def __init__(self, pos, d, p, rank, chave):
        self.pos = pos
        self.d = d
        self.p = p
        self.rank = rank

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

# gera uma arvore aleatoria com n vertices a partir de um grafo
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

# procedimento dfs modificado para verificar se o a funcao random_tree_walk gera uma arvore
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

# funcao auxiliar para o dfs    
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
    u.cor = 'preto'
    tempo += 1
    return res

# cria um conjunto de apenas um elemento, que é u
def make_set(u):
    u.p = u
    u.rank = 0

# acha um caminho de u para u.p
def find_set(u):
    if u != u.p:
        u.p = find_set(u.p)
    return u.p

# liga um vértice ao outro
def link(u, v):
    if u.rank > v.rank:
        v.p = u
    else:
        u.p = v
        if u.rank == v.rank:
            v.rank += 1

# une os caminhos de u e v chamando a funcao link(u, v)
def union(u, v):
    link(find_set(u), find_set(v))

# funcao auxiliar para o random-tree-kruskal, apos a execucao retorna uma arvore geradora minima do grafo
def mst_kruskal(g):
    i, cont = 0, 0
    n =  len(g.v)
    A = grafo([vertice(i, -float('inf'), None, 'branco', False) for i in range(n)], [[] for i in range(n)])
    for v in g.v:
        make_set(v)
    g.aresta.sort(key=lambda lista : lista[2])
    while cont < n-1:
        u, v, peso = g.aresta[i]
        i += 1
        if find_set(g.v[u]) != find_set(g.v[v]):
            A.adj[u].append(A.v[v])
            A.adj[v].append(A.v[u])
            union(g.v[u], g.v[v])
            cont += 1
    return A

# gera uma arvore aleatoria de n vertices a partir de um grafo completo
def random_tree_kruskal(n):
    g = grafoC([], [], [])
    g.v = [verticeC(i, -float('inf'), None, 0, 0) for i in range(n)]
    g.adj = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            peso = random.random()
            g.adj[i][j] = peso
            g.aresta.append([i, j, peso])
    return mst_kruskal(g)

def mst_prim(g, w, s):
    for u in g.v:
        u.chave = 0
        u.pai = None
    s.chave = 0
    Q = g.v
    while Q != []:
        u = extract_min(Q)
        for v in g.adj[u]:
            if v in Q and peso(u, v) < v.chave:
                v.pai = u
                v.chave = peso(u, v)

def random_tree_prim(n):
    g = grafoC([], [], [])
    g.v = [verticeC(i, -float('inf'), None, 0, 0) for i in range(n)]
    g.adj = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            peso = random.random()
    s = g.v[0]
    return mst_prim(g, w, s)

# escreve o resultado da funcao random_tree_walk em um arquivo
def main():
    arquivo = open("random-tree-kruskal.txt", "w")
    tempo_inicial = time.time()
    for n in range (250, 2001, 250):
        d = 0
        tempoexec = time.time()
        for i in range(500):
            g = random_tree_kruskal(n)
            assert dfs(g, n) == True
            diametro = diameter(g)
            d = d + diametro
            d = d / 500
            arquivo.write("{} {}\n".format(n, d))
            print(n, time.time() - tempoexec)
        tempo_total = time.time() - tempo_inicial
        print("Tempo: {:.2f}".format(tempo_total), "segundos")

if __name__ == '__main__':
    main()

# teste diameter 
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

# teste diameter
g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(6)]
g.adj = [[g.v[5]], 
        [g.v[3], g.v[4]], 
        [g.v[5], g.v[3]], 
        [g.v[2], g.v[1]], 
        [g.v[1]], 
        [g.v[0], g.v[2]]] 
assert diameter(g) == 5

# teste diameter
g = grafo([], [])
g.v = [vertice(i, -float('inf'), None, 'branco', False) for i in range(5)]
g.adj = [[g.v[2], g.v[4]], 
        [g.v[4]], 
        [g.v[0]], 
        [g.v[4]], 
        [g.v[0], g.v[3], g.v[1]]]
assert diameter(g) == 3

# teste diameter
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

# teste diameter
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

# teste make-set
g = grafo([verticeC(i, -float('inf'), None, 0, 0) for i in range(4)], [])
for i in range(4):
    make_set(g.v[i])
    assert g.v[i].p == g.v[i]
    assert g.v[i].rank == 0

# teste union
g = grafo([verticeC(i, -float('inf'), None, 0, 0) for i in range(3)], [])
make_set(g.v[0])
make_set(g.v[1])
make_set(g.v[2])
union((g.v[0]), (g.v[1]))
assert find_set(g.v[0]) == find_set(g.v[1])
union((g.v[1]), (g.v[2]))
assert find_set(g.v[1]) == find_set(g.v[2])

# teste find set
g = grafo([verticeC(i, -float('inf'), None, 0, 0) for i in range(5)], [])
for i in range(5):
    make_set(g.v[i])
    assert find_set(g.v[i]) == g.v[i]

# teste link
g = grafo([verticeC(i, -float('inf'), None, 0, 0) for i in range(4)], [])
make_set(g.v[0])
make_set(g.v[1])
make_set(g.v[2])
make_set(g.v[3])
link(find_set(g.v[0]), find_set(g.v[1]))
link(find_set(g.v[1]), find_set(g.v[2]))
link(find_set(g.v[2]), find_set(g.v[3]))
assert find_set(g.v[0]) == find_set(g.v[1])
assert find_set(g.v[1]) == find_set(g.v[2])
assert find_set(g.v[2]) == find_set(g.v[3])

# teste kruskal
g = grafoC([verticeC(i, -float('inf'), None, 0, 0) for i in range(4)],
    [[0,7,2,1], [7,0,11,1], [2,11,0,13], [1,1,13,0]],
    [(0, 1, 7), (0, 2, 2), (0, 3, 1), (1, 2, 11), (1, 3, 1), (2, 3, 13)])
g2 = mst_kruskal(g)
assert g2.adj == [[g2.v[3], g2.v[2]], [g2.v[3]], [g2.v[0]], [g2.v[0], g2.v[1]]]

# teste kruskal
g = grafoC([verticeC(i, -float('inf'), None, 0, 0) for i in range(4)], 
    [[0,2,14,3], [2,0,13,12], [14,13,0,9], [3,12,9,0]],
    [(0, 1, 2), (0, 2, 14), (0, 3, 3), (1, 2, 13), (1, 3, 12), (2, 3, 9)])
g2 = mst_kruskal(g)
assert g2.adj == [[g2.v[1], g2.v[3]], [g2.v[0]], [g2.v[3]], [g2.v[0], g2.v[2]]]