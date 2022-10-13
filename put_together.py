# %%
import os 
import pandas as pd 
import json 

import datetime 
import pytz

# %%


utc_now = pytz.utc.localize(datetime.datetime.utcnow())
now = utc_now.astimezone(pytz.timezone("Australia/Sydney"))
now_format = now.strftime("%-d %B %Y %H:%M%p")

print(now_format)

# %%

outer = 'output/scrapes'
folders = os.listdir(outer)

# %%

listo = []

for folder in folders:
  path = outer + "/" + folder + "/"

  for fillo in os.listdir(path):
    inter = pd.read_csv(f"{path}{fillo}")

    listo.append(inter)

# %%


cat = pd.concat(listo)
# 'Station Name', 'Time/Day', 'Height', 'Tendency', 
# 'Flood Class', 'Recent Data', 'Scraped', 'State', 'Crossing'

### Drop the header rows
# cat.dropna(subset=['Flood Class'], inplace=True)
cat = cat.loc[cat['Height'] != cat['Tendency']]

cat.loc[cat['Flood Class'].isna(), 'Flood Class'] = ''
cat.loc[cat['Tendency'].isna(), 'Tendency'] = ''
cat.loc[cat['Height'].isna(), 'Height'] = ''

cat = cat[['Station Name', 'Time/Day', 'Height', 'Tendency','Flood Class','Scraped', 'State']]

cat['Station Name'] = cat['Station Name'].str.replace("*", '')
# cat['Station Name'] = cat['Station Name'].str.replace("**", '')
cat['Station Name'] = cat['Station Name'].str.replace("#", '')
cat['Station Name'] = cat['Station Name'].str.strip()
cat['Station Name'] = cat['Station Name'].str.replace("  ", ' ')

cat['Scraped'] = pd.to_datetime(cat['Scraped'])

cat.sort_values(by=['Scraped'], ascending=False, inplace=True)

print(len(cat))
cat.drop_duplicates(subset=['Station Name'], inplace=True)
print(len(cat))

# p = cat 

# print(p)
# # print(p.columns.tolist())

# print(p['Flood Class'].unique().tolist())


# %%

### Read in station id data

ids = pd.read_csv('input/stations_ids.csv')
# 'name', 'bom_stn_num'

ids.rename(columns={
  'name': "Station Name", 
}, inplace=True)


# ids.loc[ids['Station Name'] == 'Norman Ck Caswell St  E Brisbane #', 'Station Name'] = 'Norman Ck Caswell St E Brisbane'
# ids.loc[ids['Station Name'] == 'Delatite  R at Tonga Bridge', 'Station Name'] = 'Delatite R at Tonga Bridge'

ids['Station Name'] = ids['Station Name'].str.replace("  ", ' ')

ids['Station Name'] = ids['Station Name'].str.replace("*", '')
# cat['Station Name'] = cat['Station Name'].str.replace("**", '')
ids['Station Name'] = ids['Station Name'].str.replace("#", '')
ids['Station Name'] = ids['Station Name'].str.strip()

wids = pd.merge(cat, ids, on='Station Name', how='left')
wids.dropna(subset=['bom_stn_num'], inplace=True)
# p = wids 

# p = p.loc[~p['bom_stn_num'].isna()]

# print(p)
# print(p.columns.tolist())

not_matched = [x for x in cat['Station Name'].unique().tolist() if x not in wids['Station Name'].unique().tolist()]

print(not_matched)



# %%

## Read in the station data

stat = pd.read_csv('input/stations.csv')
# 'attributes.bom_stn_num', 'attributes.name', 'attributes.lat', 
# 'attributes.long', 'attributes.state', 'attributes.location_types', 'attributes.basin'

stat = stat[['attributes.bom_stn_num', 'attributes.lat', 'attributes.long', 'attributes.state', 'attributes.basin']]

dicto = {}
for col in stat.columns.tolist():
  dicto[col] = col.replace("attributes.", '')

stat.rename(columns=dicto, inplace=True)

# p = stat 

# print(p)
# print(p.columns.tolist())

# %%

wids['bom_stn_num'] = pd.to_numeric(wids['bom_stn_num'])
stat['bom_stn_num'] = pd.to_numeric(stat['bom_stn_num'])

tog = pd.merge(wids, stat, on='bom_stn_num', how='left')


#### Clean the names

tog['Station Name'] = tog['Station Name'].str.replace("*", '')
# cat['Station Name'] = cat['Station Name'].str.replace("**", '')
tog['Station Name'] = tog['Station Name'].str.replace("#", '')
tog['Station Name'] = tog['Station Name'].str.strip()
tog['Station Name'] = tog['Station Name'].str.replace("  ", ' ')

tog = tog[['bom_stn_num', 'Station Name', 'Time/Day', 'Height', 'Tendency', 'Flood Class','lat', 'long']]

tog['Last_scraped'] = now_format

tog.drop_duplicates(subset=['bom_stn_num'], inplace=True)
tog.dropna(subset=['lat', 'long','Station Name', 'Time/Day', 'Height', 'Tendency', 'Flood Class'], inplace=True)

p = tog 

print(p)
print(p.columns.tolist())
# %%


finalJson = json.dumps(tog.to_dict('records'), indent=4)

from modules.syncData import syncData

syncData(finalJson,"oz-rainfall-floods", "bom-flood-warnings-scrape.json")