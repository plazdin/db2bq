#pylint: disable = no-name-in-module, c0115, c0116
import pyodbc
import sys
import pandas as pd
from config import Config
from utils.logger import Logger


log = Logger(__name__).get_logger()

class DBMAKER:
    
    def __init__(self) -> None:
        log.info(f'Iniciando conexión con DBMaker')
        self._conf = Config()
        try:
            self.conection = pyodbc.connect(
                f'DSN={self._conf.DSN};SVADR={self._conf.SVADR};\
                PTNUM={self._conf.PTNUM};UID={self._conf.DBMUSER};\
                PWD={self._conf.DBMPASS}')
            self.conection.setencoding(encoding='utf-16le')
            self.conection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-16le')
            self.conection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-16le')
        except Exception as err:
            log.error(err)
            sys.exit(1)
    

    def query(self, query: str) -> pd.DataFrame:
        dataframe = pd.read_sql(query, con=self.conection)
        return dataframe
    

    def get_dbm_tabla(self, tabla: str) -> pd.DataFrame:
        try:
            query = f'SELECT * FROM "SYSADM"."{tabla}"'
            dataframe = pd.read_sql(query, con= self.conection)
            return dataframe
        except Exception:
            print(f"Quizás no existe tabla llamad {tabla}. Revise los datos y vuelva a intentar.")
            return None

if __name__ == '__main__':
    dbm = DBMAKER()
    print(dbm.query("select * from SYSADM.VENDE"))
    