import csv
import ast
import json

"""
    This script is for converting my previously saved json data
    to csv format.
    May be not helpful for anyone else!
"""

# Keys to get exact info from NASA-Dict
data_locations = ["title", "url", "date", "copyright",
                  "hdurl", "explanation", "media_type", "service_version"]

with open('nasa_data.csv', 'w') as nasa:
    with open('nasa_data.json', 'r') as json_data:
        data = json_data.read()
        # data = json.load(json_data)
        data = ast.literal_eval(data)
        print(type(data))
        d_data = csv.DictWriter(nasa, restval="-", fieldnames=data_locations)
        d_data.writeheader()
        d_data.writerows(data)
