import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

def extract_rainfall():
    original_rainfall_csv = "originaldatasets/original_rainfall.csv"
    original_rainfall_csv_data = pd.read_csv(original_rainfall_csv)
    return original_rainfall_csv_data

def transform_rainfall(original_rainfall_csv_data):
    transformed_rainfall_csv_data = original_rainfall_csv_data.drop(columns=["JF", "MAM", "JJAS", "OND"])
    transformed_rainfall_csv_data = transformed_rainfall_csv_data.rename(columns={"SUBDIVISION": "State"})
    transformed_rainfall_csv_data=transformed_rainfall_csv_data.dropna()
    transformed_rainfall_csv_data.to_csv("transformeddatasets/transformed_rainfall.csv", index=False)

# Define the path to the CSV file you want to monitor
csv_file_path = 'originaldatasets\original_rainfall.csv'

# Create a variable to store the initial content of the file
initial_file_content = ''

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == csv_file_path:
            global initial_file_content
            with open(csv_file_path, 'r') as file:
                new_content = file.read()
            if new_content != initial_file_content:
                print("original_rainfall.csv was changed")
                data=extract_rainfall()
                transform_rainfall(data)
                initial_file_content = new_content
    print("hi")

if __name__ == "__main__":
    with open(csv_file_path, 'r') as file:
        initial_file_content = file.read()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(csv_file_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
