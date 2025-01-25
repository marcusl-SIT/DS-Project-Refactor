import pandas as pd

def create_df(address_list, postal_codes, cities):
    return pd.DataFrame({'address': address_list, 'postal_code': postal_codes, 'city': cities, 'store_count':0})

def filter_df(df):
    df['city'] = df['city'].apply(lambda x: 'Emmen' if x=='Emmenbrücke' else x)
    df['city'] = df['city'].apply(lambda x: 'Langnau im Emmental' if x=='Langnau i. E.' else x)
    df['city'] = df['city'].apply(lambda x: 'Brig' if x=='Glis' else x)
    df['city'] = df['city'].apply(lambda x: 'Zürich' if x=='Zürich - Flughafen' else x)

    return df

# def filter_df(col, cond):
#     return col.apply(lambda x: cond)



filtered_df = df_migros[df_migros['address'].str.contains('Glis')]
filtered_df


df_geonames = pd.read_csv(config['paths']['data_input'], sep=';')
df_geonames['Alternate Names'] = df_geonames['Alternate Names'].apply(lambda x: x.split(",") if pd.notna(x) else None)

for city in df_migros['city']:
    if city in df_geonames['Name'].values:
        index_df_geonames = df_geonames.loc[df_geonames['Name'] == city].index[0]
        population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
        coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
        df_migros.loc[df_migros['city'] == city, 'population'] = population
        df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
        df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
    elif city in df_geonames['ASCII Name'].values:
        index_df_geonames = df_geonames.loc[df_geonames['ASCII Name'] == city].index[0]
        population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
        coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
        df_migros.loc[df_migros['city'] == city, 'population'] = population
        df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
        df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
    else:
        for index, alternate_names in enumerate(df_geonames['Alternate Names'].values):
            if alternate_names!=None and city in alternate_names:
                index_df_geonames = index
                population = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Population')]
                coordinates = df_geonames.iloc[index_df_geonames, df_geonames.columns.get_loc('Coordinates')]
                df_migros.loc[df_migros['city'] == city, 'population'] = population
                df_migros.loc[df_migros['city'] == city, 'coordinates'] = coordinates
                df_migros.loc[df_migros['coordinates'] == coordinates, 'store_count'] += 1
df_migros

df_test1 = set(df_migros['city'])
len(df_test1)

df_migros_noadd = df_migros.drop(columns=['address', 'postal_code'])
df_final = df_migros_noadd.drop_duplicates()
df_final = df_final[df_final['store_count'] != 0]
df_final.rename(columns={'store_count': 'migros_count'}, inplace=True)
df_final

df_final.to_csv('df_migros.csv', index=False) # [PATH]