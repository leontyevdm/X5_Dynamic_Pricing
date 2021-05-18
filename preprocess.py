import sys
import requests

host, current_date = sys.argv[1], sys.argv[2]

airports = ['MOW', 'LED', 'KZN'] #not all

for orig in airports:
    for dest in airports:
        if orig != dest:
            data = {
                "origin": orig,
                "destination": dest,
                "flight_date": current_date,
                "date": current_date
            }
            requests.post(host + '/predict_prices', json=data)
