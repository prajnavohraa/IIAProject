import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from sqlalchemy import text

#menu:

ans="yes"
while ans==1:
    print("hi")
    ans=int(input("continue?: "))

#csv file paths
original_rainfall_csv = r"originaldatasets\original_rainfall.csv"
original_cropproduction_csv = r"originaldatasets\original_cropproduction.csv"
original_drought_csv = r"originaldatasets\original_drought.csv"
original_weather_csv = r"originaldatasets\original_weather.csv"

# original_rainfall_csv = ""
# original_cropproduction_csv = ""
# original_drought_csv = ""
# original_weather_csv = ""

source_mapping = {
    'originaldatasets/original_rainfall.csv': 'farmerrainfalltrend',
    'originaldatasets/original_cropproduction.csv': 'farmercropproductionstatistics',
    'originaldatasets/original_drought.csv': 'farmerdroughttrend',
    'originaldatasets/original_weather.csv': 'farmerweatherforecast',
}

database_mapping = {
    'farmerrainfalltrend': 'farmerdatabase',  # Use the actual database name you've set up in MySQL
    'farmerdroughttrend': 'farmerdatabase',    # Use the same actual database name for all tables in the same database
    'farmercropproductionstatistics': 'farmerdatabase',
    'farmerweatherforecast': 'farmerdatabase',
}


def extract_rainfall():
    original_rainfall_csv = r"originaldatasets/original_rainfall.csv"
    original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)
    return original_rainfall_csv_data

def extract_cropproduction():
    original_cropproduction_csv = r"originaldatasets\original_cropproduction.csv"
    original_cropproduction_csv_data = pd.read_csv(original_cropproduction_csv)
    return original_cropproduction_csv_data

# def extract_drought():
#     original_drought_csv = "originaldatasets\original_drought.csv"
#     original_drought_csv_data = pd.read_csv(original_drought_csv)
#     return original_drought_csv_data

def extract_drought():
    
    try:
        original_drought_csv = r"originaldatasets\original_drought.csv"
        original_drought_csv_data = pd.read_csv(original_drought_csv)
    except FileNotFoundError:
        print("The original file is not found. Using the alternative file.")
        original_drought_csv = "C:\\Users\\ASUS\\Desktop\\original data\\originaldatasets\\original_drought.csv"
        original_drought_csv_data = pd.read_csv(original_drought_csv)

    return original_drought_csv_data


def extract_weather():
    original_weather_csv=r"originaldatasets\original_weather.csv"
    original_weather_csv_data=pd.read_csv(original_weather_csv)
    return original_weather_csv_data


#transformation
def transform_rainfall(original_rainfall_csv_data):
    transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
    transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
    transformed_rainfall_csv_data=transformed_rainfall_csv_data.dropna()
    transformed_rainfall_csv_data.to_csv(r"transformeddatasets/transformed_rainfall.csv", index=False)
    return transformed_rainfall_csv_data

def transform_cropproduction(original_cropproduction_csv_data):
    transformed_cropproduction_csv_data = original_cropproduction_csv_data.rename(columns={"State_Name": "State", "District_Name": "District", "Crop_Year":"Year"})
    transformed_cropproduction_csv_data= transformed_cropproduction_csv_data.dropna()
    transformed_cropproduction_csv_data.to_csv(r"transformeddatasets/transformed_cropproduction.csv", index=False)
    return transformed_cropproduction_csv_data

def transform_drought(original_drought_csv_data):
    transformed_drought_csv_data=original_drought_csv_data.rename(columns={"ModerateDroughtProbability": "Moderate_prob", "SevereDroughtProbability":"Severe_prob"})
    transformed_drought_csv_data=transformed_drought_csv_data.dropna()
    transformed_drought_csv_data.to_csv(r"transformeddatasets/transformed_drought.csv", index=False)
    return transformed_drought_csv_data

def transform_weather(original_weather_csv_data):
    transformed_weather_csv_data=original_weather_csv_data.drop(columns=["sealevelpressure", "winddir", "cloudcover", "visibility", "severerisk"])
    transformed_weather_csv_data=transformed_weather_csv_data.rename(columns={"name":"District", "datetime":"Date"})    
    transformed_weather_csv_data=transformed_weather_csv_data.dropna()
    transformed_weather_csv_data.to_csv(r"transformeddatasets/transformed_weather.csv", index=False)
    return transformed_weather_csv_data

from sqlalchemy import create_engine
import urllib.parse
username = "root"
password = "tony022002@Kuku"
host = "localhost"
port = "3306"  # Default MySQL port is 3306
database = "farmerdatabase"

# Encode the password using urllib.parse.quote_plus
quoted_password = urllib.parse.quote_plus(password)

connection_string = f"mysql://{username}:{quoted_password}@{host}:{port}/{database}"
engine = create_engine(connection_string)



# loading
def global_loading(rainfall, drought, cropproduction, weather):
    
    rainfall.to_sql(name='farmerrainfalltrend', con=engine, if_exists='append', index=False)
    drought.to_sql(name='farmerdroughttrend', con=engine, if_exists='append', index=False)
    cropproduction.to_sql(name='farmercropproductionstatistics', con=engine, if_exists='append', index=False)
    weather.to_sql(name='farmerweatherforecast', con=engine, if_exists='append', index=False)

