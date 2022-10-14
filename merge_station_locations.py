# %%
import os 
import pandas as pd 

# %%


nsw = pd.read_csv('input/nsw_stations.csv')
# 'Site Id', 'Site Name', 'Latitude', 'Longitude'

nsw.rename(columns={'Site Id':'Site', 
'Site Name':'Site name', 
'Latitude':'Lat', 
'Longitude':'Lon'}, inplace=True)

nsw.dropna(subset=['Site name'], inplace=True)
nsw['Site name'] = nsw['Site name'].str.title()

nsw['Site'] = nsw['Site'].str.replace("B", '')
nsw['Site'] = nsw['Site'].str.replace("A", '')
nsw['Site'] = nsw['Site'].str.replace("D", '')
nsw['Site'] = nsw['Site'].str.replace("C", '')

nsw['Site'] = pd.to_numeric(nsw['Site'])

nsw['Rank'] = 2

# %%

vic = pd.read_csv('input/vic_stations.csv', error_bad_lines=False)
# 'STATION', 'STNAME', 'SHORTNAME', 'GAUGE', 'DATUM', 'CATCHAREA', 'ZONE', 
# 'EASTING', 'NORTHING', 'GRDATUM', 'LATITUDE', 'LONGITUDE', 'LLDATUM', 
# 'POSACC', 'ELEV', 'ELEVACC', 'FIELD', 'LAB', 'ACTIVE', 'COMMENCED', 
# 'CEASED', 'REGION'

vic = vic[['STATION', 'STNAME','LATITUDE', 'LONGITUDE']]

vic.rename(columns={'STATION':'Site', 
'STNAME':'Site name', 
'LATITUDE':'Lat', 
'LONGITUDE':'Lon'}, inplace=True)

vic.dropna(subset=['Site name'], inplace=True)

vic['Site name'] = vic['Site name'].str.title()

vic['Site'] = pd.to_numeric(vic['Site'])

vic['Rank'] = 2

# %%

old = pd.read_csv('input/station_locations_text.csv')
# 'Site', 'Site name', 'Lat', 'Lon'

old['Site'] = pd.to_numeric(old['Site'])

old['Rank'] = 4

# %%

off = pd.read_csv('input/stations_locations_api.csv')
# 'attributes.bom_stn_num', 'attributes.name', 'attributes.lat', 
# 'attributes.long', 'attributes.state', 'attributes.location_types', 'attributes.basin'

off = off[['attributes.bom_stn_num', 'attributes.name', 'attributes.lat', 'attributes.long']]
off.rename(columns={
  'attributes.bom_stn_num':'Site', 
  'attributes.name':'Site name', 
  'attributes.lat':'Lat',
  'attributes.long':'Lon'
}, inplace=True)

off['Site'] = pd.to_numeric(off['Site'])

off['Rank'] = 1

# %%

melbs = pd.read_csv('input/melbourne_water_sites.csv')
melbs['Rank'] = 2

melbs['Site'] = melbs['Site'].str.replace("B", '')
melbs['Site'] = melbs['Site'].str.replace("A", '')
melbs['Site'] = melbs['Site'].str.replace("D", '')
melbs['Site'] = melbs['Site'].str.replace("C", '')

melbs['Site'] = pd.to_numeric(melbs['Site'])



# %%


combo = pd.concat([nsw, vic, old, off])
combo.sort_values(by=['Rank'], ascending=True, inplace=True)

combo.drop_duplicates(subset=['Site'], keep='first', inplace=True)



# %%

merge_match = pd.read_csv('input/matched_station_ids.csv')

# merged_dict = merge_match[['matches', 'Site']]
# merged_dict.set_index('matches', inplace=True)

merged_dict = dict(zip(merge_match.matches, merge_match.Site))


lister = merge_match['matches'].unique().tolist()
print(lister)

listo = []

for index, row in combo.iterrows():
  nammo = row['Site name']
  if nammo in lister:
    new_number = merged_dict[nammo]
    row['Site'] = new_number

  listo.append(row)

combo = pd.concat(listo, axis=1).T


  # print(row)

# print(merged_dict)
# for 

# print(merge_match)



# %%




with open('output/station_locations.csv', 'w') as f:
  combo.to_csv(f, index=False, header=True)

p = combo 

print(p)
print(p.columns.tolist())
# %%
