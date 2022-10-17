# %%
import os 
import pandas as pd 
import json 

path = 'new_vic_river_map/input/'
out_path = 'new_vic_river_map/output/processed/'


def old_combine_from_folder(pathos):
  
  listo = []
  
  fillos = os.listdir(pathos)
  fillos = [pathos + x for x in fillos if x != '.DS_Store']

  for fillo in fillos:
    inter = pd.read_csv(fillo)

    listo.append(inter)

  cat = pd.concat(listo)

  return cat

# %%

## Read in corro

corr = pd.read_csv('new_vic_river_map/input/SWActiveSites.csv', error_bad_lines=False)
# 'STATION', 'STNAME', 'SHORTNAME', 'GAUGE', 'DATUM', 'CATCHAREA', 'ZONE', 'EASTING', 
# 'NORTHING', 'GRDATUM', 'LATITUDE', 'LONGITUDE', 'LLDATUM', 
# 'POSACC', 'ELEV', 'ELEVACC', 'FIELD', 'LAB', 'ACTIVE', 'COMMENCED', 'CEASED', 'REGION'

corr = corr.loc[corr['CEASED'].isna()]
corr = corr.loc[~corr['LATITUDE'].isna()]
corr = corr[['STATION','STNAME', 'LATITUDE', 'LONGITUDE', 'ELEV','CATCHAREA']]
corr.rename(columns={'STATION':'Site', 
'STNAME':'Station name',
'LATITUDE': "Lat", 
'LONGITUDE':'Lon', 
'ELEV': "Elevation"}, inplace=True)

# %%

# already_done = os.listdir(out_path)
already_done = []

def combine_from_folder(pathos):



  listo = []
  
  foldos = os.listdir(pathos)
  foldos = [pathos + x + '/' for x in foldos if (x != '.DS_Store') and (x != 'SWActiveSites.csv')]

  for foldo in foldos:
    print(foldo)
    fillos = os.listdir(foldo)

    fillos = [foldo + x for x in fillos if x != '.DS_Store']
    fillos = [x for x in fillos if 'MeanWaterLevel' in x]

    # print(fillos)

    for fillo in fillos:
      stem = fillo.split('/')[-1].split(".")[0]

      if f"{stem}.csv" not in already_done:
        inter = pd.read_csv(fillo, skiprows=2)

        inter['Date'] = pd.to_datetime(inter['Date'])
        inter['Cutoff'] = inter['Date'].dt.strftime("%Y-%m-%d")

        # inter = inter.loc[(inter['Cutoff'] >= '2022-10-01')]

        inter['Site'] = stem

        with open(f'{out_path}{stem}.csv', 'w') as f:
          inter.to_csv(f, index=False, header=True)

        already_done.append(f'{stem}.csv')

      else:
        continue


df = combine_from_folder(path)



# %%


df = old_combine_from_folder(out_path)



# print(df)

df['Site'] = pd.to_numeric(df['Site'])
corr['Site'] = pd.to_numeric(corr['Site'])

tog = pd.merge(df, corr, on='Site', how='left')

# print(tog)

# %%

zog = tog.loc[(tog['Cutoff'] > '2022-10-10') & (tog['Cutoff'] < '2022-10-18')].copy()

zog = zog[['Date','Site', 'Station name', 'Mean', 'Lat', 'Lon']]

zog[['Mean', 'Lat', 'Lon']].fillna('', inplace=True)

zog['Station name'] = zog['Station name'].str.title()

print(zog)

# %%

zog.dropna(subset=['Station name'], inplace=True)

keep = ["Goulburn River","Murray River", ]

listo = []

for thing in keep:

  inter = zog.loc[(zog['Station name'].str.contains(thing))]
  listo.append(inter)

goul = pd.concat(listo)

p = goul 

print(p)
# print(p.columns.tolist())

print(p['Station name'].unique().tolist())
# %%


finalJson = json.dumps(goul.to_dict('records'), indent=4)

from modules.syncData import syncData

syncData(finalJson,"oz-rainfall-floods", "vic-flooding-flow-map.json")

with open('new_vic_river_map/output/final_dumped.csv', 'w') as f:
  goul.to_csv(f, index=False, header=True)