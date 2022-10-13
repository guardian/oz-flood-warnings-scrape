# %%

import pandas as pd
import requests
import time  
import json 
import datetime 
import pytz
import re 
import random 
from bs4 import BeautifulSoup as bs 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open('input/links.json') as json_file:
    linkos = json.load(json_file)
    # print(linkos)
    # print(linkos.keys())

# %%

# Scraping!

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
now = utc_now.astimezone(pytz.timezone("Australia/Sydney"))
now_format = now.strftime('%Y-%m-%d-%H-%M')

# staters = ['NSW']

listo = []

for state in linkos:
# for state in staters:
  counter = 1
  print(f"""\n {state} \n""")
  statto = linkos[state]
  for url in statto:
    print(f"{counter}/{len(statto)}")
    counter += 1

    linko = url
    r = requests.get(linko, headers=headers)

    soup = bs(r.text, 'html.parser')

    table = soup.find('table', class_='tabledata')

    rows = table.find_all('tr')



    for row in rows:
      try:

        cells = row.find_all('td')
        station_name = cells[0].get_text()  
        linker = cells[-1].a['href'].split(".")[1]
        print(station_name)
        print(linker)
        # print(cells)
        record = {"name": station_name.strip(), "bom_stn_num":linker}

        listo.append(record)

        old = pd.read_csv('input/stations_ids.csv')

        inter = pd.DataFrame.from_records(listo)

        tog = pd.concat([old, inter])
        tog.drop_duplicates(subset=['name'], inplace=True)

        with open('input/stations_ids.csv', 'w') as f:
          tog.to_csv(f, index=False, header=True)

      except Exception as e:
        print(e)
        continue
    
    rando = random.randint(0,5)
    time.sleep(rando)





    #   print(station_name)

    #   print(linker)

    # print(table)

    # ahs = soup.findAll('a', href=True, text='Table')

    # ahs = ['http://www.bom.gov.au' + x['href'] for x in ahs]



    # print(ahs)


# %%