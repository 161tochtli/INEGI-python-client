# Descarga datos del INEGI utilizando Python

En el archivo [**_ejemplo.py_**](ejemplos/ejemplo.py) dentro de la carpeta **_ejemplos_** puedes encontrar un tutorial básico sobre el uso  de este este repositorio.
La mayor parte de los usuarios encontrarán en ese archivo el código que necesitan para guiarse en la descarga de los datos.


El siguinte código ejemplifica como descargar todos los datos para una consulta de tipo "BuscarEntidad" del DENUE:

```python
from denue import DenueInegiClient

token='mi-token'
denue_inegi = DenueInegiClient(token)
consulta = denue_inegi.BuscarEntidad(condicion="Taller mecanico", entidad_federativa="09")
consulta.to_csv(outfile="data_talleres_mecanicos.csv", download_all=True)
```

[Obtener token](https://www.inegi.org.mx/app/api/denue/v1/tokenVerify.aspx)


Puedes utilizar cualquiera de las consultas de los [catálogos disponibles](#inegi.catalogos_disponibles). Solo sustituye "BuscarEntidad" y añade los parámetros correspondientes.  


<a id="inegi.catalogos_disponibles"></a>
### Catálogos disponibles

[DENUE](#denue)

---

<a id="denue"></a>
### DENUE: Directorio Estadístico Nacional de Unidades Económicas
Ofrece los datos de identificación, ubicación, actividad económica y tamaño de más de 5 millones de unidades económicas activas en el territorio nacional.

  * [DenueInegiClient](#denue.DenueInegiClient)
    * [Buscar](#denue.DenueInegiClient.Buscar)
    * [Ficha](#denue.DenueInegiClient.Ficha)
    * [Nombre](#denue.DenueInegiClient.Nombre)
    * [BuscarEntidad](#denue.DenueInegiClient.BuscarEntidad)
    * [BuscarAreaAct](#denue.DenueInegiClient.BuscarAreaAct)
    * [BuscarAreaActEstr](#denue.DenueInegiClient.BuscarAreaActEstr)
    * [Cuantificar](#denue.DenueInegiClient.Cuantificar)

[Más información](https://www.inegi.org.mx/servicios/api_denue.html) (Pestaña "Guía para desarrolladores")

<a id="denue.DenueInegiClient"></a>

### DenueInegiClient

```python
class DenueInegiClient()
```

<a id="denue.DenueInegiClient.Buscar"></a>

### Buscar

```python
def Buscar(condicion: str = "todos",
           coordenadas: tuple = (19.42847, -99.12766),
           distancia: int = 5000,
           match_type: str = "any") -> Result
```

Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas.

**Parámetros:**

condicion (str, optional): Palabra(s) a buscar en el nombre del establecimiento, razón social,
calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad.
Para buscar todos los establecimientos, se deberá ingresar la palabra "todos". Para buscar
con más de una palabra clave, separar las palabras por espacios y utilizar el parámetro
match_type para indicar el tipo de coincidencia.
Valor por defecto es "todos".

coordenadas (tuple, optional): Par de coordenadas que definen el punto en el mapa a partir
del cual se hará la consulta alrededor. El formato de las coordenadas es latitud y longitud.
Valor por defecto es (0.0, 0.0).

distancia (int, optional): Cantidad de metros a partir de las coordenadas que definen el radio
de búsqueda. La distancia máxima es de 5 000 metros. Valor por defecto es 5000.
match_type (str): Tipo de coincidencia en las palabras a buscar en condicion. Si "any" entonces
devuelve todos los registros en los que coincida al menos una palabra en condicion. Si "all" entonces
devuelve todos los registros en los que coincidan todas las palabras en condicion. Cualquier match_type
no reconocido se considera "any".
Valor por defecto es "any".

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.Ficha"></a>

### Ficha

```python
def Ficha(id_establecimiento: str) -> Result
```

Obtiene la información de un establecimiento en específico.

**Parámetros:**

id_establecimiento (str): Clave única del establecimiento.

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.Nombre"></a>

### Nombre

```python
def Nombre(nombre_o_razon_social: str,
           entidad_federativa: str | Entidad = "00",
           registro_inicial: int = 1,
           registro_final: int = 10,
           match_type: str = "all") -> PaginatedResult
```

Realiza una consulta de todos los establecimientos por nombre o razón social y
puede ser acotado por entidad federativa.

**Parámetros:**

nombre_o_razon_social (str): Palabra(s) a buscar que se encuentran en el nombre
del establecimiento o la razón social.

entidad_federativa (str | Entidad, optional): Clave de dos dígitos de la entidad federativa
(01 a 32). Para incluir todas las entidades se especifica 00.
Valor por defecto es "00".

registro_inicial (int, optional): Número de registro a partir del cuál se mostrarán
los resultados de la búsqueda. Valor por defecto es 1.

registro_final (int, optional): Número de registro final que se mostrará en los
resultados de la búsqueda. Valor por defecto es 10.

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.BuscarEntidad"></a>

### BuscarEntidad

```python
def BuscarEntidad(condicion: str = "todos",
                  entidad_federativa: str | Entidad = "00",
                  registro_inicial: int = 1,
                  registro_final: int = 10,
                  match_type: str = "default") -> PaginatedResult
```

Realiza una consulta de todos los establecimientos y puede ser acotada por entidad federativa.

**Parámetros:**

condicion (str, optional): Palabra(s) a buscar en el nombre del establecimiento, razón social,
calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad.
Para buscar todos los establecimientos, se deberá ingresar la palabra "todos". Para buscar
con más de una palabra clave, separar las palabras por espacios y utilizar el parámetro
match_type para indicar el tipo de coincidencia.
Valor por defecto es "todos".

entidad_federativa (str | Entidad, optional): Clave de dos dígitos de la entidad federativa
(01 a 32). Para incluir todas las entidades se especifica 00.
Valor por defecto es "00".

registro_inicial (int, optional): Número de registro a partir del cuál se mostrarán
los resultados de la búsqueda. Valor por defecto es 1.

registro_final (int, optional): Número de registro final que se mostrará en los
resultados de la búsqueda. Valor por defecto es 10.

match_type (str): Tipo de coincidencia en las palabras a buscar en condicion.
Si "default" entonces devuelve una búsqueda tomando en cuenta los espacios.
Si "any" entonces devuelve todos los registros en los que coincida al menos una palabra en condicion.
Si "all" entonces devuelve todos los registros en los que coincidan todas las palabras en condicion.
Cualquier valor no reconocido en match_type se considera "default".
Valor por defecto es "default".

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.BuscarAreaAct"></a>

### BuscarAreaAct

```python
def BuscarAreaAct(condicion: str = "todos",
                  entidad_federativa: str | Entidad = "00",
                  registro_inicial: int = 1,
                  registro_final: int = 10,
                  match_type: str = "any") -> PaginatedResult
```

Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda
por área geográfica, actividad económica, nombre y clave del establecimiento.

**Parámetros:**

condicion (str, optional): Palabra(s) a buscar en el nombre del establecimiento, razón social,
calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad.
Para buscar todos los establecimientos, se deberá ingresar la palabra "todos". Para buscar
con más de una palabra clave, separar las palabras por espacios y utilizar el parámetro
match_type para indicar el tipo de coincidencia.
Valor por defecto es "todos".

entidad_federativa (str | Entidad, optional): Clave de dos dígitos de la entidad federativa
(01 a 32). Para incluir todas las entidades se especifica 00.
Valor por defecto es "00".

registro_inicial (int, optional): Número de registro a partir del cuál se mostrarán
los resultados de la búsqueda. Valor por defecto es 1.

registro_final (int, optional): Número de registro final que se mostrará en los
resultados de la búsqueda. Valor por defecto es 10.

match_type (str): Tipo de coincidencia en las palabras a buscar en condicion. Si "any" entonces
devuelve todos los registros en los que coincida al menos una palabra en condicion. Si "all" entonces
devuelve todos los registros en los que coincidan todas las palabras en condicion. Cualquier match_type
no reconocido se considera "any".
Valor por defecto es "any".

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.BuscarAreaActEstr"></a>

### BuscarAreaActEstr

```python
def BuscarAreaActEstr(entidad_federativa: str | Entidad = "00",
                      municipio: str = "0",
                      localidad: str = "0",
                      ageb: str = "0",
                      manzana: str = "0",
                      sector: str = "0",
                      subsector: str = "0",
                      rama: str = "0",
                      clase: str = "0",
                      nombre_del_establecimiento: str = "0",
                      registro_inicial: int = 1,
                      registro_final: int = 10,
                      id_establecimiento: str = "0",
                      estrato: str = "0") -> PaginatedResult
```

Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda por
área geográfica, actividad económica, nombre, clave del establecimiento y estrato.

**Parámetros:**

entidad_federativa (str | Entidad, optional): Clave de dos dígitos de la entidad federativa (01 a 32).
Para incluir todas las entidades se especifica 00. Valor por defecto es "00".

municipio (str, optional): Clave de tres dígitos del municipio (ej. 001).
Para incluir todos los municipios se especifica 0. Valor por defecto es "0".

localidad (str, optional): Clave de cuatro dígitos de la localidad (ej. 0001).
Para incluir todas las localidades se especifica 0. Valor por defecto es "0".

ageb (str, optional): Clave de cuatro dígitos AGEB (ej. 2000).
Para incluir todas las AGEBS se especifica 0. Valor por defecto es "0".

manzana (str, optional): Clave de tres dígitos de la manzana (ej. 043).
Para incluir todas las manzanas se especifica 0. Valor por defecto es "0".

sector (str, optional): Clave de dos dígitos del sector de la actividad económica (ej. 46).
Para incluir todos los sectores se especifica 0. Valor por defecto es "0".

subsector (str, optional): Clave de tres dígitos del subsector de la actividad económica ( ej. 464 ).
Para incluir todos los subsectores se especifica 0. Valor por defecto es "0".

rama (str, optional): Clave de cuatro dígitos de la rama de la actividad económica (ej. 4641 ).
Para incluir todas las ramas se especifica 0. Valor por defecto es "0".

clase (str, optional): Clave de seis dígitos de la clase (ej. 464112 ).
Para incluir todas las actividades se especifica 0. Valor por defecto es "0".

nombre_del_establecimiento (str, optional): Nombre del establecimiento a buscar.
Para incluir todos los establecimientos se especifica 0. Valor por defecto es "0".

registro_inicial (str, optional): Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
Valor por defecto es "0".

registro_final (str, optional): Número de registro final que se mostrará en resultados de la búsqueda.
Valor por defecto es "0".

id (str, optional): Clave única del establecimiento.
Para incluir todos los establecimientos se especifica 0. Valor por defecto es "0".

estrato (str, optional): Clave de un dígito del estrato.
Para incluir todos los tamaños se especifica 0.
1. Para incluir de 0 a 5 personas.
2. Para incluir de 6 a 10 personas.
3. Para incluir de 11 a 30 personas.
4. Para incluir de 31 a 50 personas.
5. Para incluir de 51 a 100 personas.
6. Para incluir de 101 a 250 personas.
7. Para incluir de 251 y más personas.
Valor por defecto es "0".

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.

<a id="denue.DenueInegiClient.Cuantificar"></a>

### Cuantificar

```python
def Cuantificar(actividad_economica: str = "0",
                area_geografica: str = "0",
                estrato: str = "0") -> Result
```

Realiza un conteo de todos los establecimientos con la opción de acotar la búsqueda por
área geográfica, actividad económica y estrato.

**Parámetros:**

actividad_economica (str, optional): Clave de dos a seis dígitos de la actividad económica.
Para considerar más de una clave deberás separarlas con coma.
Para incluir todas las actividades se especifica 0.
Dos dígitos para incluir nivel sector (ej.46).
Tres dígitos para incluir nivel subsector (ej. 464).
Cuatro dígitos para incluir nivel rama (ej. 4641).
Cinco dígitos para incluir nivel subrama (ej. 46411).
Seis dígitos para incluir nivel clase (ej. 464111).
Valor por defecto es "0".

area_geografica (str, optional): Clave de dos a nueve dígitos del área geográfica.
Para considerar más de una clave deberás separarlas con coma.
Para incluir todo el país se especifica 0.
Dos dígitos para incluir nivel estatal (ej.01 a 32).
Cinco dígitos dígitos para incluir nivel municipal (ej. 01001).
Nueve dígitos para incluir nivel localidad (ej. 010010001).
Valor por defecto es "0".

estrato (str, optional): Clave de un dígito del estrato.
Para incluir todos los tamaños se especifica 0.
1. Para incluir de 0 a 5 personas.
2. Para incluir de 6 a 10 personas.
3. Para incluir de 11 a 30 personas.
4. Para incluir de 31 a 50 personas.
5. Para incluir de 51 a 100 personas.
6. Para incluir de 101 a 250 personas.
7. Para incluir de 251 y más personas.
Valor por defecto es "0".

**Returns**:

- `response` _requests.Response_ - Respuesta de la solicitud a la API.
