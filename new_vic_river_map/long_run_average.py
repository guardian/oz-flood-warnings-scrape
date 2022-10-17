# %%
import os 
import pandas as pd 
import json 

path = 'output/processed/'

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


# %%
df = data.copy()
# 'Date', 'Mean', 'Qual', 'Cutoff', 'Site'

df = df[['Date',  'Site', 'Mean']]

for site in df['Site'].unique().tolist():
  inter = df.loc[df['Site'] == site].copy()

  print(len(inter))
  inter = remove_outliers(inter, ['Mean'], 5)
  print(len(inter))

  p = inter 

  print(p)
  print(p.columns.tolist())


# %%