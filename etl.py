
import pandas as pd
import os

# EXTRACT
original_rainfall_csv = "originaldatasets/original_rainfall.csv"
original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)

original_cropproduction_csv = "originaldatasets\original_cropproduction.csv"
original_cropproduction_csv_data = pd.read_csv(original_cropproduction_csv)

original_drought_csv = "originaldatasets\original_drought.csv"
original_drought_csv_data = pd.read_csv(original_drought_csv)

original_districtmapping_csv = "originaldatasets\original_districtmapping.csv"
original_districtmapping_csv_data = pd.read_csv(original_districtmapping_csv)

print(original_rainfall_csv_data.head())

# TRANSFORM
transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
transformed_rainfall_csv_data.to_csv("transformeddatasets/transformed_rainfall.csv", index=False)
