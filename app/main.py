from timeit import default_timer
import os
import warnings

import pandas as pd

from config import Config
from crud.bigquery import (
    decode_cols,
    truncate_table,
    delete_table,
    export_table,
    logger as bqlog)
from database import dbm
from utils.argsp import get_pargs
from utils.consts import kardur_tables, filters
from utils.logger import Logger


warnings.filterwarnings('ignore')#, category=UserWarning)
conf = Config()
logger = Logger(__name__)
log = logger.get_logger()


def main_operation(table_name: str, cols: list = None):
    '''
    Main function to syncronize all tables.\n
    Param:
    ------
    - table_name: name of the table to be synchronized.
    - cols: a list of columns that going to be extracted.
    '''    
    log_file = os.path.join(conf.LOG_PATH, table_name)
    logger.file_handler_attacher(log_file)
    bqlog.file_handler_attacher(log_file)

    in_kardur = True if table_name in kardur_tables else False
    log.info(f'Empieza extracción de {table_name}.')
    cols_str = '*' if not cols else ','.join(cols)
    filtr = '' if not table_name in filters else filters[table_name]
    
    dbm_table = dbm.query('''
        SELECT %s from "SYSADM"."%s" %s
        ''' % (cols_str, table_name, filtr))    
    
    if not isinstance(dbm_table, pd.DataFrame):
        log.error(f'{table_name} no pudo ser extraida. \
            Verifique que exista o que posea los permisos necesarios.')
        return
    
    decode_cols(dbm_table)

    if filtr == '':
        truncate_table(table_name, in_kardur)
    else:
        delete_table(table_name, in_kardur)

    export_table(table_name, dbm_table, in_kardur)
    del dbm_table

if __name__ == '__main__':

    if conf.DEBUG == True:
        log.debug('DEMO!!, no se van a ejecutar comandos reales de SQL.')
    
    bq_tables = get_pargs()
    
    for table in bq_tables:
        start = default_timer()
        cols = None
        try:
            if table == 'AUTOS8':
                cols = ['AT8_COAUTO',
			'AT8_FECHA',
			'AT8_HORA',
			'AT8_MOTIVO',
			'AT8_USUARIO'
		]
            main_operation(table, cols)
            log.info(f'{table} finalizado. Duración: {default_timer() - start:.2f} segundos.\
                \n-----------------------------------------------------------')
        except Exception as err:
            log.error(f'No se pudo procesar: {err}\
                \n-----------------------------------------------------------')
        
