# # import requests
# # import json
# # api_url = "https://api.data.gov.in/resource/8e0bd482-4aba-4d99-9cb9-ff124f6f1c2f?api-key=579b464db66ec23bdd00000195fe2791b8854ab956968311da0c0e59&format=json"

# # #making an API request
# # response = requests.get(api_url)

# # if response.status_code == 200: #if request is successful
# #     #parsing the json response
# #     data = json.loads(response.text)
    
# # print(data)


# import requests
# import json

# api_response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=31.6223&longitude=74.8753&hourly=temperature_2m,precipitation,rain,showers&daily=weathercode&timezone=auto')
# print(api_response.status_code)
# data = api_response.text
# parse_json = json.loads(data)
# for i in parse_json:
#     print(i:parse_json[i])