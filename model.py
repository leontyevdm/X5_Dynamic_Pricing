import pandas as pd
# import pandas_profiling as pp
import matplotlib as plt
import numpy as np
import seaborn as sns
import datetime

from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.utils.plotting import plot_series
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.base import ForecastingHorizon
from sktime.performance_metrics.forecasting import sMAPE, smape_loss
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.arima import ARIMA, AutoARIMA


class PricePredictor():

    def prepare_df(self):
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
        delta = flight_date - current_date
        for i in range(delta.days + 1):
            days.append((flight_date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            predictions.append(self.predict_queried_prices_for(orgn, dest, current_date, flight_date, i, df))
        return days, predictions
