import mysql.connector
from mysql.connector import errors
import time
from colorama import Fore, Style, init
mydb=mysql.connector.connect(host = "localhost", user = "root", passwd = "12345")
import sys

mycur=mydb.cursor()
mycur.execute("USE farmerdatabase")

#menu func
def print_progress_bar():
    total = 10
    for i in range(total + 1):
        text = "========" * i + " " * (total - i)
        print(f"{Fore.GREEN}\r[{text}] {i*10}/{total*10}{Style.RESET_ALL}", end="")
        time.sleep(0.1)
    print()


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

def past_rainfall(s,m):
    s=s.capitalize()
    m=m.upper()
    print("\nCurrent State is",s,"\nDo you wish to change your State Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your state :",end="")
        s=input()
        print("State Updated for this Query !!")

    print("\nCurrent Month is",m,"\nDo you wish to change your month Y/N :",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your month :",end="")
        m=input()
        print("Month Updated for this Query !!")
    s=s.capitalize()
    
    st = "SELECT AVG("+m+") FROM farmerrainfalltrend WHERE State='" + s + "'"
    mycur.execute(st)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("No data available on it")
    else:
        print("\n\nDisplaying result for past rainfall:")
        # display_table(recs, mycur.description)
        amt = recs[0][0]
        print("\n\tThe average rainfall in "+ s +" for the month of "+m+ " is: "+ str(amt)+" mm")
        if(amt < 25): print("\tWe estimate Light Rainfall in your region based on past trends. Use water cautiously and save as much as possible for irrigation!")
        elif(amt >= 25 and amt < 150): print("\tWe estimate Moderate Rain in your region based on past trends. Reuse and Save water for later!")
        elif(amt >= 150 and amt < 550): print("\tWe estimate Heavy Rain in your region based on past trends. Set up water collection areas to save water for later!")
        elif(amt >= 550): print("\tWe estimate Extreme Rain based on past trends. Stay indoors!")
        print()

def drought_prob(district):
    print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        district=input()
        print("District Updated for this Query !!")
    district=district.capitalize()
    query="select AVG(Moderate_prob), AVG(Severe_prob) from farmerdroughttrend where District= '"+ district +"' group by State, District"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("No records found")
    else:
        print("\n\tFor the District",district,"\n\t The chances of Moderate drought is "+str(int(recs[0][0]))+" % \n\t The chances of Severe drought is "+str(int(recs[0][1]))+" %")

def weather_forecast(district):
    print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        district=input()
        print("District Updated for this Query !!")
    district=district.capitalize()
    query="select Date, tempmax as 'Max Temp' ,tempmin as 'Min Temp',temp as 'Temp',dew as 'Dew Point',humidity as 'Humidity (%)',precipprob as 'Precipitation (%)', windgust as 'WindGust(m/s)',windspeed as 'WindSpeed (m/s)',solarradiation as 'SolarRadiation (W/m.sq)',uvindex as 'UVIndex Scale' from farmerweatherforecast where District='"+ district +"'group by State, District, Date, tempmax,tempmin,temp,dew,humidity,precip,precipprob,windgust,windspeed,solarradiation,uvindex"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("No records found")
    else:
        print("\nDisplaying result for 15 days weather report\n") 
        display_table(recs, mycur.description) 

def crop_produce_stats(month, dist):
    crop=input("Enter the crop name to search for :")
    dist=dist.upper()
    month=month.capitalize()
    crop=crop.capitalize()
    
    print("\nCurrent Month is",month,"\nDo you wish to change your month Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your month :",end="")
        month=input()
        print("Month Updated for this Query !!")

    print("\nCurrent District is",dist.capitalize(),"\nDo you wish to change your district Y/N :",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        dist=input()
        print("District Updated for this Query !!")
    season = ''
    if month in ['Jan','Feb','Mar']:
        season = 'Rabi'
    elif month in ['Apr','May','Jun','Jul']:
        season = 'Kharif'
    elif month in ['Aug','Sep','Oct', 'Nov','Dec']:
        season ='Autumn'
    else:
        season = 'Whole Year'
    query="select AVG((Production)/(Area))  from farmercropproductionstatistics where District= '"+ dist +"' and Season like '%"+ season +"%' and Crop= '"+ crop +"'"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        land_area=int(input("Enter your land area(in acres) :"))
        profit_rate=recs[0][0]*land_area
        print("\n\tYour land can make a maximum yield of",int(profit_rate*10),"crops of",crop,"in",dist.capitalize(),"in the",season,"season.\n\n")

def crop_recommendation(month,dist):
    dist=dist.upper()
    month=month.capitalize()
    
    print("\nCurrent Month is",month,"\nDo you wish to change your month Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your month :",end="")
        month=input()
        print("Month Updated for this Query !!")

    print("\nCurrent District is",dist.capitalize(),"\nDo you wish to change your district Y/N :",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        dist=input()
        print("District Updated for this Query !!")
    season = ''
    if month in ['Jan','Feb','Mar']:
        season = 'Rabi'
    elif month in ['Apr','May','Jun','Jul']:
        season = 'Kharif'
    elif month in ['Aug','Sep','Oct', 'Nov','Dec']:
        season ='Autumn'
    else:
        season = 'Whole Year'

    print("\nDo you want it for all season? Y/N")
    choice=str(input()).lower()
    if(choice[0]=='y'):
         query="select District, Season, Crop, AVG(Production)/AVG(Area) as 'Produce per Acre'  from farmercropproductionstatistics where District= '"+ dist +"' group by Crop, Season;"
    else:   
        query="select District,'"+season+"' as 'Season', Crop, AVG(Production)/AVG(Area) as 'Produce per Acre'  from farmercropproductionstatistics where District= '"+ dist +"' and Season like '%"+ season +"%' group by Crop;"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        display_table(recs,mycur.description)
        sorted_data = sorted(recs, key=lambda x: x[3], reverse=True)
        print("\nThese are the top 3 Recommendations for",dist,"! Go Farm Dude")
        i=1
        # Display the first three records
        for record in sorted_data[:3]:
            print(i,". Crop =",record[2],'\tSeason =',record[1],'\tProduce per Acre =',record[3])
            i+=1
        print()

def pest_warning(st,district):
    print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        district=input()
        print("District Updated for this Query !!")
    district=district.capitalize()

    hum="select AVG(humidity) from farmerweatherforecast where District= '"+district+"'"
    temp= "select AVG(temp) from farmerweatherforecast where District= '"+district+"'"
    mycur.execute(hum)
    hum_recs=mycur.fetchall()
    humidity=str(hum_recs[0][0])

    mycur.execute(temp)
    temp_recs=mycur.fetchall()
    temperature=str(temp_recs[0][0])
    print()
    print("\tThe average humidity levels expected in "+ district +" in the next 10 days is: "+humidity+ " %")
    print("\tThe average temperature expected in "+ district +" in the next 10 days is: "+temperature+ " degree fahrenheit")
    if hum_recs[0][0]>=40 and temp_recs[0][0]>=76:
        print(f"{Fore.RED}WARNING!{Style.RESET_ALL}")
        print("\n\tBased on the forecasted information of humidity and temperature in next 15 days, there MAY be possibility of pest and disease in crops. PLease take appropriate actions to prevent it from happening.")
    else:
        print("\n\tBased on the forecasted information of humidity and temperature in next 15 days, there does not seem to be possibility of pest and disease in crops.")


def soil_moisture(district):
    print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        district=input()
        print("District Updated for this Query !!")
    dist = district.capitalize()
    print()
    query="select AVG(precip) as 'Precipitation (mm)', AVG(temp) as 'Temperature (deg F)', AVG(humidity) as 'Humidity (%)', AVG(windspeed) as 'WindSpeed (m/s)', AVG(solarradiation) as 'Solar Radiation (W/m.sq)' from farmerweatherforecast where District='"+ dist +"'"
    mycur.execute(query)
    recs=mycur.fetchall()
    precip = recs[0][0]
    temp = recs[0][1]
    humi = recs[0][2]
    wind = recs[0][3]
    solar = recs[0][4]
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        display_table(recs,mycur.description)

    if(humi > 60 and precip > 10 and temp < 25 and wind < 10 and solar < 5): 
        print("\nAccording to the above data, there is a probability of high soil moisture in your locality")
    else: print("\nAccording to the above data, You have moderate soil moisture in your locality.")

def aggregate_monthly(district):
    district = district.capitalize()
    print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        district=input()
        print("District Updated for this Query !!")
    query="SELECT DISTINCT CP.State, CP.District, CP.Crop, CP.Area as 'Area (acres)', CP.Production as 'Crops Produced', RT.YEAR, RT.ANNUAL as 'Annual Rainfall (mm)' FROM farmercropproductionstatistics CP JOIN farmerrainfalltrend RT ON CP.State = RT.State AND CP.Year = RT.YEAR WHERE CP.District =  '"+district+"'"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        display_table(recs,mycur.description)

def droughtCondition():
    # district = district.capitalize()
    # print("\nCurrent district is",district,"\nDo you wish to change your district Y/N : ",end="")
    # choice=str(input()).lower()
    # if(choice[0]=='y'):
    #     print("Enter your district :",end="")
    #     district=input()
    #     print("District Updated for this Query !!")
        
    print("\n\tThis option will give you information about how drought can affect the produce of crops in a particular season")
    query = '''SELECT DISTINCT CP.State, CP.District, CP.Year, CP.Season, AVG(CP.Production/CP.Area) as 'Produce per Area', DT.Moderate_prob, DT.Severe_prob
FROM farmercropproductionstatistics CP
JOIN farmerdroughttrend DT ON CP.State = DT.State AND CP.District = DT.District
WHERE DT.Moderate_prob > 20 AND DT.Severe_prob > 10 
GROUP BY CP.Season, CP.State, CP.District, CP.Year, DT.Moderate_prob, DT.Severe_prob;
'''
# District='"+ dist +"'"
    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        display_table(recs,mycur.description)


def comprehensiveInfo(dist, year):
    print("\nCurrent district is",dist,"\nDo you wish to change your district Y/N : ",end="")
    choice=str(input()).lower()
    if(choice[0]=='y'):
        print("Enter your district :",end="")
        dist=input()
        print("District Updated for this Query !!")
    
    dist = dist.upper()
    query = "SELECT Distinct CP.State, CP.District, CP.Year, CP.Season, CP.Crop, CP.Area, CP.Production, DT.Moderate_prob, DT.Severe_prob, RT.ANNUAL FROM farmercropproductionstatistics CP JOIN farmerdroughttrend DT ON UPPER(CP.District) = UPPER(DT.District) JOIN farmerrainfalltrend RT ON UPPER(CP.State) = UPPER(RT.State) AND CP.Year = RT.YEAR LEFT JOIN farmerweatherforecast WF ON UPPER(CP.State) = UPPER(WF.State) AND UPPER(WF.District) = '"+dist.upper()+"' AND CP.Year = YEAR(WF.Date) WHERE UPPER(CP.District) = '"+dist.upper()+"' AND CP.Year = '"+year+"'";    mycur.execute(query)
    recs=mycur.fetchall()
    if len(recs)==0:
        print("\nNo data is available on it")
    else:
        display_table(recs,mycur.description)

def main_menu():
    # pretty_menu.py
    print("\nPlease provide us with some basic information to help us provide you more accurate information!")
    input_state=input("\nEnter your state: ")
    input_district=input("Enter your district: ")
    input_month= input("Enter month: ")
    ans1='y'
    while(ans1=='y'):
        print(f"""{Fore.YELLOW}
        ╔══════════════════════════════════════════════════════════════════════════════════╗
        ║                                   Farmer's Aid                                   ║
        ╠══════════════════════════════════════════════════════════════════════════════════╣
        ║ 1. Past Rainfall: Check the district's historical rainfall trend.                ║
        ║ 2. Drought Probability: Assess the likelihood of drought in your district.       ║
        ║ 3. 15-Day Forecast: View the weather forecast for your district.                 ║
        ║ 4. Crop Production Statistics: Statistics of a crop like area and production     ║
        ║ 5. Soil Moisture: Access soil moisture statistics in your district.              ║
        ║ 6. Disease & Pest Threats: Learn about potential threats in your district.       ║
        ║ 7. Crop Recommendations: Identify the best crops for your location and season.   ║
        ║ 8. Monthly Weather Data for a district                                           ║
        ║ 9. Drought condition of Crop                                                     ║
        ║ 10. Comprehensive Information                                                    ║
        ║ 11. Exit from menu                                                               ║
        ╚══════════════════════════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        
        choice = int(input("\nEnter your choice: "))

        if(choice == 1):
            past_rainfall(input_state, input_month)

        elif(choice==2):
            drought_prob(input_district)
        
        elif(choice==3):
            weather_forecast(input_district)
        
        elif(choice==4):
            crop_produce_stats(input_month, input_district)

        elif(choice==5):
            soil_moisture(input_district)

        elif(choice==6):
            pest_warning(input_state, input_district)
        
        elif(choice==7):
            crop_recommendation(input_month, input_district)

        elif(choice==8):
            aggregate_monthly(input_district)

        elif(choice==9):
            droughtCondition()

        elif(choice==10):
            year = input("Enter the year corresponding to which you want to view information: ")
            comprehensiveInfo(input_district, year)

        elif(choice==11):
            # from art import text2art
            # goodbye_art = text2art("Goodbye")
            # print(goodbye_art)
            # ans1='n'
            break
        else:
            print("Invalid choice ! Please try again !")
            main_menu()
        continue

# loginid 78793 50220
# pwd PtSHC6 V6DkySD
####


# ans="Y"
# while(ans=="Y"):
#     main_menu()
#     ans=bool(input("Do you want to continue? Y/N"))
#     if(ans!="Y" or ans!="y"):
#         break
    

if __name__ == "__main__":
    print_progress_bar()
    text = "---------------------------------Welcome to Farmer's Aid---------------------------------"
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.025)
    print()

    ans='y'
    while(ans=='y'):
        main_menu()
        ans=str(input("Do you want to continue? Y/N")).lower()
        print(ans)
        if(ans[0]=='y'):
            continue
        else:
            break
    from art import text2art
    goodbye_art = text2art("Goodbye")
    print(goodbye_art)
    print(f"----------------------------------{Fore.YELLOW}Exiting. See You Soon!{Style.RESET_ALL}----------------------------------")
