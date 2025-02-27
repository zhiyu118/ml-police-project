**contributors:**
River, Anita, Mengmeng, Felix

**desctiption:**
This machine learning project is a classification task predicting police homicides based on demographic variables in large cities.

**folders:**
 - california_shapefiles: shapefiles for california census tracts
 - new_york_shapefiles: shapefiles for new york census tracts
 - illinois_shapefiles: shapefiles for illinois census tracts
 - census_2013: contains a csv that is the result of 2013 income, 2013 education, and 2013 race demographics. there is one csv for each state, formatted as '[state abbreviation]_2013.csv'

**code files:**
 - preprocessing-notebook.ipynb, preprocess.py: contains the function clean_police_dataset, which takes the police_data.csv and cleans the dataset
 - acs_merge_police.ipynb: EDA notebook
 - acs_merge_police.py: contains the function tract_merger (used to geopandas sjoin shapefiles to the police_data.csv dataframe) and attr_merger (merges the result of tract_merger with ACS demographic data found in the census_2013 folder, and also filters for the counties that contain our cities of interest)
 - logistic_regression.ipynb: training, tuning, and testing logistic regression models on our dataset
 - build_model_dt.ipynb, build_model_dt_il.ipynb, build_model_dt_ny.ipynb: training, tuning, and testing decision tree classifier on our dataset

**data files:**
 - police_data.csv: csv file from mappingpoliceviolence.org containing information on police homicides in cities with over 100,000 in population from January 2013 to January 2025
 - final_merge_il.csv, final_merge_ca.csv, final_merge_ny.csv: the result of pd.DataFrame.to_csv() after using tract_merger and attr_merger

**presentation files:**
- Perspectives Modeling P2 Slide Deck.pdf: Our slide deck.
- Our presentation video: 
https://photos.app.goo.gl/eqWAu4TJE2ro7esBA

----------

**References:**
- Campaign Zero (2024). *Mapping Police Violence*. https://mappingpoliceviolence.org/
- Maksuta, K. D., Zhao, Y., & Yang, T.-C. (2024). Race, disadvantage, and violence: A spatial exploration of macrolevel covariates of police-involved homicides within and between US counties. *Social Science Research 119*: 102985. https://doi.org/10.1016/j.ssresearch.2024.102985
- Prabakaran, S., & Mitra, S. (2019). Design and development of machine learning algorithm for forecasting crime rate. *International Journal of Innovative Technology and Exploring Engineering 8*(11): 1217-22. https://doi.org/10.35940/ijitee.K1246.09811S19
- Verrey, J., Ariel, B., Harinam, V., & Dillon, L. (2023). Using machine learning to forecast domestic homicide via police data and super learning. *Scientific Reports 13*: 22932. https://doi.org/10.1038/s41598-023-50274-2
- Wilkes, R., & Karimi, A. (2023). Multi-group data versus dual-side theory: On race contrasts and police-caused homicides. *Social Science & Medicine 327*: 115946. https://doi.org/10.1016/j.socscimed.2023.115946
