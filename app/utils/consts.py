from datetime import date
from pprint import pprint


anio = date.today().strftime('%Y')
last_year = int(anio[2:]) - 1
anio_nc = (f'{last_year}0101')
filters = {
    "AUTOS": "where AT_COAUTO > 120000",
    "CONT": f"where CT_ANIO in ({int(anio)-1}, {int(anio)})",
    "VALECONS": f"where VC_FECHA >= {int(f'{anio}0101')}",
    "CTACTE":  f"where CC_FECHOP >= {int(f'{anio}0101')}",
    "TURNOTAL": f"where TURT_FECHA3 >= {int(anio_nc)}"
}

cols_to_decode = [
    'ART_LET_ULTCOM', 'ART_LET_ULTVEN', 'AT_INF_DOM',
    'AT_USO', 'CT_SUBDIARIO', 'PL_IBRMO', 'VC_MATERIALES'
]

kardur_tables = [
    'AUTOS','AUTOS1', 'USADOS1',
    'RESERVA', 'DEPOSITO', 'CLAAUTOS'
]

at_date_columns = ['AT_FECASIGNA',
 'AT_FECHAS_10',
 'AT_ANIOFAB',
 'AT_FECOMP',
 'AT_FECPAGO',
 'AT_FECPRO',
 'AT_FECREM',
 'AT_FEEMICE',
 'AT_FECFAC',
 'AT_FECHAS_6',
 'AT_FECRES',]
