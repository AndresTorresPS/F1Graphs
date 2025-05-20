# 🏎️ F1Graphs

Este proyecto está diseñado para aprender a modelar, analizar y simular estrategias de carrera de monoplazas desde la teoría de grafos, incluyendo paradas en pits, tipos de neumáticos, adelantamientos, entre otros.

* APIs/: Tutorial para acceder a fuentes de datos públicas sobre la Fórmula 1.
* F1Modeling/: Simulador 2D de carreras de Fórmula 1 en `pygame` a partir de modelos de grafos dirigidos ponderados. 
* GraphTheory/: Resumen del libro de teoría de grafos de Diestel con ejemplos prácticos.

---

## 🖐️ Arquitectura de F1Modeling

Este proyecto fue construido bajo los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**. Cada componente está separado por su responsabilidad principal, facilitando mantenimiento, pruebas y escalabilidad.

```
F1Modeling/
│
├── F1Data/                       # 📊 CSVs con matrices de adyacencia
│
├── F1Graphs/                     # 🔍 Módulo de modelado con grafos
│   ├── f1_graphs.py                # Modelamiento de carreras de F1 con grafos
│   ├── F1Utils/                
│       └── graphs_utils.py           # Contiene herramientas de modelado con grafos
│
├── F1Simulation/                 # 🎮 Módulo de simulación 2D con Pygame
│   ├── f1_race_logic.py            # Contiene la lógica de los modelos de carrera
│   ├── f1_race.py                  # Controla el flujo de carrera
│   ├── F1Utils/                    
│       └── race_utils.py             # Contiene componentes de simulación
│
├── F1Test/                       # ✅ Módulo de pruebas unitarias con pytest
│   ├── test_graphs_utils.py
|   ├── test_race_utils.py
│
├── f1_config.py                  # ⚙️ Configuraciones generales de la aplicación
├── f1_doc.ipynb                  # 📝 Documentación detallada
├── f1_main.py                    # 🔁 Orquesta lectura, lógica, simulación y testing
├── README.md                     # 📝 Este archivo
└── requirements.txt              # 📦 Dependencias
```

---

## 🚀 Funcionalidades principales

* Lectura de matrices de adyacencia desde archivos `csv`
* Construcción de grafos dirigidos con pesos usando `networkx`
* Visualización de diferentes caminos posibles con `matplotlib`
* Cálculo de caminos más cortos
* Simulación 2D de una carrera con `pygame`
* Validación entre los resultados por medio de grafos y usando simulador
* Toolbox adaptable de Pygame para expandir la aplicación
* Pruebas unitarias con `pytest`

---

## 🛠️ Requisitos

`python 3.10+` `pygame` `networkx` `pandas` `pytest` `matplotlib`

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo ejecutar

```bash
python f1_main.py
```

---

## 🧪 Ejecutar tests

```bash
pytest tests/
```

---

## 📍 Autor

**Jaime Andrés Torres Duque**

Aspirante al título de Ingeniero de Software.

Contacto = { 
institucional: jandrestorres@poligran.edu.co, 
personal: jaimetodu@hotmail.com
}
