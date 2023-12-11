
# pylint: disable = C0114, C0115, C0116, R0903
from google.oauth2.service_account import Credentials
from google.cloud import bigquery
import pandas_gbq as pdg
import pandas as pd
from config import Config
from utils.logger import Logger


log = Logger(__name__).get_logger()


class BigQuery:
    
    def __init__(self) -> None:
        try:
            self._conf = Config()
            self._cred = Credentials.from_service_account_file(self._conf.JSONPATH)
        except Exception as err:
            log.error(err)
    
    def query(self, query):
        client = bigquery.Client(
            credentials=self._cred,
            project='bd-sanjorge',)
        job = client.query(query)
        log.info(f'Query iniciada como {job.job_id}.')
        job.result()


class BQObject:

    def __init__(self) -> None:
        try:
            log.info('Iniciando conexión con BigQuery.')
            self._conf = Config()
            self._cred = Credentials.from_service_account_file(self._conf.JSONPATH)
        except Exception as err:
            log.error(err)


    def get_sj_tabla(self, tabla: str) -> pd.DataFrame:
        query = "SELECT * FROM `bd-sanjorge`.SJ.%s" % tabla
        dataframe = pdg.read_gbq(
            query, project_id='bd-sanjorge',
            progress_bar_type=None,
            credentials=self._cred
            )
        return dataframe

    
    def query(self, query: str) -> pd.DataFrame:
        dataframe = pdg.read_gbq(
            query, project_id='bd-sanjorge',
            progress_bar_type=None,
            credentials=self._cred
            )
        return dataframe
    

    def export_merge(self, df1: pd.DataFrame, tabla: str, exists: str='replace') -> None:
        '''Params:
        -------
        - df1: Exports the dataframe to a merge table in BigQuery.
        - tabla: Table name.
        - exists: As pandas-gbq.to_gbq method. Default: "replace".'''
        try:
            pdg.to_gbq(df1 , f'bd-sanjorge.MERGE.{tabla}',
                progress_bar=False,
                project_id='bd-sanjorge', if_exists=exists,
                credentials=self._cred)
        except Exception as err:
            log.error(f'No se pudo exportar dataframe. Error: {err}')


    def export(self, df1: pd.DataFrame, tabla: str, exists='replace') -> None:
        '''Params:
        -------
        df1: Dataframe to export to Google BigQuery. \n
        exists: As pandas-gbq.to_gbq method. Default: "replace".'''
        try:
            pdg.to_gbq(df1 , tabla,
                progress_bar=False,
                project_id='bd-sanjorge', if_exists=exists,
                credentials=self._cred)
        except Exception as err:
            log.error(f'No se pudo exportar dataframe. Error: {err}')

