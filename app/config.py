import os
from dotenv import dotenv_values, load_dotenv

class Config:
    '''Levanta todas las variables de entorno establecidas en diferentes archivos .env.'''
    DEBUG: bool = True

    LOG_PATH: str
    JSONPATH: str
    
    DBMUSER: str
    DBMPASS: str

    SVADR: str
    PTNUM: int
    DSN: str
    DRIVER: str


    def __init__(self) -> None:
        load_dotenv()
        self.__dict__.update({
            **dotenv_values(os.environ['DB_SETTINGS']),
            **dotenv_values(os.environ['DB_CREDENTIALS']),
            'JSONPATH':  os.environ['JSONPATH'],
            'LOG_PATH':  os.environ['LOG_PATH'],
            'DEBUG':  eval(os.environ['DEBUG'])
        })

        if not self.DEBUG:
            self.__dict__.update({
            **dotenv_values(os.environ['DB_SETTINGS'].replace('debug/', '')),
            **dotenv_values(os.environ['DB_CREDENTIALS'].replace('debug/',''))
            })

    def __repr__(self) -> None:
        for k, v in self.__dict__.items():
            print(f'{k}: {v} -- {type(v)}') 

if __name__ == '__main__':
    conf = Config()
    conf.__repr__()