# def global_loading(rainfall, drought, cropproduction, weather):
#     for code_db_name, actual_db_name in database_mapping.items():
#         transformed_data = locals()[code_db_name]  # Get the transformed data from the code's variables
#         transformed_data.to_sql(name=actual_db_name, con=engine, if_exists='append', index=False)


def local_loading(data,tablename):
    data.to_sql(name=tablename, con=engine, if_exists='append', index=False)

x=extract_rainfall()
rainfall=transform_rainfall(x)

y=extract_cropproduction()
cropproduction=transform_cropproduction(y)

z=extract_drought()
drought=transform_drought(z)

a=extract_weather()
weather=transform_weather(a)

global_loading(rainfall,drought,cropproduction,weather)

initial_file_content1 = ''
initial_file_content2 = ''
# initial_file_content3 = ''
initial_file_content4 = ''

class MyHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        if event.src_path in source_mapping:
            print(f"Local source {event.src_path} was removed.")
            transformed_file = source_mapping[event.src_path]
            connection = engine.connect()
            sql_query = text(f"DROP TABLE IF EXISTS {transformed_file};")
            connection.execute(sql_query)
    
    def on_created(self, event):
        if event.src_path in source_mapping:
            print(f"Local source {event.src_path} was added.")
            transformed_file = source_mapping[event.src_path]

            if transformed_file == 'transformeddatasets/transformed_rainfall.csv':
                data = extract_rainfall()
                transformed_data = transform_rainfall(data)
            elif transformed_file == 'transformeddatasets/transformed_cropproduction.csv':
                data = extract_cropproduction()
                transformed_data = transform_cropproduction(data)
            elif transformed_file == 'transformeddatasets/transformed_drought.csv':
                data = extract_drought()
                transformed_data = transform_drought(data)
            elif transformed_file == 'transformeddatasets/transformed_weather.csv':
                data = extract_weather()
                transformed_data = transform_weather(data)

            local_loading(transformed_data, transformed_file)
            print(f"Data from {event.src_path} loaded into {transformed_file} in the database.")

    def on_modified(self, event):
        #rainfall
        if event.src_path == original_rainfall_csv:
            global initial_file_content1
            with open(original_rainfall_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content1:
                print("original_rainfall.csv was changed")
                data=extract_rainfall()
                transformed_data=transform_rainfall(data)
                connection = engine.connect()
                sql_query = text("drop table farmerrainfalltrend")
                # Execute the SQL command
                connection.execute(sql_query)
                local_loading(transformed_data, "farmerrainfalltrend")
                initial_file_content1 = new_content

        #drought
        if event.src_path == original_drought_csv:
            global initial_file_content2
            with open(original_drought_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content2:
                print("original_drought.csv was changed")
                data=extract_drought()
                transformed_data=transform_drought(data)
                connection = engine.connect()
                sql_query = text("drop table farmerdroughttrend")
                # Execute the SQL command
                connection.execute(sql_query)
                local_loading(transformed_data, "farmerdroughttrend")
                initial_file_content2 = new_content

        #cropproduction
        if event.src_path == original_cropproduction_csv:
            global initial_file_content3
            initial_file_content3=''
            with open(original_cropproduction_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content3:
                print("original_cropproduction.csv was changed")
                data=extract_cropproduction()
                transformed_data=transform_cropproduction(data)
                connection = engine.connect()
                sql_query = text("drop table farmercropproductionstatistics")
                # Execute the SQL command
                connection.execute(sql_query)
                local_loading(transformed_data,"farmercropproductionstatistics")
                initial_file_content3 = new_content

        #weather
        if event.src_path == original_weather_csv:
            global initial_file_content4
            with open(original_weather_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content4:
                print("original_weather.csv was changed")
                data=extract_weather()
                transformed_data=transform_weather(data)
                connection = engine.connect()
                sql_query = text("drop table farmerweatherforecast")
                # Execute the SQL command
                connection.execute(sql_query)
                local_loading(transformed_data, "farmerweatherforecast")
                initial_file_content4 = new_content



if __name__ == "__main__":
    
    #for rainfall
    with open(original_rainfall_csv, 'r') as file1:
        initial_file_content = file1.read()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(original_rainfall_csv), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    #for drought
    with open(original_drought_csv, 'r') as file2:
        initial_file_content = file2.read()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(original_drought_csv), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    #for cropproduction
    with open(original_cropproduction_csv, 'r') as file3:
        initial_file_content = file3.read()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(original_cropproduction_csv), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    #for weather data
    with open(original_weather_csv, 'r') as file4:
        initial_file_content = file4.read()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(original_weather_csv), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#gives average temperature of a district predicted in next few days
def get_average_temp_data(date, district):
    sql_query = text("SELECT AVG(temp) from farmerweatherforecast where District="+district+ ";")
    connection = engine.connect()
    connection.execute(sql_query)

#gives the rainfall of a state in a particular month and year(past)
def get_year_month_rainfall(state,year,month):
    sql_query = text("SELECT State, YEAR, "+month+ " from farmerrainfalltrend where State="+state+" and YEAR="+ year+";")
    connection = engine.connect()
    connection.execute(sql_query)


# Perform schema matching and select the most similar attribute
# schema_matches = perform_schema_matching(global_attributes, local_new_attributes)

# Print the matching results with the highest similarity score
# for attr_a, (best_match, max_similarity) in schema_matches.items():
#     print(f"Best matching for '{attr_a}': '{best_match}' with similarity score: {max_similarity}")

