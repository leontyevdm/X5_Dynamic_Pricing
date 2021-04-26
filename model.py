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
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import xgboost as xgb

class PricePredictor():
    def init_db(self):
        self.data=self.init_df()

    def get_int(self,s):
        try:
            return int(s)
        except:
            return None

    def init_df(self) -> pd.DataFrame:
        df = pd.read_csv('aviasales_data_t.csv')
        df['departure_time'] = pd.to_datetime(df['departure_at'], errors='coerce')
        df['requested_time'] = pd.to_datetime('20' + df['requested_at'], errors='coerce')
        df['before_flight'] = (df['departure_time'] - df['requested_time']).apply(
            lambda x: x.total_seconds() / 3600)
        df['requested_date'] = df['requested_time'].apply(lambda x: x.date())
        df['departure_date'] = df['departure_time'].apply(lambda x: x.date())
        df = pd.DataFrame(df[['price', 'before_flight', 'origin', 'destination', 'departure_date', 'requested_date']])
        df['price'] = df['price'].apply(lambda x: self.get_int(x))
        df = df.groupby(['departure_date', 'requested_date', 'origin', 'destination']).min()

        df = df.reset_index()

        return df


    def prepare_df(self,origin, destination) -> pd.DataFrame:
        df = self.data.loc[self.data['origin'] == origin]
        df = df.loc[df['destination'] == destination]
        df.drop(['origin', 'destination'], axis=1)

        return df

    def create_only_date_train_features(self,df):
        rows = [self.create_date_features(df.iloc[i]) for i in range(len(df))]
        curr_df = pd.DataFrame(rows)
        return curr_df

    def create_date_features(self,old_row):
        row = {}
        req_date = pd.to_datetime(old_row['requested_date'])
        row['req_dayofweek'] = req_date.dayofweek
        row['req_quarter'] = req_date.quarter
        row['req_month'] = req_date.month
        row['req_year'] = req_date.year
        row['req_dayofyear'] = req_date.dayofyear
        row['req_dayofmonth'] = req_date.day
        row['req_weekofyear'] = req_date.weekofyear

        dep_date = pd.to_datetime(old_row['departure_date'])
        row['dep_dayofweek'] = dep_date.dayofweek
        row['dep_quarter'] = dep_date.quarter
        row['dep_month'] = dep_date.month
        row['dep_year'] = dep_date.year
        row['dep_dayofyear'] = dep_date.dayofyear
        row['dep_dayofmonth'] = dep_date.day
        row['dep_weekofyear'] = dep_date.weekofyear

        row['before_flight'] = old_row['before_flight']
        return row

    def predict(self,origin, destination, current_date, flight_date):
        flight_date = date.strptime(flight_date, '%d.%m.%y')
        current_date = date.strptime(current_date, '%d.%m.%y')
        df = self.prepare_df(origin, destination)
        df = df[df['departure_date'] < flight_date.date()]
        y_train = df['price']
        X_train = self.create_only_date_train_features(df)
        model = xgb.XGBRegressor().fit(X_train, y_train)

        rows = []
        days = []
        delta = flight_date - current_date
        for i in range(delta.days + 1):
            req_date = (flight_date - timedelta(days=i)).date()
            fl_date = flight_date.date()
            before_flight = timedelta(days=i).total_seconds() / 3600
            days.append(str(req_date))
            rows.append({'departure_date': fl_date, 'requested_date': req_date, 'before_flight': before_flight})

        X_test = self.create_only_date_train_features(pd.DataFrame(rows))
        y_pred = model.predict(X_test)
        return days, list(y_pred)

    def show_real_prices(self,origin, destination, current_date, flight_date, delta_days=7):
        flight_date= date.strptime(flight_date, '%d.%m.%y')
        current_date= date.strptime(current_date,'%d.%m.%y')
        df = self.prepare_df(origin, destination)
        days = []
        prices = []
        for i in range(delta_days + 1):
            req_date = (flight_date - timedelta(days=i)).date()
            fl_date = flight_date.date()
            days.append(str(req_date))
            price = None
            try:
                cur_df = df.loc[df['departure_date'] == fl_date]
                price = cur_df.loc[cur_df['requested_date'] == req_date]['price'].iloc[0]
            except:
                pass
            prices.append(price)

        return days, list(prices)