# %%
import os 
import pandas as pd 
import json 

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
cat.loc[cat['Flood Class'].isna(), 'Flood Class'] = ''
cat = cat.loc[cat['Height'] != cat['Tendency']]

cat = cat[['Station Name', 'Time/Day', 'Height', 'Tendency','Flood Class','Scraped', 'State']]

cat['Station Name'] = cat['Station Name'].str.replace("*", '')
# cat['Station Name'] = cat['Station Name'].str.replace("**", '')
cat['Station Name'] = cat['Station Name'].str.replace("#", '')
cat['Station Name'] = cat['Station Name'].str.replace("  ", ' ')
cat['Station Name'] = cat['Station Name'].str.strip()

cat.sort_values(by=['Scraped'], ascending=False, inplace=True)

cat.drop_duplicates(subset=['Station Name'], inplace=True)

cat.reset_index(inplace=True, drop=True)

with open('output/dumped.csv', 'w') as f:
  cat.to_csv(f, index=False, header=True)

p = cat

print(p)
print(p.columns.tolist())

print(p['Flood Class'].unique().tolist())


# %%

### Groiup by state


cat['Count'] = 1


grp = cat.groupby(by=['State'])['Count'].sum().reset_index()


p = grp 

print(p)
print(p.columns.tolist())