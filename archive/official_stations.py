# %%
from codecs import ignore_errors
import pandas as pd 
import requests 
import re 
import io
import numpy as np 


from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
    s = df_2[key2].tolist()
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# %%

# # # r = requests.get('http://www.bom.gov.au/climate/data/lists_by_element/stations.txt', headers=headers)

# # # print(r.text)
# # # print(r.status_code)

# # # tabs = pd.read_html('http://www.bom.gov.au/climate/data/lists_by_element/stations.txt')

# # # tabs = pd.read_html(r.text)

# # # df = tabs[0]

# names=['Site','Dist','Site name','Start','End','Lat','Lon','Source','STA', 'Height (m)','Bar_ht','WMO']

# # # df = pd.read_csv('input/official_stations.txt',names=['Site','Dist','Site name','Start','End','Lat','Lon','Source','STA', 'Height (m)','Bar_ht','WMO'],
# # #  skiprows=4, delim_whitespace=True)

# # df = pd.read_csv('input/official_stations.txt', skiprows=5, delimiter="\t")

# df = pd.read_table('input/official_stations.txt', sep="\s+", names=names)

# # df = pd.concat([df.columns.to_frame().T, df], ignore_index=True)

# # # df.columns = ['Site','Dist','Site name','Start','End','Lat','Lon','Source','STA', 'Height (m)','Bar_ht','WMO']

# # df = df[:19417]

# # df = df[['Site']]

# p = df 

# print(p)
# print(p.columns.to_list())

# %%

stringo = ''

file = open('input/official_stations.txt', 'r')
lines = file.readlines()

for line in lines:
  line = line.strip()
  line = line.replace(" - ", '')
  line = re.sub("\(.*\)", "", line)
  line = re.sub("(?<=[a-zA-Z])\s\d", "", line)
  line = re.sub("(?<=[a-zA-Z])(\s)(?=[a-zA-Z])", "_", line)
  line = re.sub("\s+", ",", line)
  line = re.sub("(?<=[a-zA-Z])(_)(?=[a-zA-Z])", " ", line)
  # print(line)
  # print(type(line))
  stringo += line
  stringo += '\n'
# print(stringo)
# print(lines)

# print(stringo)

df = pd.read_csv(io.StringIO(stringo), sep=",", header=None, error_bad_lines=False)
df.columns = ['Site','Dist','Site name','Start','End','Lat','Lon','Source','STA', 'Height (m)','Bar_ht','WMO']

# %%
zdf = df.copy()
zdf.dropna(subset=['Source'], inplace=True)

zdf['Site name'] = zdf['Site name'].str.title()

zdf.loc[zdf['End'] == "..", 'End'] = np.nan

zdf['End'] = pd.to_numeric(zdf['End'])

zdf = zdf.loc[zdf['End'].isna()]

zdf = zdf[['Site', 'Site name', 'Lat', 'Lon']]

with open('input/station_locations_text.csv', 'w') as f:
  zdf.to_csv(f, index=False, header=True)

p = zdf 

print(p)
print(p.columns.to_list())

# %%

