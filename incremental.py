import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd


#csv file paths
original_rainfall_csv = "originaldatasets\original_rainfall.csv"
original_cropproduction_csv = "originaldatasets\original_cropproduction.csv"
original_drought_csv = "originaldatasets\original_drought.csv"
original_districtmapping_csv = "originaldatasets\original_districtmapping.csv"


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

def extract_districtmapping():
    original_districtmapping_csv = "originaldatasets\original_districtmapping.csv"
    original_districtmapping_csv_data = pd.read_csv(original_districtmapping_csv)
    return original_districtmapping_csv_data


#transformation
def transform_rainfall(original_rainfall_csv_data):
    transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
    transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
    transformed_rainfall_csv_data=transformed_rainfall_csv_data.dropna()
    transformed_rainfall_csv_data.to_csv("transformeddatasets/transformed_rainfall.csv", index=False)


def transform_cropproduction(original_cropproduction_csv_data):
    

# Define the path to the CSV file you want to monitor
# csv_file_path = 'originaldatasets\original_rainfall.csv'

# Create a variable to store the initial content of the file
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
                data=extract_rainfall()
                transform_rainfall(data)
                initial_file_content2 = new_content

        if event.src_path == original_cropproduction_csv:
            global initial_file_content3
            with open(original_cropproduction_csv, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content3:
                print("original_cropproduction.csv was changed")
                data=extract_rainfall()
                transform_rainfall(data)
                initial_file_content3 = new_content

        
    

if __name__ == "__main__":
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

    # with open(original_cropproduction_csv, 'r') as file:
    #     initial_file_content = file.read()

    # event_handler = MyHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path=os.path.dirname(original_cropproduction_csv), recursive=False)
    # observer.start()

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()

    # with open(original_rainfall_csv, 'r') as file:
    #     initial_file_content = file.read()

    # event_handler = MyHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path=os.path.dirname(original_rainfall_csv), recursive=False)
    # observer.start()

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()
