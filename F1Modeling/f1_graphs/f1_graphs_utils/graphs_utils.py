import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class GraphCreation:

    def di_unweighted_graph(adjacency_df):
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
    
    def di_weighted_graph(adjacency_df):
        """
        Crea un grafo dirigido y ponderado a partir de un DataFrame de adyacencia.
        Se agrega una arista con el peso correspondiente.
        """
        G = nx.DiGraph()
        for source in adjacency_df.index:
            for target in adjacency_df.columns:
                weight = adjacency_df.loc[source, target]
                if weight != 0:
                    G.add_edge(source, target, weight=weight)
        return G
    
class GraphAnalysis:

    def dfs(graph, start):
        """
        Realiza una búsqueda en profundidad (DFS) en el grafo dirigido.
        Devuelve una lista de nodos visitados.
        """
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(set(graph.neighbors(node)) - visited)
        return list(visited)

    def dijkstra(graph, source, target):
        """
        Devuelve el camino más corto y la distancia mínima entre dos nodos en un grafo dirigido.
        """
        try:
            path = nx.dijkstra_path(graph, source=source, target=target, weight='weight')
            distance = nx.path_weight(graph, path, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return [], float('inf')
    
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
        
class GraphVisualization:

    @staticmethod
    def draw_graph(graph, paint_shortest_paths=False, shortest_paths=None, save_path=None, show_plot=True):
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

        # Resaltar caminos más cortos si se proporciona
        if paint_shortest_paths and shortest_paths:
            colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
            for i, path in enumerate(shortest_paths):
                color = colors[i % len(colors)]
                edges_in_path = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(
                    graph, pos,
                    edgelist=edges_in_path,
                    edge_color=color,
                    width=3,
                    arrows=True
                )

        # Dibujar etiquetas de los pesos
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        if edge_labels:
            nx.draw_networkx_edge_labels(
                graph, pos, edge_labels=edge_labels,
                font_color='black', font_size=10,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
            )

        plt.axis('off')

        if save_path:
            plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight')
            print(f"✅ Grafo guardado en: {save_path}")

        if show_plot:
            plt.show()
        else:
            plt.close()