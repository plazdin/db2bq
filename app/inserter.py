import logging
from timeit import default_timer as dt

from database import dbm, bqo
from utils.argsp import get_pargs


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('NEW_TABLES')

def post_new_table(tabla: str) -> None:
    '''
    Add new tables to bigquery.
    Does require a unique arg with the name of the table
    '''

    start = dt()
    log.info(f'Extracting {tabla}')
    df1 = dbm.get_dbm_tabla(tabla.upper())
    log.info(f'Extraction finished in {dt() - start}. Begining poblate bd-sanjorge.SJ.{tabla}')
    start = dt()
    bqo.export(df1, f'bd-sanjorge.SJ.{tabla}', exists='replace')
    log.info(f'Finished in {dt() - start}.')


if __name__ == '__main__':
    args = get_pargs()

    for tabla in args:
        post_new_table(tabla)