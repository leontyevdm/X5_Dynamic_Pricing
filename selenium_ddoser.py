from selenium import webdriver
import os
import time

chromedriver = "/Users/Mvideo/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
url_default = 'https://www.aviasales.ru/search/'
iata_codes = ['MOW', 'LED', 'KZN', 'CEK', 'SVX', 'AER', 'KRR', 'KGD']    # Moscow, Saint Petersburg, Kazan, Chelyabinsk, Ekaterinburg, Sochi, Krasnodar, Kaliningrad
iata_codes_extra = ['SGC', 'OVB', 'VVO', 'YKS']      # Surgut, Novosibirsk, Vladivostok, Yakutsk
iata_codes_for_extra = ['MOW', 'LED', 'SVX']

while True:
    for date in range(8, 31):
                url = url_default
                if date < 10:
                    date = '0' + str(date)
                else:
                    date = str(date)
                url += 'SGC'
                url += date
                url += '05'
                url += 'MOW'
                url += '1' # это костыль от разработчиков авиасейлс
                print(url)
                driver.get(url)
                time.sleep(15)





'''
for orig in iata_codes_extra:
    for dest in iata_codes_for_extra:
        for date in range(7, 30):
            url = url_default
            if date < 10:
                date = '0' + str(date)
            else:
                date = str(date)
            url += orig
            url += date
            url += '05'
            url += dest
            url += '1' # это костыль от разработчиков авиасейлс
            print(url)
            driver.get(url)
            time.sleep(20)
'''