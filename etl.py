# import pandas as pd;
# from sqlalchemy import create_engine
# import os

# #EXTRACT
# original_rainfall_csv="iia\originaldatasets\original_rainfall.csv"
# original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)
# # print(original_rainfall_csv_data.head())
# # print(original_rainfall_csv_data.dtypes)

# #TRANSFORM

# original_rainfall_csv_data.drop(columns=["JF","MAM","JJAS","OND"])
# original_rainfall_csv_data.rename(columns={"SUBDIVISION":"State"})
# original_rainfall_csv_data.to_csv("iia\\transformeddatasets\\transformed_rainfall.csv")

import pandas as pd
import os

# EXTRACT
original_rainfall_csv = "iia/originaldatasets/original_rainfall.csv"
original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)

# TRANSFORM
transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
transformed_rainfall_csv_data.to_csv("iia/transformeddatasets/transformed_rainfall.csv", index=False)
