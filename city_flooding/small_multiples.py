# %%
import os
import this 
import pandas as pd 
import json 

path = 'city_flooding/output/processed/'

# path = 'output/processed/'


# %%

## Read in corro

corr = pd.read_csv('/Users/josh_nicholas/github/oz-flood-warnings-scrape/new_vic_river_map/input/SWActiveSites.csv', error_bad_lines=False)
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


# %%

def remove_outliers(df,columns,n_std):
    for col in columns:
        print('Working on column: {}'.format(col))
        
        mean = df[col].mean()
        sd = df[col].std()
       
        df = df[(df[col] <= mean+(n_std*sd))]
        
    return df

####

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

data = old_combine_from_folder(path)

flood_levels = {'Campaspe River at Rochester  Waranga Western Ch Syphn':{'Minor': 8, 'Moderate':8.8 , 'Major':9.1}, 
'Goulburn River at Shepparton':{'Minor': 9.5, 'Moderate': 10.7, 'Major': 11}, 
'Murray River at Echuca':{'Minor': 93.5, 'Moderate': 93.9, 'Major':94.4},  
'Loddon River at Murray Valley Highway Bridge (Kerang)':{'Minor': 77, 'Moderate': 77.5, 'Major':77.8}}

# %%

keep = [405204, 409200, 406202, 407242]

df = data.loc[data['Site'].isin(keep)].copy()

df['City'] = df['City'].str.title().str.strip()
df['Date'] = pd.to_datetime(df['Date'])

df.sort_values(by=['Date'], ascending=True, inplace=True)

df['Site'] = pd.to_numeric(df['Site'])
corr['Site'] = pd.to_numeric(corr['Site'])

df['Mean'] = pd.to_numeric(df['Mean'])

tog = pd.merge(df, corr, on='Site', how='left')
tog = tog[['Date', 'Mean', 'Cutoff', 'Site', 'City', 'Station name']]

tog['Station name'] = tog['Station name'].str.title()
# print(tog.columns.tolist())

listo = []

for city in tog['City'].unique().tolist():
  inter = tog.loc[tog['City'] == city].copy()

  inter['Month'] = inter['Date'].dt.month
  inter['Day'] = inter['Date'].dt.day

  inter = inter.loc[inter['Cutoff'] > '2010-01-01']
  inter = inter.loc[inter['Month'] == 10]

  this_year = inter.loc[inter['Date'].dt.year == 2022]
  this_year.rename(columns={'Mean': "This year"}, inplace=True)

  previous = inter.loc[inter['Date'].dt.year != 2022]

  grp = previous.groupby(by=['Month', 'Day','Site', 'City', 'Station name'])['Mean'].mean().reset_index()

  grp['Mean'] = round(grp['Mean'], 2)

  grp.rename(columns={'Mean':'Average past 10 years'}, inplace=True)

  # grp = grp[[]]

  combo = pd.merge(grp, this_year, on=['Month', 'Day','Site', 'City', 'Station name'], how='left')

  combo['Month'] = combo['Month'].astype(str)

  combo['Day'] = combo['Day'].astype(str)

  combo['Year'] = '2020'

  combo['New date'] = combo['Day'] + '/' + combo['Month'] + '/' + combo['Year']

  combo['New date'] = pd.to_datetime(combo['New date'], format="%d/%m/%Y")

  combo = combo[['New date', 'Station name', 'Average past 10 years','This year']]

  combo['This year'] = combo['This year'].interpolate(limit_area='inside')

  listo.append(combo)


# %%


cat = pd.concat(listo)

cat['New date'] = cat['New date'].dt.strftime("%Y-%m-%d")
cat.fillna('', inplace=True)

cat.set_index('New date', inplace=True)

cat['Station name'] = cat['Station name'].str.replace(" @ ", ' at ')

cat['Station name'] = cat['Station name'].str.replace("D/S", '')

cat['Minor'] = ''
cat['Moderate'] = ''
cat['Major'] = ''

for station in cat['Station name'].unique().tolist():
  for thing in ['Minor', 'Major']:
  # for thing in ['Minor', 'Moderate', 'Major flood']:
    cat.loc[(cat['Station name'] == station), thing] = flood_levels[station][thing]

cat = cat[['Station name','This year', 'Minor', 'Major']]

cat.rename(columns={'This year': "Daily average", 'Minor': "Minor flood", 'Major': "Major flood"}, inplace=True)

p = cat 

print(p)
print(p.columns.tolist())

print(p['Station name'].unique().tolist())

# %%


from modules.yachtCharter import yachtCharter


def makeStateVaccinations(df):

	template = [
			{
				"title": "Average daily river heights compared to flood thresholds",
				"subtitle": "",
				"footnote": "",
				"source": " | Source: Victoria Department of Environment, Land, Water & Planning",
				"dateFormat": "%Y-%m-%d",
				"xAxisLabel": "",
				"yAxisLabel": "",
				"timeInterval":"day",
				# "tooltip":"<strong>Date: </strong>{{#nicedate}}Date{{/nicedate}}<br/><strong>Rolling average per 100: </strong>{{State or territory}}",
				"periodDateFormat":"",
				"margin-left": "27",
				"margin-top": "25",
				"margin-bottom": "22",
				"margin-right": "22",
				"xAxisDateFormat": "%b %d"
			}
		]
	key = []
	periods = [{"label":"Data change", "start":"2021-08-16","end":"","textAnchor":"start"}]
	labels = []
	options = [{"numCols":2, "chartType":"line", "height":300, "scaleBy":"max"}]
	chartId = [{"type":"smallmultiples"}]
	df.fillna('', inplace=True)
	df = df.reset_index()
	chartData = df.to_dict('records')

	yachtCharter(template=template,options=options, data=chartData, periods=periods, chartId=chartId, chartName=f"vic-flooding-rivers-cities-small-multiples")

makeStateVaccinations(cat)