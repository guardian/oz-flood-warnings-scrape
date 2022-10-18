# %%
import os 
import pandas as pd 
import json 
import numpy as np 

path = 'new_vic_river_map/output/processed/'

# %%

def remove_outliers(df,columns,n_std):
    for col in columns:
        print('Working on column: {}'.format(col))
        
        mean = df[col].mean()
        sd = df[col].std()
       
        df = df[(df[col] <= mean+(n_std*sd))]
        
    return df

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

# %%

data = combine_from_folder(path)

### Restrict to the stations that we want

rivers_to_use = pd.read_csv('new_vic_river_map/input/rivers_to_use.csv')

rivers_to_use['id'] = pd.to_numeric(rivers_to_use['id'])

rivers_to_use = rivers_to_use['id'].unique().tolist()

data['Site'] = pd.to_numeric(data['Site'])

zdf = data.loc[data['Site'].isin(rivers_to_use)]


# %%

df = zdf.copy()

df = df[['Date', 'Mean','Site']]

df['Mean'] = pd.to_numeric(df['Mean'])

p = df 

print(p)
print(p.columns.tolist())

dicto = {}

for site in df['Site'].unique().tolist():
  inter = df.loc[df['Site'] == site].copy()

  print(inter)

  inter.dropna(subset=['Mean'], inplace=True)

  # print(len(inter))
  inter = remove_outliers(inter, ['Mean'], 5)
  # print(len(inter))

  average = inter['Mean'].mean()
  maxxer = inter['Mean'].max()

  if average != np.nan: 

    dicto[site] = {"Average": average, "Max": maxxer}

  # p = inter 

  # print(p)
  # print(p.columns.tolist())


# %%

print(dicto)
# %%

from modules.syncData import syncData

finalJson = json.dumps(dicto, indent=4)

syncData(finalJson,"oz-rainfall-floods", "vic-flooding-long-term-averages.json")

with open('new_vic_river_map/output/long_run_averages.json', 'w') as fp:
    json.dump(dicto, fp)


print([x for x in rivers_to_use if x not in df['Site'].unique().tolist()])