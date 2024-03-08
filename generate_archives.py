import json

def generar_archivos_json(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
        for i, registro in enumerate(data):
            # Generar un nuevo nombre de archivo para cada registro
            nombre_archivo = f'registros/registro_{i+1}.json'
            # Escribir el registro actual en un nuevo archivo JSON
            with open(nombre_archivo, 'w') as nuevo_archivo:
                json.dump(registro, nuevo_archivo, indent=4)

# Nombre del archivo JSON que contiene el array de registros
archivo_json = './registros/confluence_spaces.json'

# Llamar a la función para generar los archivos JSON
generar_archivos_json(archivo_json)