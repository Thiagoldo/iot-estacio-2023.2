import pyodbc
from datetime import *
from pandas import *
from Models import GeoCoding, Forecast

server = 'iotestacio.database.windows.net'
database = 'iot'
username = 'iotestacio'
password = '{Estudante@1}'
driver= '{SQL Server}'

class Azure:

    # def __init__(self) -> None:

    def save(str_pesquisada:str, date_pesquisada:str, geo:GeoCoding, resultado:DataFrame | Series):
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+ server+';PORT=1433;DATABASE='+ database+';UID='+ username+';PWD='+  password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""INSERT INTO dbo.weather (
                    string_pesquisado,
                    date_pesquisada,
                    date_da_pesquisa,
                    nome_retorno,
                    estado_retorno,
                    pais_retorno,
                    data_retorno,
                    elevacao_retorno,
                    precipitacao_retorno,
                    humidade_retorno,
                    temp_media_retorno,
                    temp_maxima_retorno,
                    temp_minima_retorno,
                    nascer_sol_retorno,
                    por_sol_retorno    
                ) VALUES (
                    '{str(str_pesquisada)}',
                    '{str(date_pesquisada)}',
                    '{str(datetime.today().strftime("%d/%m/%Y"))}',
                    '{str(geo.name)}',
                    '{str(geo.state)}',
                    '{str(geo.country)}',
                    '{str(date_pesquisada)}',
                    '{str(geo.elevation)}',
                    '{str(resultado['precipitation_probability'].values[0])}',
                    '{str(resultado['relativehumidity'].values[0])}',
                    '{str(resultado['temperature'].values[0])}',
                    '{str(resultado['MaxTemperature'].values[0])}',
                    '{str(resultado['MinTemperature'].values[0])}',
                    '{str(resultado['Sunrise'].values[0])}',
                    '{str(resultado['Sunset'].values[0])}'
                );""")
