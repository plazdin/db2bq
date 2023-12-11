from timeit import default_timer

import pandas as pd

from config import Config
from database import bqo, gbq
from utils.consts import *
from utils.logger import Logger, timer_format
from utils.pd_utils import process_at_date_columns

conf = Config()

logger = Logger(__name__)
log = logger.get_logger()


def decode_cols(dbm_table: pd.DataFrame) -> None:
    '''
    Analyse all columns in the dataframe and, if any is in the list of
    columns to decode, it will be decoded to UTF-8.\n
    Param:
    -------
    - dbm_table: Dataframe to be decoded.
    '''
    for col in list(dbm_table.columns): 
        if col in cols_to_decode:
            dbm_table[col] = dbm_table[col].str.decode('utf-8')


def format_as_gbq_table(
    table_name: str,
    dbm_table: pd.DataFrame,
    in_kardur: bool = False) -> None:
    '''
    Takes 1 register from the table in BigQuery to get the dtypes and
    converts the dataframe dtypes.\n
    Params:
    -------
    - table_name: Table to be formated.
    - dbm_table: Dataframe of table.
    - in_kardur: If table is in kardur. Default is False.
    '''
    dataset = 'KARDUR' if in_kardur else 'SJ'
    bq_table = bqo.query(f"SELECT * from bd-sanjorge.{dataset}.{table_name} limit 1")
    dbm_table = dbm_table.astype(bq_table.dtypes.to_dict())
    del bq_table
    return dbm_table


def truncate_table(table_name: str, in_kardur: bool = False) -> None:
    '''
    Truncates the entire table in BigQuery.\n
    Params:
    -------
    - table_name: Table to be truncated.
    - in_kardur: boolean that tells if needs to be processed to kardur schema.
    '''
    log.info(f'Empieza TRUNCATE de {table_name}.')
    if conf.DEBUG:
        log.debug('returning from truncate.')
        return
    start = default_timer()
    
    try:
        bqo.query(f'truncate table bd-sanjorge.SJ.{table_name}')
        if in_kardur:
            bqo.query(f'truncate table bd-sanjorge.KARDUR.{table_name}')
        log.info(f'Truncate finalizado. Duración: {timer_format(default_timer() - start)}')
    except Exception as err:
        log.error(err)


def delete_table(table_name: str, in_kardur: bool = False) -> None:
    '''
    Deletes part of the table with specific filter, this in the dict filters.\n
    Params:
    -------
    - table_name: Table to be deleted.
    - in_kardur: boolean that tells if needs to be processed to kardur schema.
    '''
    log.info(f'Empieza Delete de {table_name}.')
    if conf.DEBUG:
        log.debug('returning from delete.')
        return
    start = default_timer()
    
    try:
        gbq.query(f'delete bd-sanjorge.SJ.{table_name} {filters[table_name]}')
        if in_kardur:
            gbq.query(f'delete bd-sanjorge.KARDUR.{table_name} {filters[table_name]}')
        log.info(f'Delete finalizado. Duración: {timer_format(default_timer() - start)}')
    except Exception as err:
        log.error(err)


def export_table(
    table_name: str,
    dbm_table: pd.DataFrame,
    in_kardur: bool) -> None:
    '''
    Exports the table to bigquery.\n
    Params:
    -------
    - table_name: Table to be exported.
    - dbm_table: Dataframe of table.
    - in_kardur: boolean that tells if needs to be processed to kardur schema.
    '''
    start = default_timer()
    log.info(f'Insertando registros nuevos a {table_name}.')
    if conf.DEBUG:
        log.debug('returning from export.')
        return
    
    if in_kardur:
        dbm_table = format_as_gbq_table(table_name, dbm_table, in_kardur)
        bqo.export(
            dbm_table, f'bd-sanjorge.KARDUR.{table_name}', exists='append')
    
    if table_name == 'AUTOS':
        dbm_table = process_at_date_columns(dbm_table)
    
    dbm_table = format_as_gbq_table(table_name, dbm_table)
    bqo.export(dbm_table, f'bd-sanjorge.SJ.{table_name}', exists='append')
    
    total_time = timer_format(default_timer() - start)
    log.info(f'Operación finalizada. Duración: {total_time}')
