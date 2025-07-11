import pandas as pd
from f1_graphs.f1_graphs_utils.graphs_utils import GraphCreation, GraphAnalysis, GraphVisualization
import os

class F1Graph:
    input_dir = "f1_data/"
    output_dir = 'f1_output/graphs_models'

    @staticmethod
    def create_graph(filename):
        """
        Crea y guarda la imagen de un grafo dirigido y ponderado desde un archivo CSV.
        No calcula caminos más cortos.
        """
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_dir = 'f1_output/graphs_models'
        os.makedirs(output_dir, exist_ok=True)

        # Cargar el archivo CSV
        adjacency_df = pd.read_csv(F1Graph.input_dir+filename, index_col=0)
        graph = GraphCreation.di_weighted_graph(adjacency_df)

        # Ruta para guardar la imagen
        image_path = os.path.join(output_dir, f'{base_name}.png')

        # Dibujar y guardar el grafo sin rutas resaltadas
        GraphVisualization.draw_graph(
            graph,
            paint_shortest_paths=False,
            save_path=image_path,
            show_plot=False
        )
        print(f"✅ PNG del grafo guardado en {image_path}")

    @staticmethod
    def optimize(filename, start_node='Start', target_node='End'):
        """
        Calcula los caminos más cortos desde un archivo CSV de adyacencia,
        guarda la imagen del grafo con rutas resaltadas,
        y exporta los resultados a archivos CSV.
        """
        base_name = os.path.splitext(os.path.basename(filename))[0]
        os.makedirs(F1Graph.output_dir, exist_ok=True)

        # Cargar el archivo CSV
        adjacency_df = pd.read_csv(F1Graph.input_dir+filename, index_col=0)
        graph = GraphCreation.di_weighted_graph(adjacency_df)

        # Calcular los caminos más cortos
        shortest_paths, shortest_distance = GraphAnalysis.all_shortest_paths(graph, start_node, target_node)

        # Guardar la imagen con caminos resaltados
        optimized_image_path = os.path.join(F1Graph.output_dir, f'{base_name}_optimized.png')
        GraphVisualization.draw_graph(
            graph,
            paint_shortest_paths=True,
            shortest_paths=shortest_paths,
            save_path=optimized_image_path,
            show_plot=False
        )

        # Guardar los caminos más cortos en CSV
        paths_csv_path = os.path.join(F1Graph.output_dir, f'{base_name}_optimal_paths.csv')
        paths_df = pd.DataFrame({'Optimal Paths': [' >>> '.join(path) for path in shortest_paths]})
        paths_df.to_csv(paths_csv_path, index=False)

        # Guardar la distancia mínima en CSV
        dist_csv_path = os.path.join(F1Graph.output_dir, f'{base_name}_optimal_solution.csv')
        dist_df = pd.DataFrame({'Optimal solution': [shortest_distance]})
        dist_df.to_csv(dist_csv_path, index=False)

        print(f"✅ Caminos óptimos guardados en {paths_csv_path}")
        print(f"✅ Solución óptima guardada en {dist_csv_path}")
        print(f"✅ PNG del grafo optimizado guardada en {optimized_image_path}")