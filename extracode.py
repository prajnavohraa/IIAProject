import mysql.connector
from datetime import datetime
from datetime import datetime, date, timedelta
import time
from colorama import Fore, Style, init

def print_progress_bar():
    total = 10
    for i in range(total + 1):
        progress = "========" * i + " " * (total - i)
        print(f"{Fore.GREEN}\r[{progress}] {i*10}/{total*10}{Style.RESET_ALL}", end="")
        time.sleep(0.1)
    print()

if __name__ == "__main__":
    print_progress_bar()
mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='root'
)

#Helper function to find maximum length of column needed for display
def find_max_col_length(recs, col_index, col_name):
    max_col_length = 0
    for record in recs:
        curr_length = len(str(record[col_index]))
        if curr_length > max_col_length:
            max_col_length = curr_length
    return max(max_col_length, len(col_name))


#Helper function to display the given table 'recs'
def display_table(recs, table_desciption):
    widths = []
    columns = []
    boundary = '|'
    separator = '+'
    index = 0
    
    for cd in table_desciption:
        widths.append(find_max_col_length(recs, index, cd[0]))
        columns.append(cd[0])
        index+=1
     
    for w in widths:
        boundary += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'
     
    print(separator)
    print(boundary % tuple(columns))
    print(separator)
    for row in recs:
        print(boundary % row)
    print(separator)


wallet = 20000
cursor=mydb.cursor()
# mydb.get_autocommit()
mydb.autocommit=True
# mydb.get_autocommit()
mycur.execute("USE farmerdatabase")

name=""
phoneNo=""
location=""
land_area=0
crop=""
month=""


#done
def past_rainfall(s,m):
    st = "SELECT AVG("+m+") FROM farmerrainfalltrend WHERE State='" + s + "'"
    
#    
def drought_prob(month,district):
    query="select mod_prob,severe_prob from farmerdroughttrend where District= "+ district + " and Month= "+ month + ";"


def crop_suggestion():
    ="Select State, District from  farmercropproduction where Season = 'Whole year' ; 
    #def crop_suggestion():
    #season = input("Enter the season: ")
    #query = "SELECT State, District FROM farmercropproduction WHERE Season = %s;"
    

def soil 
    
    

def crop_produce_stats(month,location, crop):
    location=location.upper()
    month=month.capitalize()
    crop=crop.capitalize()
    season = ''
    if month in ['January','February','March']:
        season = 'Rabi'
    elif month in ['April','May','June','July']:
        season = 'Kharif'
    else:
        season = 'Whole Year'
    query="select Area Production from farmercropproductionstatistics where District= "+ location + " and Season= "+ season + " and Crop="+ crop +";"


def main_menu():
    # pretty_menu.py
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════════════╗
    ║                                   Farmer's Aid                                   ║
    ╠══════════════════════════════════════════════════════════════════════════════════╣
    ║ 1. Past Rainfall: Check the district's historical rainfall trend.                ║
    ║ 2. Drought Probability: Assess the likelihood of drought in your district.       ║
    ║ 3. 10-Day Forecast: View the weather forecast for your district.                 ║
    ║ 4. Crop Recommendations: Identify the best crops for your location and season.   ║
    ║ 5. Soil Moisture: Access soil moisture statistics in your district.              ║
    ║ 6. Disease & Pest Threats: Learn about potential threats in your district.       ║
    ║ 7. 
    ╚══════════════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)
    choice = int(input("Enter your choice: "))

    if(choice == 1):
        past_rainfall()

    elif(choice==2):
        drought_prob()
    
    elif(choice==3):
        weather_forecast()
    
    elif(choice==4):
        crop_suggestion()

    elif(choice==5):
        soil_moisture()

    elif(choice==6):
        disease_pest()
    
    elif(choice==7):
        disease_pest()

    elif(choice==8):
        disease_pest()

    else:
        print("Invalid choice ! Please try again !")
        main_menu()



# loginid 78793 50220
# pwd PtSHC6 V6DkySD
####


if __name__ == "__main__":
    print_progress_bar()
    text = "---------------------------------Welcome to Farmer's Aid---------------------------------"
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()
    main_menu()
    print("-----------------------------------------------------------------------------------------")
