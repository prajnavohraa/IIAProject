import pandas as pd
import os
import numpy as np

# EXTRACT
def extract_rainfall():
    original_rainfall_csv = "originaldatasets/original_rainfall.csv"
    original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)

original_cropproduction_csv = "originaldatasets\original_cropproduction.csv"
original_cropproduction_csv_data = pd.read_csv(original_cropproduction_csv)

original_drought_csv = "originaldatasets\original_drought.csv"
original_drought_csv_data = pd.read_csv(original_drought_csv)

original_districtmapping_csv = "originaldatasets\original_districtmapping.csv"
original_districtmapping_csv_data = pd.read_csv(original_districtmapping_csv)

# print(original_rainfall_csv_data.head())

# TRANSFORM

#rainfall
def transform_rainfall(original_rainfall_csv_data):
    transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
    transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
    transformed_rainfall_csv_data=transformed_rainfall_csv_data.dropna()
    transformed_rainfall_csv_data.to_csv("transformeddatasets/transformed_rainfall.csv", index=False)

# drought
transformed_drought_csv_data = original_drought_csv_data
# transformed_drought_csv_data['State'] = 'hello'
# condition = transformed_drought_csv_data['District'] == '1(a) Haryana, Chandigarh & Delhi'
# transformed_drought_csv_data.loc[condition, 'State'] = 'Haryana'
# transformed_drought_csv_data.to_csv("transformeddatasets/transformed_drought.csv", index=False)
# print(transformed_drought_csv_data.head())
print(transformed_drought_csv_data.iloc[1:3,0:1])
# plan :
# we have csv -> etl -> dump into sql -> create that view thing in sql ->  then increment(wala thing)
