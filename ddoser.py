import requests

url_default = 'https://www.aviasales.ru/search/'
iata_codes = ['MOW', 'LED', 'KZN', 'CEK', 'SVX', 'AER', 'KRR', 'KGD']    # Moscow, Saint Petersburg, Kazan, Chelyabinsk, Ekaterinburg, Sochi, Krasnodar, Kaliningrad
iata_codes_extra = ['SGC', 'OVB', 'VVO', 'YKS']      # Surgut, Novosibirsk, Vladivostok, Yakutsk
iata_codes_for_extra = ['MOW', 'LED', 'SVX']


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    "Content-Type":"text" # прикинулся браузером
}


for orig in iata_codes_extra:
    for dest in iata_codes_for_extra:
        for date in range(4, 30):
            url = url_default
            if date < 10:
                date = '0' + str(date)
            else:
                date = str(date)
            url += orig
            url += date
            url += dest
            url += '1' # это костыль от разработчиков авиасейлс
            print(url)
            request = requests.get(url, timeout=30, headers=headers)


#print(data.text)
#это выводит html, но скрипт не спевает сработать, и html относительно браузерной версии неполный