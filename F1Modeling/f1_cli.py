import os
import shlex
import importlib.util
from f1_graphs.f1_graph_modeling import F1Graph

def print_help():
    print("""
  COMANDOS DISPONIBLES:

  create graph <archivo.csv>       → Guarda el PNG del grafo
  optimize <archivo.csv>           → Identifica y guarda camino(s) más corto(s) y PNG del grafo optimizado
  simulate <archivo.py>            → Ejecuta una simulación 2D del archivo indicado
  help                             → Muestra COMANDOS DISPONIBLES
  exit                             → Para salir del programa
    """)

def simulate_py_file(filename):
    """
    Ejecuta un archivo Python de simulación ubicado en f1_sim/.
    """
    filepath = os.path.join("f1_sim", filename)

    if not os.path.isfile(filepath):
        print(f"❌ Archivo no encontrado: {filepath}")
        return

    try:
        print(f"🏁 Ejecutando simulación: {filename}")
        spec = importlib.util.spec_from_file_location("f1_simulation_module", filepath)
        sim_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sim_module)
        print("✅ Simulación finalizada correctamente.\n")
    except Exception as e:
        print(f"❌ Error al ejecutar la simulación: {e}\n")

def cli_main():
    print("🚀 Bienvenido a F1Graphs CLI. Escribe 'help' para ver los comandos disponibles.")

    while True:
        try:
            command = input(">>> ").strip()
            parts = shlex.split(command)

            if not parts:
                continue

            if parts[0].lower() == 'exit':
                print("👋 Saliendo de F1Graphs CLI.")
                break

            elif parts[0].lower() == 'help':
                print_help()

            elif parts[0].lower() == 'create' and len(parts) == 3 and parts[1].lower() == 'graph':
                filename = parts[2]
                F1Graph.create_graph(filename)

            elif parts[0].lower() == 'optimize' and len(parts) == 2:
                filename = parts[1]
                F1Graph.optimize(filename)

            elif parts[0].lower() == 'simulate' and len(parts) == 2 and parts[1].endswith('.py'):
                simulate_py_file(parts[1])

            else:
                print("❌ Comando no reconocido. Escribe 'help' para ver las opciones.")

        except KeyboardInterrupt:
            print("\n❌ Interrupción del usuario. Escribe 'exit' para salir.")
        except Exception as e:
            print(f"⚠️ Error al procesar el comando: {e}")

if __name__ == "__main__":
    cli_main()
