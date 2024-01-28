import pandas as pd
from utils import download_all
from models import Entidad
from denue import DenueInegiClient

token = "tu-token--ver-portada-de-repositorio-para-instrucciones"

denue_inegi = DenueInegiClient(token)

download_all(
    denue_inegi.BuscarEntidad(
        condicion="Taller mecanico"
        ,entidad_federativa=Entidad.DISTRITO_FEDERAL
        ,registro_inicial=1
        ,registro_final=100),
    outfile="Talleres_Mecanicos_CDMX.csv"
)

df = pd.read_csv("Talleres_Mecanicos_CDMX.csv")
print(df.head())
