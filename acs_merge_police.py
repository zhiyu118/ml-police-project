import pandas as pd
import geopandas as gpd
import numpy as np
from preprocess import clean_police_dataset
import shapely
from shapely.geometry import point

# Anita Sun
# .py version of my notebook file for importing functions

def tract_merger(pol_filepath, shapefile_path):
    ''' 
    takes in the police homicide filepath and the census tract shapefile path
    and merges them together for that particular state

    pol_filepath: (str) file path for the police homicide csv
    shapefile_path: (str) file path for the census tract polygons shapefile

    returns:
    geo_joined_df: (GeoPandas Dataframe) a geopandas dataframe
    '''
    gdf = gpd.read_file(shapefile_path)
    pol_df = clean_police_dataset(pol_filepath)
    pol_df['geometry'] = gpd.points_from_xy(pol_df['longitude'], pol_df['latitude'])
    pol_gdf = gpd.GeoDataFrame(pol_df, geometry='geometry', crs="EPSG:4326")
    geo_joined_df = gpd.sjoin(gdf.to_crs(crs='EPSG:26916'), pol_gdf.to_crs(crs='EPSG:26916'))
    geo_joined_df = geo_joined_df[['GEOIDFQ','name', 'age', 'gender', 'race',
       'date', 'street_address', 'city', 'state', 'zip', 'county',
       'agency_responsible', 'ori', 'cause_of_death', 'circumstances',
       'disposition_official', 'officer_charged', 'news_urls',
       'signs_of_mental_illness', 'allegedly_armed', 'wapo_armed',
       'wapo_threat_level', 'wapo_flee', 'geography', 'encounter_type',
       'initial_reason', 'call_for_service', 'tract',
       'hhincome_median_census_tract', 'latitude', 'longitude',
       'pop_total_census_tract', 'pop_white_census_tract',
       'pop_black_census_tract', 'pop_native_american_census_tract',
       'pop_asian_census_tract', 'pop_pacific_islander_census_tract',
       'pop_other_multiple_census_tract', 'pop_hispanic_census_tract',
       'lat_long', 'month', 'day', 'year']]
    # renaming GEOIDFQ to GEO_ID so we can merge with ACS later
    geo_joined_df.rename(columns={'GEOIDFQ':'GEO_ID'}, inplace=True)
    # correcting year column to dtype int64
    geo_joined_df['year'] = geo_joined_df['year'].astype(int)

    return geo_joined_df


def booleaner(obj, list_like):
    ''' 
    returns 1 if obj is found in list_like, else returns zero
    obj: (anything)
    list_like: (listlike)
    '''
    if obj in list_like:
        return 1
    else:
        return 0
    

def attr_merger(geo_joined_df, census_file_path, county):
    ''' 
    takes a geo_df, census_file_path, and year and merges them all together
    geo_joined_df: (GeoPandasDataFrame) a sjoin of a state's .shp shapefile and the original police homicide csv
        has column 'GEOIDFQ' renamed to 'GEO_ID' for merging;
    census_file_path: file path for census tract demographic information, should be csv, year = 2013
    county: (str) county in question
    
    returns:
        df: a pd DataFrame containing census demographic data and a column that contains boolean val for pol homicide
    '''
    df = pd.read_csv(census_file_path)
    # dropping row index zero because it contains column name information and not data
    df = df.drop(index=0, axis=0)

    # converting all possible columns to float for later regression/classification analysis
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except:
            continue
        
    df['in_county'] = df.NAME.str.extract(r'\s*([\w\s]+ County)', expand=False)
    
    if type(county)==str:
        df = df[df['in_county'] == county]
    if type(county)==list:
        df = df[df['in_county'].isin(county)]        
    df['target'] = df.apply(
		lambda x: booleaner(x['GEO_ID'], geo_joined_df['GEO_ID'].values),
        axis=1
	)

    # performing merge on the 'GEO_ID' column with the sjoined tract polygon/homicide df
    return df

