from dagster import materialize_to_memory
from datetime import date, datetime
from unittest.mock import patch, Mock
from loupi_dagster.assets import (
    get_data_vantage,
    time_series_last,
    time_series_complete,
)
import pandas as pd

@patch('requests.get')
def test_smoke(mock_get):
    
    mock_response_data = {
        'Time Series (5min)': {
            '2023-11-17 19:55:00': {
                '1. open': '365.8700',
                '2. high': '366.4600',
                '3. low': '365.7100',
                '4. close': '366.2700',
                '5. volume': '18316'
            },
            '2023-11-17 19:50:00': {
                '1. open': '365.9700',
                '2. high': '365.9700',
                '3. low': '365.4000',
                '4. close': '365.7900',
                '5. volume': '31031'
            }
        }
    }
    
    mock_get.return_value.json.return_value = mock_response_data
    
    df = get_data_vantage()

    expected_df = pd.DataFrame(
        {
            'datetime':['2023-11-17 19:55:00','2023-11-17 19:50:00'],
            '1. open': ['365.8700', '365.9700'],
            '2. high': ['366.4600', '365.9700'],
            '3. low': ['365.7100', '365.4000'],
            '4. close': ['366.2700', '365.7900'],
            '5. volume': ['18316', '31031'],
        }
    )

    pd.testing.assert_frame_equal(df, expected_df)
    
