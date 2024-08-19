from datetime import datetime
import pytz
from metatrader import Metatrader
from setup import USER, PASSWORD

# Define the timezone (GMT-3)
timezone = pytz.timezone("America/Sao_Paulo")

STOCK = "VALE3"

DATE_START = datetime(2024, 1, 15)
DATE_END = datetime(2024, 1, 16, hour=17)
PREVISION_DATE_START = datetime(2024, 1, 17)
PREVISION_DATE_END = datetime(2024, 1, 17, hour=12)

DATE_START = timezone.localize(DATE_START)
DATE_END = timezone.localize(DATE_END)
PREVISION_DATE_START = timezone.localize(PREVISION_DATE_START)
PREVISION_DATE_END = timezone.localize(PREVISION_DATE_END)

TIMEFRAME = 1

"""
Horário ideal de negociação: de 10:10 até 16:50
copy_rates_from_range_date não usa horário para puxar os dados dentro do utc_from_date. 
Então para pegar o inicio do dia desejado, coloque o dia anterior no valor date_start 
até o horário desejado do dia seguinte.
"""

if __name__ == "__main__":
    mt = Metatrader(USER, PASSWORD)
    # esse dataframe pode ser especificado para qualquer data. Ele deve ser entregue ao modelo para treino.
    df_training = mt.copy_rates_from_range_date(
        stock_code=STOCK,
        utc_from_date=DATE_START,
        utc_to_date=DATE_END,
        timeframe=TIMEFRAME,
        write_csv_file=True,
        file_name_constructor="Training",
    )

    # as datas para esse dataframe devem bater com as datas da previsão, permitindo testar datas passadas e comparar a previsão com o resultado real
    df_prevision = mt.copy_rates_from_range_date(
        stock_code=STOCK,
        utc_from_date=PREVISION_DATE_START,
        utc_to_date=PREVISION_DATE_END,
        timeframe=TIMEFRAME,
        write_csv_file=True,
        file_name_constructor="Prevision",
    )

    # ADICIONAR AQUI O MODELO E CASO NECESSÁRIO O PLOT DE GRÁFICO

    print(df_prevision)
