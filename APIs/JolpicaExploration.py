import requests
import pandas as pd

# Definir el año y el nombre del piloto
anio = 2024
nombre_piloto = "hamilton"

# URL de la API de Jolpica
url = f"https://api.jolpi.ca/ergast/f1/{anio}/drivers/{nombre_piloto}/results.json"
respuesta = requests.get(url)

# Verificar si la solicitud fue exitosa
if respuesta.status_code == 200:
    datos = respuesta.json()
    
    # Lista para almacenar los datos
    resultados = []
    
    # Recorrer las carreras y extraer los datos
    for carrera in datos['MRData']['RaceTable']['Races']:
        nombre_carrera = carrera['raceName']
        fecha = carrera['date']
        posicion = carrera['Results'][0]['position']
        tiempo = carrera['Results'][0].get('Time', {}).get('time', 'N/A')  # Manejo de tiempo no disponible
        
        resultados.append([nombre_carrera, fecha, posicion, tiempo])
    
    # Crear un DataFrame con pandas
    df = pd.DataFrame(resultados, columns=["Carrera", "Fecha", "Posición Final", "Tiempo Final"])
    
    # Guardar el DataFrame en un archivo CSV
    nombre_archivo = f"hamilton_{anio}_resultados.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8')
    
    print(f"Datos guardados en {nombre_archivo}")
else:
    print(f"Error al obtener los datos: {respuesta.status_code}")
