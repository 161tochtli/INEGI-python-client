from enum import Enum

class Entidad(Enum):
    """
    Enumeration representing the entity federative codes in Mexico as per INEGI's data.

    The values are the codes corresponding to each entity federative in Mexico.

    Examples:
        entidad_code = Entidad.SINALOA.code
    """

    AGUASCALIENTES = '01'
    BAJA_CALIFORNIA = '02'
    BAJA_CALIFORNIA_SUR = '03'
    CAMPECHE = '04'
    COAHUILA_DE_ZARAGOZA = '05'
    COLIMA = '06'
    CHIAPAS = '07'
    CHIHUAHUA = '08'
    DISTRITO_FEDERAL = '09'
    DURANGO = '10'
    GUANAJUATO = '11'
    GUERRERO = '12'
    HIDALGO = '13'
    JALISCO = '14'
    MEXICO = '15'
    MICHOACAN_DE_OCAMPO = '16'
    MORELOS = '17'
    NAYARIT = '18'
    NUEVO_LEON = '19'
    OAXACA = '20'
    PUEBLA = '21'
    QUERETARO_DE_ARTEAGA = '22'
    QUINTANA_ROO = '23'
    SAN_LUIS_POTOSI = '24'
    SINALOA = '25'
    SONORA = '26'
    TABASCO = '27'
    TAMAULIPAS = '28'
    TLAXCALA = '29'
    VERACRUZ_DE_IGNACIO_DE_LA_LLAVE = '30'
    YUCATAN = '31'
    ZACATECAS = '32'
    ENTIDAD_FEDERATIVA_NO_ESPECIFICADA = '33'

    @property
    def code(self):
        return self.value

    @classmethod
    def normalize(cls, entidad):
        if isinstance(entidad, cls):
            entidad = entidad.code
        elif isinstance(entidad, str):
            entidad = entidad.zfill(2)
        elif isinstance(entidad, int):
            entidad = str(entidad).zfill(2)
        else:
            raise ValueError(f"Invalid type for entidad_federativa: {type(entidad)}")
        return entidad

