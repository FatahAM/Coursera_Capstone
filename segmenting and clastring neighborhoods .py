#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system("conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

# for webscraping import Beautiful Soup 
from bs4 import BeautifulSoup

import xml

get_ipython().system("conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library

print('Libraries imported.')


# In[98]:


url = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(url,'lxml')


# ### The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
# 

# In[99]:


table_post = soup.find('table')
fields = table_post.find_all('td')

postcode = []
borough = []
neighbourhood = []

for i in range(0, len(fields), 3):
    postcode.append(fields[i].text.strip())
    borough.append(fields[i+1].text.strip())
    neighbourhood.append(fields[i+2].text.strip())
        
df = pd.DataFrame(data=[postcode, borough, neighbourhood]).transpose()
df.columns = ['Postcode', 'Borough', 'Neighborhood']
df.head()


# ###  process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.

# In[100]:


df['Borough'].replace('Not assigned', np.nan, inplace=True)
df.dropna(subset=['Borough'], inplace=True)
df.head()


# ### For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table

# In[101]:


dfgroup = df.groupby(['Postcode', 'Borough'])['Neighborhood'].apply(', '.join).reset_index()
dfgroup.columns = ['Postcode', 'Borough', 'Neighborhood']
dfgroup.head()


# ### If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.

# In[102]:


dfgroup['Neighborhood'].replace('Not assigned', "Queen's Park", inplace=True)
dfgroup.head()


# In[103]:


dfgroup.shape


# In[ ]:





#  
# ######   - Given that this package can be very unreliable,in case you are not able to get the geographical coordinates of the neighborhoods using the Geocoder package,here is a link to a csv file that has the geographical coordinates of each postal code: http://cocl.us/Geospatial_data
#  ####   Use the Geocoder package or the csv file to create the following dataframe:
# ####    I used csv file and merge the tables
# 

# In[104]:


df_geo = pd.read_csv('http://cocl.us/Geospatial_data')
df_geo.columns = ['Postcode', 'Latitude', 'Longitude']


# In[105]:


df_postcode = pd.merge(dfgroup, df_geo, on=['Postcode'], how='inner')
df_merge = df_postcode[['Borough', 'Neighborhood', 'Postcode', 'Latitude', 'Longitude']].copy()
df_merge.head()


#  ####   Coordinates of Toronto
#   ####  Map of Toronto
# 
# 

# In[106]:


address = 'Toronto, Canada'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of the City of Toronto are {}, {}.'.format(latitude, longitude))


# In[107]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(df_merge['Latitude'], df_merge['Longitude'], df_merge['Borough'], df_merge['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=3,
        popup=label,
        color='green',
        fill=True,
        fill_color='#3199cc',
        fill_opacity=0.3,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# #### Segmenting and Clustering
# ###### Foursquare API Credentials

# In[108]:


CLIENT_ID = 'C50U5PW0KUQFAYG3VW3C3OTKWLKYAMDVDPEKKC3COOAML32M' 
CLIENT_SECRET = 'FQW0AQA0PF52RSL5ZQ3YSHMI2O4QQWYDGVTC5HJ2WFCTO4VI'
VERSION = '20180605' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# ##### Toronto Neighbourhoods selection

# In[109]:


df_toronto = df_merge[df_merge['Borough'].str.contains('Toronto')]
data = df_toronto.reset_index(drop=True)
data


# 
# #### Toronto Neighborhoods map

# In[136]:


map_torontohood = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(data['Latitude'], data['Longitude'], data['Borough'], data['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=3,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3199cc',
        fill_opacity=0.3,
        parse_html=False).add_to(map_torontohood)  
    
map_torontohood


# ##### View the first neighbourhood

# In[111]:


data.loc[0, 'Neighborhood']


# ####  the coordinates of The Beaches

# In[134]:


neighborhood_latitude = data.loc[0, 'Latitude'] # neighbourhood latitude value
neighborhood_longitude = data.loc[0, 'Longitude'] # neighbourhood longitude value

neighborhood_name = data.loc[0, 'Neighborhood'] # neighbourhood name

print('Latitude and longitude values of {} are {}, {}.'.
      format(neighborhood_name, neighborhood_latitude, neighborhood_longitude))

