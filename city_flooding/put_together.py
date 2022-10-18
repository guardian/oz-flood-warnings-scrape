# %%
import os 
import pandas as pd 
import json 

path = 'city_flooding/input/'
out_path = 'city_flooding/output/processed/'


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
  # foldos = [x for x in foldos if x == 'shepparton']
  foldos = [pathos + x + '/' for x in foldos if (x != '.DS_Store') and (x != 'SWActiveSites.csv') and (x != 'rivers_to_use.csv')]

  for foldo in foldos:
    # print(foldo)

    city = foldo.split('/')[-2]

    fillos = os.listdir(foldo)

    fillos = [foldo + x for x in fillos if x != '.DS_Store']
    fillos = [x for x in fillos if 'MeanWaterLevel' in x]

    print(fillos)

    for fillo in fillos:
      stem = fillo.split('/')[-1].split(".")[0]

      if f"{stem}.csv" not in already_done:
        inter = pd.read_csv(fillo, skiprows=2)

        inter['Date'] = pd.to_datetime(inter['Date'])
        inter['Cutoff'] = inter['Date'].dt.strftime("%Y-%m-%d")

        # inter = inter.loc[(inter['Cutoff'] >= '2022-10-01')]

        inter['Site'] = stem
        inter['City'] = city 

        with open(f'{out_path}{stem}.csv', 'w') as f:
          inter.to_csv(f, index=False, header=True)

        already_done.append(f'{stem}.csv')

      else:
        continue


df = combine_from_folder(path)



# %%