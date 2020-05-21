import json
from flask import request
import os

def get_data():
    with open(os.getcwd() + '/Data/book_list.json', 'r') as f:
        id_json = json.loads(f.read()) #now is python dict
        #id_json.append(['{"firstname": "Tiffany", "lastname": "Lai", "totalprice": 230, "depositpaid": False, "bookingdates": {"checkin": "2018-01-05","checkout": "2018-01-07"}, "additionalneeds": "extra water bottles"}'])

    return id_json #get data return so u can use those data later


def create_data(data):
    # get existing data from file
    # put existing data in json dict
    # append existing json dict new data
    # write the data to file
    json_data = get_data()
    json_data.append(data) #python dict/list

    with open(os.getcwd() + '/Data/book_list.json', 'w') as f:

        json.dump(json_data, f) #write python into file in json formate
        #json.dumps(f.write(json_data))

def update_data(data):
    #with open(os.getcwd() + '/Data/book_list.json', 'r') as f:
     #   id_json = json.load(f)
        #id_json[id]["firstname"] = "Lily"
        #print(id_json)
    get_data()

    with open(os.getcwd() + '/Data/book_list.json', 'w') as f1:
        json.dump(data, f1)
        #f.write(json.dumps(id_json))










