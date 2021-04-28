from sklearn.metrics import r2_score, mean_squared_log_error, max_error

import pandas as pd
import numpy as np
import datetime
from time import perf_counter

from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils.plotting import plot_series
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.base import ForecastingHorizon
from sktime.performance_metrics.forecasting import sMAPE, smape_loss
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.arima import ARIMA, AutoARIMA

from tabulate import tabulate

import warnings
warnings.filterwarnings('ignore')

date_parser = lambda ts: datetime.strptime(ts, "%y-%m-%dT%H:%M:%SZ")
df = pd.read_csv('./pricing/aviasales_data_t.csv')
df['requested_at'] = pd.to_datetime(df['requested_at'], format="%y-%m-%dT%H:%M:%SZ", errors="coerce")
df['departure_at'] = pd.to_datetime(df['departure_at'], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
df['expires_at'] = pd.to_datetime(df['expires_at'], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
df['price'] = pd.to_numeric(df["price"], errors="coerce")
df = df.dropna()
df = df.drop_duplicates(subset=['departure_at', 'expires_at', 'airline', 'flight_number', 'price'], keep='first')


def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# Profile prediction func and test prediction quality
def ml_model_test(orgn : str, dest : str,
                  current_date : datetime.datetime, flight_date : datetime.datetime,
                  predictor_f, target_f):
    print(orgn, dest)

    tic = perf_counter()
    predictions = predictor_f(orgn, dest, current_date, flight_date)
    tac = perf_counter()
    elapsed_time = tac - tic
    
    targets = target_f(orgn, dest, current_date, flight_date)
    print(f"Elapsed time: {elapsed_time:0.4f} seconds")
    print(predictions[1], targets[1])
    
    r2 = r2_score(targets[1], predictions[1])
    msle = mean_squared_log_error(targets[1], predictions[1])
    max_err = max_error(targets[1], predictions[1])
    mape = mean_absolute_percentage_error(targets[1], predictions[1])
    
    print("R2:", r2)
    print("MSLE:", msle)
    print("Max error:", max_err)
    print("MAPE:", mape)
    
    return (str(predictor_f), orgn, dest, elapsed_time, r2, msle, max_err, mape)

# INSERT YOUR FUNCTION
def predict_queried_prices(orgn, dest, current_date, flight_date):
    days = []
    predictions = []
    delta = flight_date - current_date
    for i in range(delta.days + 1):
        days.append((flight_date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        predictions.append(predict_queried_prices_for(orgn, dest, current_date, flight_date, i))
    return days, predictions

def predict_queried_prices_for(orgn, dest, current_date, flight_date, n_days):
    
    orgn_dest = df[(df["origin"] == orgn) & (df["destination"] == dest) & (df["departure_at"] <= flight_date) 
                   & (df["requested_at"] >= df["departure_at"] - datetime.timedelta(days=n_days + 1))
                   & (df["requested_at"] <= df["departure_at"] - datetime.timedelta(days=n_days))] 
    
    orgn_dest_day_min = orgn_dest.resample('D', on='requested_at')['price'].min()
  
    orgn_dest_day_min = orgn_dest_day_min.fillna(orgn_dest_day_min.mean())  # not very smart
    
    y = orgn_dest_day_min
    y_train, y_test = temporal_train_test_split(y)
    
    forecaster = AutoARIMA()
    forecaster.fit(y_train)
    fh = ForecastingHorizon(y_test.index, is_relative=False)
    y_pred = forecaster.predict(fh)
    return round(y_pred[-1])

# INSERT YOUR FUNCTION
def show_real_prices(orgn, dest, current_date, flight_date, delta_days=7):
    
    orgn_dest = df[(df["origin"] == orgn) & (df["destination"] == dest) & (df["departure_at"] <= flight_date + datetime.timedelta(days=1))
                   & (df["departure_at"] >= flight_date)]
    
    days = []
    prices = []
    for i in range(delta_days + 1):
        orgn_dest_day = orgn_dest[(orgn_dest["requested_at"] >= orgn_dest["departure_at"] - datetime.timedelta(days=i + 1))
                           & (orgn_dest["requested_at"] <= orgn_dest["departure_at"] - datetime.timedelta(days=i))]
        if orgn_dest_day.empty:
            orgn_dest_day = orgn_dest[(orgn_dest["expires_at"] >= orgn_dest["departure_at"] - datetime.timedelta(days=i + 1))
                               & (orgn_dest["expires_at"] <= orgn_dest["departure_at"] - datetime.timedelta(days=i))]
        
        prices.append(round(orgn_dest_day["price"].min()))
        days.append((flight_date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        
    return days, prices



# JUST AN EXAMPLE

i = "MOW"
ml_test_results = []
for i in ['MOW', 'LED']: # NaNs in others , 'KZN', 'CEK', 'SVX', 'AER', 'KRR', 'KGD'
    for j in ['MOW', 'LED', 'KZN', 'CEK', 'SVX', 'AER', 'KRR', 'KGD']: # , 'SGC'
        if i != j:
            ml_test_results.append(ml_model_test(i, j, datetime.datetime(2021,4,20), datetime.datetime(2021,4,27),
                                             predict_queried_prices, show_real_prices))
ml_test_results.append(ml_model_test("MOW", "SGC", datetime.datetime(2021,4,20), datetime.datetime(2021,4,27),
                                             predict_queried_prices, show_real_prices))            
            
ml_test_df = pd.DataFrame(ml_test_results)
ml_test_df.columns = ['predictor_func', 'origin', 'destination', 'elapsed_time', 'r2_score', 'msle_score', 'max_error', 'mape']
print(tabulate(ml_test_df, headers = 'keys', tablefmt = 'psql'))

    