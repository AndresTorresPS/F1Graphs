import networkx as nx

def read_graph(graph_name):

    # Crea un grafo
    G = nx.Graph()

    # Crea un contador para informar al usuario cuántas aristas ha ingresado
    edges = 1

    # Proporciona instrucciones para ingresar aristas
    print(f"\nIntroduce una a una las aristas del grafo {graph_name} (formato: nodo1 nodo2). Escribe 'fin' para terminar:")

    # Ciclo que se ejecuta hasta que usuario ingresa 'fin'
    while True:

        # Ingreso de aristas por parte del usuario
        edge_string = input(f"Arista {edges} de {graph_name}: ")

        # Si el usuario ingresa 'fin', se construye el grafo con las aristas que el usuario ingresó antes de 'fin'
        if edge_string.lower() == 'fin':
            break

        # Añade la arista u,v (nodo1,nodo2) al grafo
        try:
            u, v = edge_string.strip().split()
            G.add_edge(u,v)
        except:
            print("Entrada no válida. Intenta con el formato: nodo1 nodo2")
        
        edges += 1

    # Devuelve el grafo construido a partir de las aristas ingresadas
    return G

def print_graph(graph_name, G):
    print(f"\nGrafo {graph_name}")
    print(f"Vértices: {sorted(G.nodes)}")
    print(f"Aristas: {sorted(G.edges)}")

def operate(G1, G2):

    U = nx.Graph()
    I = nx.Graph()
    D = nx.Graph()
    DS = nx.Graph()

    try:
        U = nx.compose(G1, G2)
    except Exception as e: 
        print(f"\nNo se pueden operar con Unión: {e}")

    try:
        I = nx.intersection(G1, G2)
    except Exception as e: 
        print(f"\nNo se pueden operar con Intersección: {e}")

    try:
        D = nx.difference(G1, G2)
    except Exception as e: 
        print(f"\nNo se pueden operar con Diferencia: {e}")

    try:
        DS = nx.symmetric_difference(G1, G2)
    except Exception as e: 
        print(f"\nNo se pueden operar con Diferencia Simétrica: {e}")

    return U, I, D, DS

def main():
    print("Operaciones de conjuntos con grafos (usando NetworkX)")
    G1 = read_graph("G1")
    G2 = read_graph("G2")

    print_graph("G1", G1)
    print_graph("G2", G2)

    U, I, D, DS = operate(G1,G2)

    print_graph("Unión (G1 U G2)", U)
    print_graph("Intersección (G1 ∩ G2)", I)
    print_graph("Diferencia (G1 - G2)", D)
    print_graph("Diferencia simétrica (G1 Δ G2)", DS)

if __name__ == "__main__":
    main()
