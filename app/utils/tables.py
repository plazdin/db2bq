from consts import tablas, filters

def column_string_agregator(cols: list) -> str:
    return(','.join(cols))

base_query = """
SELECT {} FROM SYSADM.{} {}
"""

for tabla in filters:
    filter = '' if tabla not in filters.keys() else filters[tabla]
    print(base_query.format(
        column_string_agregator(tablas[tabla]),
        tabla, filter))