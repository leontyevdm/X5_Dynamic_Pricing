import pandas as pd
from tqdm.notebook import tqdm

df = pd.read_csv('aviasales_data_t.csv')
flights = pd.read_csv('flights.csv')

df['flight'] = df['airline'] + df['flight_number']
flights = flights.set_index('flight')
flights = flights.drop_duplicates()

def check_airport(expected, actual):
  if expected == '':
    return True
  if actual == 'MOW' and expected in ['SVO', 'DME', 'VKO', 'ZIA']:
    return True
  return actual == expected  

df['direct'] = False

for i in tqdm(range(len(df))):
  try:
    flight = flights.loc[df['flight'][i]]
    df['direct'][i] = check_airport(flight['origin'], df['origin'][i]) and check_airport(flight['destination'], df['destination'][i])
  except:
    pass  

df['aircraft'] = ''

for i in tqdm(range(len(df))):
  try:
    flight = flights.loc[df['flight'][i]]
    df['aircraft'][i] = flight['aircraft']
  except:
    pass  

df = df.drop(['flight'], axis=1)

df.to_csv('direct_flights.csv')
