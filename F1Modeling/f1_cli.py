from f1_graphs.f1_graph_modeling import F1Graph

def print_help():
    print("""
  COMANDOS DISPONIBLES:

  create graph <archivo.csv>       → Guarda el PNG del grafo
  optimize <archivo.csv>           → Identifica y guarda camino(s) más corto(s) y PNG del grafo optimizado
  help                             → Muestra COMANDOS DISPONIBLES
  exit                             → Para salir del programa
    """)

def cli_main():
    print("🚀 Bienvenido a F1Graphs CLI. Escribe 'help' para ver los comandos disponibles.")

    while True:
        try:
            command = input(">>> ").strip()

            if command.lower() == 'exit':
                print("Saliendo de F1Graphs CLI.")
                break

            elif command.lower() == 'help':
                print_help()

            elif command.lower().startswith("create graph"):
                parts = command.split()
                if len(parts) == 3 and parts[2].endswith('.csv'):
                    F1Graph.create_graph(parts[2])
                else:
                    print("Comando no reconocido Prueba con: create graph archivo.csv")

            elif command.lower().startswith("optimize"):
                parts = command.split()
                if len(parts) == 2 and parts[1].endswith('.csv'):
                    F1Graph.optimize(parts[1])
                else:
                    print("Comando no reconocido. Prueba con: optimize archivo.csv")

            else:
                print("Comando no reconocido. Escribe 'help' para ver las opciones.")

        except KeyboardInterrupt:
            print("\nInterrupción del usuario. Escribe 'exit' para salir.")
        except Exception as e:
            print(f"Error al procesar el comando: {e}")

if __name__ == "__main__":
    cli_main()
