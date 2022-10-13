# %%
import json 
import pandas as pd 
import requests


# %%

r = requests.get('https://hosting.wsapi.cloud.bom.gov.au/arcgis/rest/services/flood/National_Flood_Gauge_Network/MapServer/4/query?where=1%3D1&outFields=*&f=pjson')

# %%

data = r.content

with open('input/stations.json', 'wb') as f:
    f.write(data)

# %%

with open('input/stations.json') as json_file:
    data = json.load(json_file)

print(data.keys())

# df = pd.read_json('input/stations.json')
df = pd.json_normalize(data, record_path =['features'])

# 'attributes.bom_stn_num', 'attributes.name', 'attributes.lat', 'attributes.long',
# 'attributes.state', 'attributes.location_types', 'attributes.forecast_site_classification', 
# 'attributes.basin', 'attributes.objectid', 'geometry.x', 'geometry.y'


df = df[['attributes.bom_stn_num', 'attributes.name', 'attributes.lat', 'attributes.long', 
'attributes.state', 'attributes.location_types', 'attributes.basin']]

with open('input/stations.csv', 'w') as f:
  df.to_csv(f, index=False, header=True)

# p = df 

# print(p)
# print(p.columns.tolist())

# %%
