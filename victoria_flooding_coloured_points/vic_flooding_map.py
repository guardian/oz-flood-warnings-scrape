
# %%
import pandas as pd 
import requests
import xmltodict
import json 
fillo = 'https://data.water.vic.gov.au/wgen/sites.rs.anon.xml?1665961747893?1665961749299'

import datetime 
import pytz

# %%

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
now = utc_now.astimezone(pytz.timezone("Australia/Sydney"))
now_format = now.strftime('%Y-%m-%d-%H-%M')

scraped_time = now.strftime('%H:%M%p %A')

# print(now_format)
# print(scraped_time)

# %%

r = requests.get(fillo)


# %%

dicto = xmltodict.parse(r.text)
# print(dicto['sitedata']['sites']['site'])

# %%



df = pd.DataFrame.from_dict(dicto['sitedata']['sites']['site'])
# '@station', '@grpkeys', '@grpvals', '@grpvalsdesc', '@latdec', 
# '@lngdec', '@shortname', '@stname', '@colour', '@var_100x00_100', 
# '@var_100x00_100_dt', '@var_100x00_141', '@var_100x00_141_dt', 
# '@var_10x00_10', '@var_10x00_10_dt'

zdf = df.copy()

with open(f'output/vic_map_scrape/{now_format}.csv', 'w') as f:
  df.to_csv(f, index=False, header=True)

df = df[['@station', '@latdec', 
'@lngdec', '@stname', '@colour', '@var_100x00_100']]

df.rename(columns={'@station':"Site", 
'@latdec': 'Lat', 
'@lngdec':"Lon", 
'@stname': "Site name",
'@var_100x00_100': 'Water Level (m)', 
'@colour':"Colour"}, inplace=True)

df['Water Level (m)'].fillna('', inplace=True)

# df["Site name"] = df["Site name"].str.replace(" @ ", ' at ')

df["Site name"] = df["Site name"].str.title()

df['Scraped'] = scraped_time


# p = df 

# print(p)
# print(p.columns.tolist())

# print(dicto)
# %%



finalJson = json.dumps(df.to_dict('records'), indent=4)

from modules.syncData import syncData

syncData(finalJson,"oz-rainfall-floods", "vic-flooding-map-colours.json")



# %%

# ddf = zdf.copy()
# # ddf = ddf[['@station', '@colour','@var_100x00_100']]

# # ddf = ddf.loc[ddf['@colour'] == 'purple']
# ddf = ddf.loc[ddf['@stname'].str.contains("JAMIESON RIVER @ GERRANG BRIDGE")]

# ddf.sort_values(by=['@var_100x00_100'], ascending=False, inplace=True)

# p = ddf 

# print(p)
# print(p.columns.tolist())
# # %%
