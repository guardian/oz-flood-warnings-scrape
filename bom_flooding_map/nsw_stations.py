# %%
import os 
import pandas as pd 

path = 'input/nsw_stations_map/'

# %%

def combine_from_folder(pathos):
  
  listo = []
  
  fillos = os.listdir(pathos)
  fillos = [pathos + x for x in fillos if x != '.DS_Store']

  for fillo in fillos:
    inter = pd.read_csv(fillo)

    listo.append(inter)

  cat = pd.concat(listo)

  return cat


df = combine_from_folder(path)

# %%

zdf = df.copy()
# 'Site Id', 'Site Name', 'Latitude', 'Longitude', 'Easting', 
# 'Northing', 'Zone', 'Gauge Zero (Ahd)', 'Site Start Date', 
# 'Site Cease Date', 'Drainage Area (Sq.Km)', 'Unnamed: 11'

zdf.drop_duplicates(subset=['Site Id'], inplace=True)
zdf['Site Name'] = zdf['Site Name'].str.title()

zdf = zdf[['Site Id', 'Site Name', 'Latitude', 'Longitude']]

with open('input/nsw_stations.csv', 'w') as f:
  zdf.to_csv(f, index=False, header=True)



p = zdf

print(p)
print(p.columns.tolist())
# %%
