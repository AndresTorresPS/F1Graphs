import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

def all_shortest_paths(graph, source, target):
    """
    Devuelve una tupla (lista de caminos más cortos, distancia mínima) entre dos nodos en un grafo dirigido.
    Cada camino es una lista de nodos.
    """
    try:
        paths = list(nx.all_shortest_paths(graph, source=source, target=target, weight='weight'))
        if not paths:
            return [], float('inf')
        # Calcular la distancia del primer camino (todos tienen la misma distancia)
        distance = nx.path_weight(graph, paths[0], weight='weight')
        return paths, distance
    except nx.NetworkXNoPath:
        return [], float('inf')

def print_graph(graph):
    plt.figure(figsize=(10, 7))  # Tamaño más grande para mejor legibilidad
    pos = nx.spring_layout(graph, k=10, seed=100)  # Distribución más clara y reproducible
    nx.draw(
        graph, pos,
        with_labels=True,
        node_color='skyblue',
        edge_color='gray',
        arrows=True,
        node_size=1200,
        font_size=12,
        font_weight='bold'
    )
    # Dibujar etiquetas de los pesos si existen
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=edge_labels,
            font_color='black', font_size=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )
    plt.axis('off')
    #plt.tight_layout()
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

def print_graph_with_paths(graph, paths):
    
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(graph, k=10, seed=100)
    nx.draw(
        graph, pos,
        with_labels=True,
        node_color='skyblue',
        edge_color='gray',
        arrows=True,
        node_size=1200,
        font_size=12,
        font_weight='bold'
    )
    # Colores para los caminos
    colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
    for i, path in enumerate(paths):
        color = colors[i % len(colors)]
        edges_in_path = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=edges_in_path,
            edge_color=color,
            width=3,
            arrows=True
        )
    # Dibujar etiquetas de los pesos DESPUÉS de los caminos resaltados
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=edge_labels,
            font_color='black', font_size=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Leer la matriz de adyacencia desde el archivo CSV (incluyendo encabezados)
    adjacency_df = pd.read_csv('F1Data/mark_01.csv', index_col=0)

    # Crear el grafo dirigido y ponderado
    mark_01_graph = new_di_graph(adjacency_df)

    # Imprime los caminos más cortos y la distancia mínima entre 'Start' y 'End'
    paths, distance = all_shortest_paths(mark_01_graph, 'Start', 'End')
    print(all_shortest_paths(mark_01_graph, 'Start', 'End'))

    # Imprime el grafo con los caminos resaltados
    print_graph_with_paths(mark_01_graph, paths)




    
