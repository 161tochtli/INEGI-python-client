import pandas as pd
from models import Entidad
from denue import DenueInegiClient

# Escribe tu token. Para obtenerlo, ingresa a: https://www.inegi.org.mx/app/api/denue/v1/tokenVerify.aspx
token = "mi-token-valido"

# Aqui deteminamos que queremos utilizar los datos de Denue
denue_inegi = DenueInegiClient(token)

# Aquí es donde escribimos la consulta deseada de acuerdo a los parámetros definidos en
# https://www.inegi.org.mx/servicios/api_denue.html#introduccion
# Por ejemplo, utilizando "BuscarEntidad":
consulta = denue_inegi.BuscarEntidad(condicion="Taller mecanico", registro_inicial=1, registro_final=10, entidad_federativa=Entidad.DISTRITO_FEDERAL)

# Nota: Para determinar la entidad federativa, puedes utilizar "Entidad.nombre_de_la_entidad". La lista de nombres de entidades
# válidos la puedes encontrar en la portadad del repositorio


# Aquí obtenemos los datos de la consulta.
# Existen dos métodos para obtener los datos, como un dataframe de pandas o como un archivo csv:
# 1. Como un dataframe de Pandas
df = consulta.to_pandas()
# 2. Como un archivo CSV (ventaja: Puedes descargar más datos y luego cargarlos a un dataframe)
# Descarga simple (solo los datos entre "registro_inicial" y "registro_final")
consulta.to_csv(outfile="mi_consulta.csv")
# Descarga completa (todos los datos disponibles)
consulta.to_csv(outfile="data_completa.csv", download_all=True)

# Además, si quieres que se genere un nombre de archivo por ti, puedes solo especificar el nombre de la carpeta en
# donde quieres guardar los datos, y la ruta al archivo se guardará en outfile.
outfile = consulta.to_csv(folder="../data/")#, download_all=True)
df = pd.read_csv(outfile) # Cargamos los datos a un dataframe
# Nota: Se recomienda utilizar la descarga simple para probar las consultas antes de realizar una descarga completa.
