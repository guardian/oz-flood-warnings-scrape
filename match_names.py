# %%
import os 
import pandas as pd 
import json 

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# %%

def fuzzy_merge(df_1, df_2, key1, key2, threshold=95, limit=1):
    s = df_2[key2].tolist()
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1

# %%

### Read in list of scraped ids 
ids = pd.read_csv('input/stations_ids_scraped.csv')

ids.rename(columns = {'bom_stn_num':'Site',
'name':'Site name'}, inplace=True)

# p = ids 

# print(p)
# print(p.columns.tolist())

# %%
### Read in list of locations

lock = pd.read_csv('output/station_locations.csv')
# 'Site', 'Site name', 'Lat', 'Lon', 'Rank'

lock = lock[['Site', 'Site name', 'Lat', 'Lon']]

lock['Site name'] = lock['Site name'].str.replace(" @ ", " at ")

in_both = [x for x in ids['Site'].unique().tolist() if x in lock['Site'].unique().tolist()]

# %%

### Cut down to just stations that don't have a shared id 

locked = lock.loc[~lock['Site'].isin(in_both)]

print(len(ids))

idsed = ids.loc[~ids['Site'].isin(in_both)]

print(len(idsed))

# %%
### Find merges for all the ones that aren't already matched

merged = fuzzy_merge(idsed, locked, 'Site name', 'Site name')

merged = merged.loc[merged['matches'] != '']

p = merged

print(p)

print(p.columns.tolist())



# %%

with open('input/matched_station_ids.csv', 'w') as f:
    merged.to_csv(f, index=False, header=True)

print(len(merged))

print(len(merged.loc[merged['matches'] == '']))


# %%

merged = pd.read_csv('input/matched_station_ids.csv')

matched = pd.merge(merged, locked, right_on='Site name', left_on='matches')

p = matched

print(p)
print()

# matched_station_locations
# %%
