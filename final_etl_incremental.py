import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

#csv file paths
original_rainfall_csv = "originaldatasets\original_rainfall.csv"
original_cropproduction_csv = "originaldatasets\original_cropproduction.csv"
original_drought_csv = "originaldatasets\original_drought.csv"
original_weather_csv = "originaldatasets\original_weather.csv"

def extract_rainfall():
    original_rainfall_csv = "originaldatasets/original_rainfall.csv"
    original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)
    return original_rainfall_csv_data

def extract_cropproduction():
    original_cropproduction_csv = "originaldatasets\original_cropproduction.csv"
    original_cropproduction_csv_data = pd.read_csv(original_cropproduction_csv)
    return original_cropproduction_csv_data

def extract_drought():
    original_drought_csv = "originaldatasets\original_drought.csv"
    original_drought_csv_data = pd.read_csv(original_drought_csv)
    return original_drought_csv_data

def extract_weather():
    original_weather_csv="originaldatasets\original_weather.csv"
    original_weather_csv_data=pd.read_csv(original_weather_csv)
    return original_weather_csv_data


#transformation
def transform_rainfall(original_rainfall_csv_data):
    transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
    transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
    transformed_rainfall_csv_data=transformed_rainfall_csv_data.dropna()
    transformed_rainfall_csv_data.to_csv("transformeddatasets/transformed_rainfall.csv", index=False)
    return transformed_rainfall_csv_data

def transform_cropproduction(original_cropproduction_csv_data):
    transformed_cropproduction_csv_data = original_cropproduction_csv_data.rename(columns={"State_Name": "State", "District_Name": "District", "Crop_Year":"Year"})
    transformed_cropproduction_csv_data= transformed_cropproduction_csv_data.dropna()
    transformed_cropproduction_csv_data.to_csv("transformeddatasets/transformed_cropproduction.csv", index=False)
    return transformed_cropproduction_csv_data

def transform_drought(original_drought_csv_data):
    transformed_drought_csv_data=original_drought_csv_data.rename(columns={"ModerateDroughtProbability": "Moderate_prob", "SevereDroughtProbability":"Severe_prob"})
    transformed_drought_csv_data=transformed_drought_csv_data.dropna()
    transformed_drought_csv_data.to_csv("transformeddatasets/transformed_drought.csv", index=False)
    return transformed_drought_csv_data

def transform_weather(original_weather_csv_data):
    transformed_weather_csv_data=original_weather_csv_data.drop(columns=["sealevelpressure", "winddir", "cloudcover", "visibility", "severerisk"])
    transformed_weather_csv_data=transformed_weather_csv_data.rename(columns={"name":"District", "datetime":"Date"})    
    transformed_weather_csv_data=transformed_weather_csv_data.dropna()
    transformed_weather_csv_data.to_csv("transformeddatasets/transformed_weather.csv", index=False)
    return transformed_weather_csv_data

#loading
def loading(rainfall, drought, cropproduction, weather):
    from sqlalchemy import create_engine

    username = "root"
    password = "12345"
    host = "localhost"
    port = "3306"  # Default MySQL port is 3306
    database = "farmerdatabase"
    connection_string = f"mysql://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    rainfall.to_sql(name='farmerrainfalltrend', con=engine, if_exists='append', index=False)
    drought.to_sql(name='farmerdroughttrend', con=engine, if_exists='append', index=False)
    cropproduction.to_sql(name='farmercropproductionstatistics', con=engine, if_exists='append', index=False)
    weather.to_sql(name='farmerweatherforecast', con=engine, if_exists='append', index=False)



x=extract_rainfall()
rainfall=transform_rainfall(x)

y=extract_cropproduction()
cropproduction=transform_cropproduction(y)

z=extract_drought()
drought=transform_drought(z)

a=extract_weather()
weather=transform_weather(a)

loading(rainfall,drought,cropproduction,weather)

# Define the path to the CSV file you want to monitor
# csv_file_path = 'originaldatasets\original_rainfall.csv'


initial_file_content1 = ''
initial_file_content2 = ''
initial_file_content3 = ''
initial_file_content4 = ''

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == original_rainfall_csv:
            global initial_file_content1
            with open(original_rainfall_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content1:
                print("original_rainfall.csv was changed")
                data=extract_rainfall()
                transform_rainfall(data)
                initial_file_content1 = new_content

        if event.src_path == original_drought_csv:
            global initial_file_content2
            with open(original_drought_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content2:
                print("original_drought.csv was changed")
                data=extract_drought()
                transform_drought(data)
                initial_file_content2 = new_content

        if event.src_path == original_cropproduction_csv:
            global initial_file_content3
            with open(original_cropproduction_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content3:
                print("original_cropproduction.csv was changed")
                data=extract_cropproduction()
                transform_cropproduction(data)
                initial_file_content3 = new_content

        if event.src_path == original_weather_csv:
            global initial_file_content4
            with open(original_weather_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content4:
                print("original_weather.csv was changed")
                data=extract_weather()
                transform_weather(data)
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
