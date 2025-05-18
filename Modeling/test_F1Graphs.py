import networkx as nx
from F1Graphs import new_di_graph

def test_new_di_graph_empty():
    matriz = []
    G = new_di_graph(matriz)
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() == 0
    assert G.number_of_edges() == 0

def test_new_di_graph_single_node():
    matriz = [[0]]
    G = new_di_graph(matriz)
    assert G.number_of_nodes() == 1
    assert G.number_of_edges() == 0

def test_new_di_graph_simple():
    matriz = [
        [0, 1],
        [0, 0]
    ]
    G = new_di_graph(matriz)
    assert set(G.nodes) == {0, 1}
    assert set(G.edges) == {(0, 1)}

def test_new_di_graph_multiple_edges():
    matriz = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ]
    G = new_di_graph(matriz)
    assert set(G.nodes) == {0, 1, 2}
    assert set(G.edges) == {(0, 1), (1, 2), (2, 0)}

def test_new_di_graph_self_loop():
    matriz = [
        [1, 0],
        [0, 0]
    ]
    G = new_di_graph(matriz)
    assert (0, 0) in G.edges
    assert G.number_of_edges() == 1

