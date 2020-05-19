import json
from flask import request

def get_data():
    with open('/Users/yuchienhuang/PycharmProjects/python_api_testing/Restful_unittest_Booker/Mock_Flask/Data/book_list.json', 'r') as f:
        id_json = json.loads(f.read())
        #id_json.append(['{"firstname": "Tiffany", "lastname": "Lai", "totalprice": 230, "depositpaid": False, "bookingdates": {"checkin": "2018-01-05","checkout": "2018-01-07"}, "additionalneeds": "extra water bottles"}'])

    return id_json



