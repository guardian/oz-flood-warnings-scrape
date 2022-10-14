import pandas as pd
import utm 
# import convertbng
# from convertbng.util import convert_bng, convert_lonlat

df = pd.read_excel('input/HydrologicDataAvailability.xlsx',skiprows=2, sheet_name='Data Availability')
'Catchment', 'Site ID', 'Station Name', 'DG No', 'Data Type', 
'ITN Callup', 'Station Short Name', 'Easting', 'Northing', 'Melway Ref.', 
'Unnamed: 10', 'Unnamed: 11', 'Esmap Ref.', 'Unnamed: 13', 'Unnamed: 14', 
'Date Commissioned', 'Unnamed: 16', 'Digital Data Start Date ', 
'Unnamed: 18', 'Data Quality', 'Unnamed: 20', 'Flow Control Condition', 'Comments'


df = df[['Site ID', 'Station Name','Easting', 'Northing']]

df.dropna(subset=['Easting'], inplace=True)

df['Lat'] = ''
df['Long'] = ''


listo = []

for index, row in df.iterrows():
  east = row['Easting']
  north = row['Northing']

  res = utm.to_latlon(east,  north, 55, 'H')

  row['Lat'] = res[0]
  row['Long'] = res[1]

  listo.append(row)

fin = pd.concat(listo, axis=1).T

fin = fin[['Site ID', 'Station Name', 'Lat', 'Long']]

fin.rename(columns = {'Site ID': 'Site', 
'Station Name': "Station name", 
'Lat': 'Lat', 
'Long':'Lon'},inplace=True)

with open('input/melbourne_water_sites.csv', 'w') as f:
  fin.to_csv(f, index=False, header=True)

print(fin)
print(fin.columns.tolist())
# print(p.columns.tolist())


# res = convert_bng(350760,  5816830)

# eastings = [350760.00]

# northings = [5816830.00]

# res_list_en = convert_lonlat(eastings, northings)

# print(res_list_en)



# res = utm.to_latlon(350760,  5816830, 55, 'H')

# print(res)