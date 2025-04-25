import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1️⃣ Datos ficticios de posiciones por vuelta
datos_vueltas = [
    (1, 5), (2, 4), (3, 3), (4, 3), (5, 2), (6, 2), (7, 2), (8, 4), (9, 5), 
    (10, 6), (11, 6), (12, 5), (13, 4), (14, 3), (15, 3)
]

# 2️⃣ Convertir a DataFrame
df = pd.DataFrame(datos_vueltas, columns=["Vuelta", "Posición"])
df.to_csv("norris_2024_australia_posiciones_ficticio.csv", index=False, encoding="utf-8")
print(f"📂 Datos ficticios guardados en norris_2024_australia_posiciones_ficticio.csv")

# 3️⃣ Construcción del grafo
G = nx.DiGraph()  # Grafo dirigido

for i in range(len(df) - 1):
    vuelta_actual = f"Vuelta {df.iloc[i]['Vuelta']}"
    vuelta_siguiente = f"Vuelta {df.iloc[i + 1]['Vuelta']}"
    cambio_pos = df.iloc[i + 1]['Posición'] - df.iloc[i]['Posición']  # Positivo si perdió posiciones

    G.add_edge(vuelta_actual, vuelta_siguiente, weight=abs(cambio_pos))

# 4️⃣ Visualización del grafo
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)  # Disposición visual del grafo
edges = G.edges(data=True)
edge_weights = [d['weight'] for (_, _, d) in edges]

nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=8, width=edge_weights)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("📊 Cambios de Posición de Norris en Australia (Datos Ficticios)")
plt.show()

# 5️⃣ Análisis de la carrera
print(f"📊 Análisis de la carrera ficticia de Norris en Australia:")
print(f"- Posición inicial: {df.iloc[0]['Posición']}°")
print(f"- Posición final: {df.iloc[-1]['Posición']}°")
print(f"- Mayor avance en una vuelta: {df['Posición'].diff().min()} posiciones")
print(f"- Mayor pérdida en una vuelta: {df['Posición'].diff().max()} posiciones")
