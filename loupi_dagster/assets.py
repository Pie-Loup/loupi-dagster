from dagster import asset, op
from loupi_dagster.duckpond import SQL
from datetime import datetime
import os
import pandas as pd
import requests

@op
def get_data_vantage():
    
    url = "https://www.alphavantage.co/query"
    querystring = {
        "apikey": os.environ.get("VANTAGE_APIKEY")
        , "interval":"5min"
        , "function":"TIME_SERIES_INTRADAY"
        , "symbol":"MSFT"
        , "datatype":"json"
        , "output_size":"compact"
    }

    response = requests.get(url, params=querystring)
    data = response.json()['Time Series (5min)']

    return pd.DataFrame.from_dict(data, orient='index').reset_index(names=['datetime'])

@asset
def time_series_last() -> SQL:
    df = get_data_vantage()
    return SQL("select * from $df", df=df)

@asset
def time_series_complete(time_series_last) -> SQL:
    dt_now = str(datetime.now())
    print(dt_now)
    return SQL(
            """
              select 
                *
                , $dt_now as synced_at
              from $time_series_last
              union all
              select 
                *
              from time_series_complete
            """,
            time_series_last=time_series_last,
            dt_now=dt_now,
        )
