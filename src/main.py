import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
import time

import yaml

#from create_dataframe import create_df
#from create_dataframe import *
import create_dataframe as cr

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
    
config = read_yaml('./config.yml')

driver = webdriver.Chrome()
#driver.get("https://filialen.migros.ch/it/center:46.8182,8.2275/zoom:8/") # [_PATH]
driver.get(config['paths']['URL'])
driver.fullscreen_window()
filter_button_xpath = '//*[@id="storefinder"]/main/nav/header/button[2]/span[2]'

wait = WebDriverWait(driver, 10)
filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, filter_button_xpath)))
filter_button.click()

cookies_button_xpath = '//*[@id="onetrust-reject-all-handler"]'
cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, cookies_button_xpath)))
cookies_button.click()

time.sleep(2)


supermarket_button_xpath = '//*[@id="markets"]'
supermarket_button = wait.until(EC.element_to_be_clickable((By.XPATH, supermarket_button_xpath)))
supermarket_button.click()

select_supermarket_xpath = '//*[@id="storefinder"]/main/nav/div[2]/div/fieldset/label[1]/label/input'
select_supermarket = wait.until(EC.element_to_be_clickable((By.XPATH, select_supermarket_xpath)))
select_supermarket.click()

show_supermarkets_xpath = '//*[@id="storefinder"]/main/nav/footer/button/span'
show_supermarkets = wait.until(EC.element_to_be_clickable((By.XPATH, show_supermarkets_xpath)))
show_supermarkets.click()

time.sleep(2)

store_num_xpath = '//*[@id="storefinder"]/main/nav/header/button[1]/span[1]'
store_num = driver.find_element(By.XPATH, store_num_xpath).text.split(" ")[0]
print(store_num)

ul_element_xpath = '//*[@id="msrc-storefinder-storelist"]/div/ul'
ul_element = wait.until(EC.presence_of_element_located((By.XPATH, ul_element_xpath)))
div_element_xpath = '//*[@id="msrc-storefinder-storelist"]/div'
div_element = wait.until(EC.presence_of_element_located((By.XPATH, div_element_xpath)))

address_list = set()

while len(address_list) < int(store_num):
    try:
        div_element = driver.find_element(By.XPATH, div_element_xpath)
        li_elements = div_element.find_elements(By.TAG_NAME, 'li')
        for index, li in enumerate(li_elements, start=1):
            p_text = li.find_element(By.XPATH, './a/div/p').text
            address_list.add(p_text)
        driver.execute_script("arguments[0].scrollTop += 400;", div_element)
    except StaleElementReferenceException:
        div_element = driver.find_element(By.XPATH, div_element_xpath)

print(len(address_list))
driver.quit()

# %%
address_list = list(address_list)
len(address_list)

# %%
postal_codes = []
cities = []

for address in address_list:
    address = address.replace(",","").split(" ")[::-1]
    for item in address:
        if all((char.isdigit() and len(item)>2) for char in item):
            postal_codes.append(item)
            ref_index = address.index(item)
            ref_add = address[:ref_index]
            ref_add_reversed = ref_add[::-1]
            cities.append(" ".join(ref_add_reversed))
            break
        else: 
            continue

# df_migros = pd.DataFrame({'address': address_list, 'postal_code': postal_codes, 'city': cities, 'store_count':0})
df_migros = cr.create_df(address_list, postal_codes, cities)
df_migros = cr.filter_df(df_migros)
# # %%
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Emmen' if x=='Emmenbrücke' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Langnau im Emmental' if x=='Langnau i. E.' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Brig' if x=='Glis' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Zürich' if x=='Zürich - Flughafen' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Sempach' if 'Sempach' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Genève' if 'Genève' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Saint-Maurice' if 'St-Maurice' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Saint Gallen' if 'St.Gallen' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Sainte-Croix' if x=='Ste-Croix' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Saint-Imier' if x=='St-Imier' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Romanel-sur-Lausanne' if x=='Romanel-s-Lausanne' else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Lancy' if 'Lancy' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Ostermundigen' if x=='Ostermundigen 1' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Renens' if x=='Chavannes-Renens' in x else x)
# df_migros['city'] = df_migros['city'].apply(lambda x: 'Bussigny' if x=='Bussigny-Lausanne' in x else x)

# def filter_df(col, cond):
#     return col.apply(lambda x: cond)


# # %%
# filtered_df = df_migros[df_migros['address'].str.contains('Glis')]
# filtered_df

# # %%
# #file_path = 'geonames-all-cities-with-a-population-1000-2.csv' # [_PATH]
# df_geonames = pd.read_csv(config['paths']['data_input'], sep=';')
# df_geonames['Alternate Names'] = df_geonames['Alternate Names'].apply(lambda x: x.split(",") if pd.notna(x) else None)

# for city in df_migros['city']:
#     if city in df_geonames['Name'].values:
#         index_df_geonames = df_geonames.loc[df_geonames['Name'] == city].index[0]
#         population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
#         coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
#         df_migros.loc[df_migros['city'] == city, 'population'] = population
#         df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
#         df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
#     elif city in df_geonames['ASCII Name'].values:
#         index_df_geonames = df_geonames.loc[df_geonames['ASCII Name'] == city].index[0]
#         population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
#         coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
#         df_migros.loc[df_migros['city'] == city, 'population'] = population
#         df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
#         df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
#     else:
#         for index, alternate_names in enumerate(df_geonames['Alternate Names'].values):
#             if alternate_names!=None and city in alternate_names:
#                 index_df_geonames = index
#                 population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
#                 coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
#                 df_migros.loc[df_migros['city'] == city, 'population'] = population
#                 df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
#                 df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
# df_migros

# # %%
# df_test1 = set(df_migros['city'])
# len(df_test1)

# # %%
# df_migros_noadd = df_migros.drop(columns=['address', 'postal_code'])
# df_final = df_migros_noadd.drop_duplicates()
# df_final = df_final[df_final['store_count'] != 0]
# df_final.rename(columns={'store_count': 'migros_count'}, inplace=True)
# df_final

# # %%
# df_final.to_csv('df_migros.csv', index=False) # [PATH]

# %%
df_test2 = set(df_final['city'])
len(df_test2)

# %%
missing_cities = df_test1 - df_test2

# %%
len(missing_cities)

# %%



