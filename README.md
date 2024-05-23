# Weather Monitoring and Drought Assessment for Farmers

Project, "Weather Monitoring and Drought Assessment for Farmers," provides a platform through which farmers can access accurate and relevant information concerning vital factors like crop conditions, weather patterns, rainfall, and drought. This information will help them make appropriate decisions to help get better overall crop production.
In this document, we mention the various methods/algorithms used to extract, transform and load information into our database. We also mention schema matching and mapping, which helped us create a uniform database which can be unified together. 

## ETL(Extract, Transform, Load) Performed:
We begin ETL(Extract, Transform and Load) by extracting our data from sources like data.gov.in, open-meteo.com, indiawaterportal.org, etc. These data sources form the base of our database to provide concise and essential information to farmers. We use four datasets in our database, which give information regarding weather, drought, rainfall and crop production. Each of these factors plays a crucial role in the decision-making of a crop for the farmers. Using the information we provide on our platform, farmers can make informed decisions about their cropping practices and crop choices. 

### Importing Libraries:
The script starts by importing the necessary libraries such as time, os, pandas, watchdog, and sqlalchemy. These libraries are used for file handling, data processing, and database interactions.

### CSV File Paths:
It defines file paths for several CSV files (original, rainfall_csv, original_cropproduction_csv, original_drought_csv, and original_weather_csv), which will be used to provide information to the users(farmers).

### Data Extraction:
There are functions to extract data from these CSV files using pandas and return the data as DataFrames. There are functions to extract data from these CSV files using pandas and return the data as DataFrames (e.g., extract_rainfall, extract_cropproduction, extract_drought, extract_weather). Several functions (extract_rainfall, extract_cropproduction, extract_drought, and extract_weather) are defined to read the data from these CSV files using the Pandas library. The extracted data is stored in DataFrames.

## Data Transformation:
The transform_rainfall(), transform_cropproduction(), transform_drought(), and transform_weather() functions transform the data into a format that is compatible with the MySQL database. 
For rainfall data, columns 'JF', 'MAM', 'JJAS', and 'OND' are dropped, and the 'SUBDIVISION' column is renamed to 'State'. Rows with missing data are removed. The transformed data is then saved as a new CSV file in the 'transformeddatasets' directory.
For crop production data, columns 'State_Name', 'District_Name', and 'Crop_Year' are renamed to 'State', 'District', and 'Year', respectively. Rows with missing data are removed, and the transformed data is saved as a new CSV file.
For drought data, columns 'ModerateDroughtProbability' and 'SevereDroughtProbability' are renamed to 'Moderate_prob' and 'Severe_prob'. Rows with missing data are removed, and the transformed data is saved as a new CSV file.
For weather data, several columns ('sealevelpressure', 'winddir', 'cloudcover', 'visibility', 'severerisk') are dropped. Column names 'name' and 'datetime' are renamed 'District' and 'Date', respectively. Rows with missing data are removed, and the transformed data is saved as a new CSV file.

### Database Connection:
The script establishes a database connection using SQLAlchemy to a MySQL database named 'farmerdatabase'. The connection details, including the username, password, host, and port, are defined.

### Data Loading:
The Script defines functions for loading data into the SQL database globally and locally into specific tables. The local_loading() function loads the data into the MySQL database.
Two functions for data loading are defined:
global_loading loads the transformed data from all datasets (rainfall, drought, crop production, and weather) into separate database tables.
local_loading is a generic function to load any data and specify the target table name.
The script then extracts and transforms data for each dataset (rainfall, drought, crop production, and weather) and loads it into the corresponding database tables.

### Incremental View Approach:
The script creates a MyHandler class inherited from the FileSystemEventHandler class. The MyHandler class overrides the on_modified() method to handle file change events. The on_modified() method extracts, transforms and loads the updated data from the CSV file that was changed.
The script then creates an Observer object and schedules the MyHandler object to monitor the directories containing the CSV files. 
The script then starts the Observer object and enters a loop where it waits for file change events. When a file change event is detected, the Observer object calls the on_modified() method of the MyHandler object.

### File System Monitoring:
To monitor changes to the original CSV files, the script uses the watchdog library to detect modifications. It sets up separate monitoring for each CSV file.
When a file is modified, the corresponding event handler is triggered. It checks for changes in the file's content, re-extracts and transforms the data if necessary, and reloads it into the respective database table.

### Observation Loop:
The script enters an observation loop to monitor changes to the CSV files continuously. It sleeps for 1 second between checks and can be interrupted by a keyboard interrupt (Ctrl+C).

### Summary Note:
The script automates the ETL process for multiple datasets related to agriculture and weather by monitoring changes in the original data files, updating the transformed data, and loading it into a MySQL database.
This automation ensures that the database remains up-to-date with the latest data from the original CSV files, which can be valuable for applications in agriculture and weather forecasting.
