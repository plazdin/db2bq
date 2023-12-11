import argparse
from typing import List

parser = argparse.ArgumentParser(description='Parser para tablas a sincronizar desde DBM a BQ.')
parser.add_argument('-t', '--tables', nargs='+', type=str)

def get_pargs() -> List | None:
    args = parser.parse_args()
    return args._get_kwargs()[0][1]

if __name__ == '__main__':
    parsed = get_pargs()
    if parsed != None:
        print(parsed)
    else:
        print('No existen args')
