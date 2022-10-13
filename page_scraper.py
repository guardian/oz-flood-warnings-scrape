# %%

import pandas as pd
import requests
import time  
import json 
import datetime 
import pytz
import re 
import random 

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


for state in linkos:
  counter = 1
  print(f"""\n {state} \n""")
  statto = linkos[state]
  for url in statto:
    print(f"{counter}/{len(statto)}")
    counter += 1
    # print(url)

    stem = re.search('\?(.*)\.html', url)[0]
    stem = stem.replace('.html', '')
    stem = stem.replace('?', '')

    
    linko = url
    r = requests.get(linko, headers=headers)


    tabs = pd.read_html(r.text)[0]
    tabs['Scraped'] = now
    tabs['State'] = state

    with open(f'output/scrapes/{state}/{stem}-{now_format}.csv', 'w') as f:
      tabs.to_csv(f, index=False, header=True)

    rando = random.randint(0,10)
    time.sleep(rando)


# # %%

# %%
