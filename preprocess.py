##########
# Preprocessing & City/Neighborhood Encoding
# Felix Chen - flora-concise - Comment: Felix wrote the vast majority of the code
# except the first two lines (the importation).
# 
##########

import numpy as np
import pandas as pd

def clean_police_dataset(path):
    '''
    Parses .csv file of police dataset and outputs a cleaned pandas dataframe.
    '''
    with open(path, 'r', errors='replace') as pol_datafile:
        pol_df = pd.read_csv(pol_datafile)
    
    # Drop columns with >= 30% missing values
    null_sum = pol_df.isnull().sum()
    pol_df.drop(columns=pol_df.columns[null_sum > len(pol_df) * 0.3], inplace=True)
    pol_df.shape, pol_df.columns


    #######################
    ##### Categorical #####
    #######################

    # 'city' is made all lower-case here
    pol_df['city'] = pol_df['city'].str.lower()

    # 'tract' contains extraneous '.0' from erroneous conversion -> remove '.0'
    pol_df['tract'] = pol_df['tract'].astype('string').str.replace('.0', '')

    # 'cause_of_death' is really a list and should be parsed as such
    # Although here we keep it as a string so we can search later
    pol_df['cause_of_death'] = pol_df['cause_of_death'].astype('string')  #.str.split(', ')

    # pol_df.dropna(subset=['cause_of_death'])
    pol_df['cause_of_death']

    # other categorical columns
    cat_cols = ['gender', 'race', 'city', 'state', 'zip',
                'county', 'agency_responsible', 'tract']
    pol_df[cat_cols] = pol_df[cat_cols].astype('category')
    

    #####################
    ##### Numerical #####
    #####################

    float64_cols = ['latitude', 'longitude']
    float32_cols = ['age']
    pol_df[float64_cols] = pol_df[float64_cols].astype('float64')
    pol_df[float32_cols] = pol_df[float32_cols].astype('float32')

    # Converting latitude and longitude to an array of tuples
    # https://stackoverflow.com/questions/9758450/pandas-convert-dataframe-to-array-of-tuples/34551914#34551914

    pol_df['lat_long'] = list(pol_df[['latitude', 'longitude']].itertuples(index=False, name=None))

    # Alternative:
    # pol_df['lat_long'] = pol_df[['latitude', 'longitude']].values.tolist()

    # Drop columns without lat_long
    pol_df.dropna(subset=['lat_long'], inplace=True)


    #########################
    ##### Date and Time #####
    #########################

    # Convert to DateTime type
    series_date = pol_df['date'].astype('string').str.split('/')
    df_date = pd.DataFrame(series_date.tolist(), columns=['month','day', 'year'])
    pol_df['date'] = pd.to_datetime(df_date)
    pol_df = pd.DataFrame.join(pol_df, df_date)


    ##########################
    ##### String or Text #####
    ##########################

    str_cols = ['name', 'street_address']
    pol_df[str_cols] = pol_df[str_cols].astype('string')


    ########################
    ##### Final Return #####
    ########################

    return pol_df
