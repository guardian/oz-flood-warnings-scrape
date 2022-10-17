# %%
import time 
import random 
import json 

from os import link
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


dicto = {}

# %%

def linkscraper(state):
  linko = states[key][0]
  limit = states[key][1]

  r = requests.get(linko, headers=headers)

  soup = bs(r.text, 'html.parser')

  context = soup.find('div', id = 'content')

  linkos = context.find_all('a')

  linkos = [x['href'] for x in linkos]
  linkos = ["http://www.bom.gov.au" + x for x in linkos if 'cgi-bin' in x]

  linkos = linkos[:limit]

  print(linkos)
  return linkos


# %%
states = {"NSW": ['http://www.bom.gov.au/nsw/flood/rain_river.shtml',9],
'VIC': ['http://www.bom.gov.au/vic/flood/rain_river.shtml',8],
'QLD':['http://www.bom.gov.au/qld/flood/rain_river.shtml',12],
'SA':['http://www.bom.gov.au/sa/flood/rain_river.shtml',7],
'TAS':['http://www.bom.gov.au/tas/flood/rain_river.shtml',3],
'WA':['http://www.bom.gov.au/wa/flood/rain_river.shtml',8],
'NT':['http://www.bom.gov.au/nt/flood/rain_river.shtml', 1],
}


# %%

for key in states.keys():
  
  dicto[key] = linkscraper(key)

  with open('input/links.json', 'w') as fp:
      json.dump(dicto, fp)


  rando = random.randint(0,5)
  time.sleep(rando)

