import pandas as pd
# import pandas_profiling as pp
import matplotlib as plt
import numpy as np
import seaborn as sns
import datetime
from datetime import datetime as date
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils.plotting import plot_series
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.base import ForecastingHorizon
from sktime.performance_metrics.forecasting import sMAPE, smape_loss
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.arima import ARIMA, AutoARIMA

cached_models = {}


def get_cached_models():
    global cached_models
    return cached_models

def get_prepared_df():
    date_parser = lambda ts: datetime.strptime(ts, "%y-%m-%dT%H:%M:%SZ")
    df = pd.read_csv('aviasales_data_t.csv')
    df['requested_at'] = pd.to_datetime(df['requested_at'], format="%y-%m-%dT%H:%M:%SZ", errors="coerce")
    df['departure_at'] = pd.to_datetime(df['departure_at'], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    df['expires_at'] = pd.to_datetime(df['expires_at'], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    df['price'] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna()
    df = df.drop_duplicates(subset=['departure_at', 'expires_at', 'airline', 'flight_number', 'price'],
                            keep='first')
    return df


def fit_forecast_model(orgn, dest, n_days, df):
    orgn_dest = df[(df["origin"] == orgn) & (df["destination"] == dest)
                   & (df["requested_at"] >= df["departure_at"] - datetime.timedelta(days=n_days + 1))
                   & (df["requested_at"] <= df["departure_at"] - datetime.timedelta(days=n_days))]
    # print(orgn_dest)

    orgn_dest_day_min = orgn_dest.resample('D', on='requested_at')['price'].min()

    orgn_dest_day_min = orgn_dest_day_min.fillna(orgn_dest_day_min.mean())  # not very smart

    y = orgn_dest_day_min
    forecaster = AutoARIMA()
    forecaster.fit(y)
    return forecaster


def fit_cached_models():
    airports = ['MOW', 'LED', 'KZN'] #not all
    df = get_prepared_df()
    for orig in airports:
        for dest in airports:
            if orig != dest:
                print(orig, dest)
                get_cached_models()[orig + dest] =\
                    [fit_forecast_model(orig, dest, n_days, df) for n_days in range(7)]


class PricePredictor():

    def prepare_df(self):
        return get_prepared_df()

    def predict_queried_prices_for(self,orgn, dest, current_date, flight_date, n_days, df):
        orgn_dest = df[(df["origin"] == orgn) & (df["destination"] == dest) & (df["departure_at"] <= flight_date)
                       & (df["requested_at"] >= df["departure_at"] - datetime.timedelta(days=n_days + 1))
                       & (df["requested_at"] <= df["departure_at"] - datetime.timedelta(days=n_days))]
        # display(orgn_dest)

        orgn_dest_day_min = orgn_dest.resample('D', on='requested_at')['price'].min()

        orgn_dest_day_min = orgn_dest_day_min.fillna(orgn_dest_day_min.mean())  # not very smart

        # display(orgn_dest_day_min)

        y = orgn_dest_day_min
        y_train, y_test = temporal_train_test_split(y)  # make test smaller?
        fh = ForecastingHorizon(y_test.index, is_relative=False)
        forecaster = AutoARIMA()
        forecaster.fit(y_train)
        y_pred = forecaster.predict(fh)
        # plot_series(y_train, y_test, y_pred, labels=["y_train", "y_test", "y_pred"])
        return round(y_pred[-1])

    def predict_queried_prices(self,orgn, dest, current_date, flight_date):
        df = self.prepare_df()
        days = []
        predictions = []
        flight_date= date.strptime(flight_date, '%d.%m.%y')
        current_date= date.strptime(current_date,'%d.%m.%y')

        delta = flight_date - current_date
        for i in range(delta.days + 1):
            days.append((flight_date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            predictions.append(self.predict_queried_prices_for(orgn, dest, current_date, flight_date, i, df))
        return days, predictions

    def predict_actual_queried_prices_for(self, orgn, dest, current_date, flight_date, n_days, df):
        forecaster = get_cached_models()[orgn + dest][n_days]
        pred_date = flight_date - datetime.timedelta(days=n_days)
        fh = ForecastingHorizon(pd.DatetimeIndex([pred_date]), is_relative=False)
        y_pred = forecaster.predict(fh)
        return y_pred[0]


    def show_real_prices(self,orgn, dest, current_date, flight_date, delta_days=7):
        flight_date= date.strptime(flight_date, '%d.%m.%y')
        current_date= date.strptime(current_date,'%d.%m.%y')
        df = self.prepare_df()
        orgn_dest = df[(df["origin"] == orgn) & (df["destination"] == dest) & (
                    df["departure_at"] <= flight_date + datetime.timedelta(days=1))
                       & (df["departure_at"] >= flight_date)]
        # display(orgn_dest)

        days = []
        prices = []
        for i in range(delta_days + 1):
            orgn_dest_day = orgn_dest[
                (orgn_dest["requested_at"] >= orgn_dest["departure_at"] - datetime.timedelta(days=i + 1))
                & (orgn_dest["requested_at"] <= orgn_dest["departure_at"] - datetime.timedelta(days=i))]
            if orgn_dest_day.empty:
                orgn_dest_day = orgn_dest[
                    (orgn_dest["expires_at"] >= orgn_dest["departure_at"] - datetime.timedelta(days=i + 1))
                    & (orgn_dest["expires_at"] <= orgn_dest["departure_at"] - datetime.timedelta(days=i))]

            prices.append(orgn_dest_day["price"].min())
            days.append((flight_date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            # display(orgn_dest_day)
        return days, prices