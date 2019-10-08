
##  Assignment: Segmenting and Clustering Neighborhoods in Toronto


### explore and cluster the neighborhoods in Toronto.

### 1- Start by creating a new Notebook for this assignment.

### 2- Use the Notebook to build the code to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe



```python
# importing necessary libraries

import pandas as pd

import numpy as np

from bs4 import BeautifulSoup

import requests
```


```python
# getting data from internet

wikipedia_link='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
raw_wikipedia_page= requests.get(wikipedia_link).text

# using beautiful soup to parse the HTML/XML codes.

soup = BeautifulSoup(raw_wikipedia_page,'xml')

#print(soup.prettify())

```

### extracting raw table from Wikipedia page


```python
# extracting the raw table inside that webpage

table = soup.find('table')

Postcode      = []
Borough       = []
Neighbourhood = []

# print(table)

# extracting a clean form of the table

for tr_cell in table.find_all('tr'):
    
    counter = 1
    Postcode_var      = -1
    Borough_var       = -1
    Neighbourhood_var = -1
    
    for td_cell in tr_cell.find_all('td'):
       
    if counter == 1: 
            Postcode_var = td_cell.text
        
        if counter == 2: 
            Borough_var = td_cell.text
            tag_a_Borough = td_cell.find('a')
            
        if counter == 3: 
            Neighbourhood_var = str(td_cell.text).strip()
            tag_a_Neighbourhood = td_cell.find('a')
            
        counter +=1
        
    if (Postcode_var == 'Not assigned' or Borough_var == 'Not assigned' or Neighbourhood_var == 'Not assigned'): 
        continue
    try:
        if ((tag_a_Borough is None) or (tag_a_Neighbourhood is None)):
            continue
    except:
        pass
    if(Postcode_var == -1 or Borough_var == -1 or Neighbourhood_var == -1):
        continue
        
    Postcode.append(Postcode_var)
    Borough.append(Borough_var)
    Neighbourhood.append(Neighbourhood_var)

```

### integrating Postal codes with more than 1 neighbour


```python
unique_p = set(Postcode)
print('num of unique Postal codes:', len(unique_p))
Postcode_u      = []
Borough_u       = []
Neighbourhood_u = []


for postcode_unique_element in unique_p:
    p_var = ''; b_var = ''; n_var = ''; 
    for postcode_idx, postcode_element in enumerate(Postcode):
        if postcode_unique_element == postcode_element:
            p_var = postcode_element;
            b_var = Borough[postcode_idx]
            if n_var == '': 
                n_var = Neighbourhood[postcode_idx]
            else:
                n_var = n_var + ', ' + Neighbourhood[postcode_idx]
    Postcode_u.append(p_var)
    Borough_u.append(b_var)
    Neighbourhood_u.append(n_var)

```

    num of unique Postal codes: 77


###  creating Pandas Dataframe


```python
toronto_dict = {'Postcode':Postcode_u, 'Borough':Borough_u, 'Neighbourhood':Neighbourhood_u,}
df_toronto = pd.DataFrame.from_dict(toronto_dict)
df_toronto.to_csv('toronto_part1.csv')
df_toronto.head(14)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Postcode</th>
      <th>Borough</th>
      <th>Neighbourhood</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M2R</td>
      <td>North York</td>
      <td>Willowdale West</td>
    </tr>
    <tr>
      <th>1</th>
      <td>M1S</td>
      <td>Scarborough</td>
      <td>Agincourt</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M2K</td>
      <td>North York</td>
      <td>Bayview Village</td>
    </tr>
    <tr>
      <th>3</th>
      <td>M1N</td>
      <td>Scarborough</td>
      <td>Birch Cliff</td>
    </tr>
    <tr>
      <th>4</th>
      <td>M1P</td>
      <td>Scarborough</td>
      <td>Dorset Park, Scarborough Town Centre, Wexford ...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>M4B</td>
      <td>East York</td>
      <td>Woodbine Gardens, Parkview Hill</td>
    </tr>
    <tr>
      <th>6</th>
      <td>M4V</td>
      <td>Central Toronto</td>
      <td>Deer Park, Rathnelly, South Hill</td>
    </tr>
    <tr>
      <th>7</th>
      <td>M5A</td>
      <td>Downtown Toronto</td>
      <td>Harbourfront, Regent Park</td>
    </tr>
    <tr>
      <th>8</th>
      <td>M8Y</td>
      <td>Etobicoke</td>
      <td>Humber Bay, Mimico NE, Old Mill South, The Que...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>M1G</td>
      <td>Scarborough</td>
      <td>Woburn</td>
    </tr>
    <tr>
      <th>10</th>
      <td>M8W</td>
      <td>Etobicoke</td>
      <td>Alderwood, Long Branch</td>
    </tr>
    <tr>
      <th>11</th>
      <td>M1C</td>
      <td>Scarborough</td>
      <td>Highland Creek, Rouge Hill, Port Union</td>
    </tr>
    <tr>
      <th>12</th>
      <td>M5T</td>
      <td>Downtown Toronto</td>
      <td>Chinatown, Grange Park, Kensington Market</td>
    </tr>
    <tr>
      <th>13</th>
      <td>M1E</td>
      <td>Scarborough</td>
      <td>Morningside, West Hill</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_toronto.shape
```




    (77, 3)




```python

```
