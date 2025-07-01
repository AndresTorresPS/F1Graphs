import pandas as pd
from F1Utils.graphs_utils import GraphCreation, GraphAnalysis, GraphVisualization

class F1Graphs:

    # Leer la matriz de adyacencia desde el archivo CSV (incluyendo encabezados)
    csv_file = 'F1Data/mark_01.csv'
    adjacency_df = pd.read_csv(csv_file, index_col=0)

    # Crear el grafo dirigido y ponderado
    mark_01_graph = GraphCreation.di_weighted_graph(adjacency_df)

    # Imprime los caminos más cortos y la distancia mínima entre 'Start' y 'End'
    start_node = 'Start'
    target_node = 'End'
    shortest_paths, shortest_distance = GraphAnalysis.all_shortest_paths(mark_01_graph, start_node, target_node)
    print(f"Graph created from {csv_file}")
    print(f"Shortest paths from {start_node} to {target_node} using Dijkstra: {shortest_paths}\nShortest distance: {shortest_distance}")

    # Imprime el grafo con los caminos resaltados
    GraphVisualization.draw_graph(mark_01_graph, paint_shortest_paths=True, shortest_paths=shortest_paths)




    
