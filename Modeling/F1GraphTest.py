import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def new_di_graph_unweighted(adjacency_df):
    """
    Crea un grafo dirigido sin pesos a partir de un DataFrame de adyacencia.
    Se agrega una arista si el valor es distinto de cero.
    """
    G = nx.DiGraph()
    for source in adjacency_df.index:
        for target in adjacency_df.columns:
            if adjacency_df.loc[source, target] != 0:
                G.add_edge(source, target)
    return G

def new_di_graph(adjacency_df):
    """
    Crea un grafo dirigido y ponderado a partir de un DataFrame de adyacencia.
    Los valores del DataFrame se usan como pesos de las aristas.
    """
    G = nx.DiGraph()
    for source in adjacency_df.index:
        for target in adjacency_df.columns:
            weight = adjacency_df.loc[source, target]
            if weight != 0:
                G.add_edge(source, target, weight=weight)
    return G

def print_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
    plt.show()

'''
# Ejemplo: Crear un DataFrame 5x5 de adyacencia con nombres personalizados
nombres = ['A', 'B', 'C', 'D', 'E']
df_adyacencia = pd.DataFrame([
    [0, 1, 0, 0, 1],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0]
], index=nombres, columns=nombres)

grafo = new_di_graph(df_adyacencia)
visualizar_grafo(grafo)
'''

'''
# Leer la matriz de adyacencia desde el archivo CSV sin tomar en cuenta los pesos
adjacency_df = pd.read_csv('Mark01.csv', index_col=0)
mark_01_graph = new_di_graph_unweighted(adjacency_df)
print_graph(mark_01_graph)
'''

# Leer la matriz de adyacencia desde el archivo CSV (incluyendo encabezados)
adjacency_df = pd.read_csv('Mark01.csv', index_col=0)
mark_01_graph = new_di_graph(adjacency_df)
print_graph(mark_01_graph)

