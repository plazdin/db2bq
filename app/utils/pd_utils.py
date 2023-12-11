from datetime import datetime

import pandas as pd

import numpy as np

from .consts import at_date_columns


def process_dates(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Separates all date columns into a dataframe, fills nulls as 0 and convert into int64.
    '''
    df_dates=df[at_date_columns].copy()

    float_columns = df_dates.select_dtypes(include=['float']).columns.tolist()
    df_dates[float_columns] = df_dates[float_columns].fillna(0)
    df_dates[float_columns] = df_dates[float_columns].astype('int64')

    df_dates = df_dates.astype(str)

    return df_dates


def parse_date2(col):
    '''
    Formats every row depending on the length of the row itself.\n
    Returns the same column formated.
    '''
    columna_str = str(col)
    format_patterns = [
        ('%y%m%d', 3),
        ('%y%m%d', 4),
        ('%d%m%y', 5),
        ('%y%m%d', 5),
        ('%y%m%d', 6),
        ('%d%m%y', 6),
        ('%d%m%Y', 7),
        ('%Y%m%d', 8),
        ('%d%m%Y', 8)
    ]
    
    if len(columna_str) < 6:
        columna_str = columna_str.zfill(6)

    for pattern_info in filter(
        lambda x: x[1] == len(columna_str),
        format_patterns):
        pattern = pattern_info[0]

        try:
            fecha = datetime.strptime(columna_str, pattern)
            today = datetime.today()
            
            if fecha > today:
                # Invalid future date, swap year and day
                year = fecha.year
                day = fecha.day
                last_two_digits = str(year)[-2:]
                new_year = str(day) + str(year)[:2]
                new_day = last_two_digits + columna_str[-2:]
                fecha = fecha.replace(year=int(new_year), day=int(new_day))
            
            fecha_formateada = fecha.strftime('%Y-%m-%d')
            return fecha_formateada
        
        except ValueError:
            pass
    return col 


def parsear_dates(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Return a dataframe with all date columns formated.
    '''
    for column in at_date_columns:
        if column != "AT_ANIOFAB":
            df[column] = df[column].apply(parse_date2)
    return df


def convert_columns_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Converts the date_columns from the dataframe into "datetime" dtype and convert invalid dates in nulls.
    '''
    today = datetime.today()
    for column in at_date_columns:
        if column != 'AT_ANIOFAB':
            df[column] = pd.to_datetime(df[column], errors='coerce')
            invalid = df[column] > today
            df.loc[invalid,column]= np.nan
            df[column] = df[column].dt.tz_localize('UTC')
    return df


def update_date_columns(df: pd.DataFrame,
    df_dates: pd.DataFrame) -> pd.DataFrame:
    '''
    Replace all datetime columns from initial dataframe with the formated columns.
    '''
    for date_column in at_date_columns:
        df[date_column] = df_dates[date_column]
    return df 


def process_at_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Process all date columns for SYSADM.AUTOS to format to a more legible datestring.
    '''
    # Llamada a process_dates
    df_dates = process_dates(df)

    # Llamada a parsear_dates
    df_dates = parsear_dates(df_dates)

    # Llamada a convert_columns_to_datetime
    df_dates = convert_columns_to_datetime(df_dates)
    
    # llamada a update_date_columns
    df = update_date_columns(df, df_dates)

    return df

# df = process_and_convert_dates(df, at_date_columns)
