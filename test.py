
# Richard Lin
# Since Longitude of American cities are negative (west of Prime Meridian)
# we will replace the longitude values with negative conversions.

# run on terminal $python3 -m pip install requests (in case of no library)

# importing the requests library 
# treat the longitude coordinates as negative
import requests 
import re
import json

locations = []
points = []
input = open("input.txt", "r")

for line in input:
    locations.append(line)

# loop to retrieve coordinate points and put into array of lat/long coords
for element in locations:
    coords = re.findall('\d*\.?\d+',element)
    coords[1] = "-"+coords[1] #notice how a negative sign is added to the longitude value
    points.append(coords)

grid_links = []
# Retrieving forecast links
# finds forcast links for each individual location using requests library
for point in points:
    link = "https://api.weather.gov/points/" + point[0] + "," + point[1]
    response = requests.get(link)
    response_dict = response.json()
    properties_dict = response_dict['properties']
    forecast_grid = properties_dict['forecast']
    grid_links.append(forecast_grid)

# temperature_list
# finds Wednesday Night temperatures by converting json response to dictionaries
# dictionaries are turned to smaller dictionaries to access final "temperature" key
# the temperatures are appended to the "temperature_list" array
temperature_list = []
for link in grid_links:
    response = requests.get(link)
    response_dict = response.json()
    properties_dict = response_dict['properties']
    periods_list = properties_dict['periods'] 
    for period in periods_list:
        if period["name"] == "Wednesday Night":
            temperature_list.append(period["temperature"])

final_str = str(temperature_list).strip('[]')

# write to output.txt file

f = open("output.txt","w")
f.write(final_str)
f.close()