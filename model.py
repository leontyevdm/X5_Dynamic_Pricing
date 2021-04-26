import pandas as pd
import numpy as np
from datetime import datetime, timedelta



class PricePredictor():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import xgboost as xgb

    def get_int(self,s):
        try:
            return int(s)
        except:
            return None

    def prepare_df(self,origin, destination) -> pd.DataFrame:
        df = pd.read_csv('aviasales_data_t.csv')
        df = df.loc[df['origin'] == origin]
        df = df.loc[df['destination'] == destination]
        df['departure_time'] = pd.to_datetime(df['departure_at'], errors='coerce')
        df['requested_time'] = pd.to_datetime('20' + df['requested_at'], errors='coerce')
        df['before_flight'] = (df['departure_time'] - df['requested_time']).apply(
            lambda x: x.total_seconds() / 3600)
        df['requested_date'] = df['requested_time'].apply(lambda x: x.date())
        df['departure_date'] = df['departure_time'].apply(lambda x: x.date())
        df = df.groupby(['departure_date', 'requested_date']).min()
        df = pd.DataFrame(df[['price', 'before_flight']])
        df['price'] = df['price'].apply(lambda x: self.get_int(x))
        df = df.reset_index()

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
        return days, y_pred

    def show_real_prices(self,origin, destination, current_date, flight_date, delta_days=7):
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

        return days, prices