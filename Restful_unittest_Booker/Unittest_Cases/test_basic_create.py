import requests
import json
import unittest
import jsonpath

head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
info1 = {'firstname': 'Chole',
         'lastname': 'Bryson',
         'totalprice': 230, 'depositpaid': False,
         'bookingdates': {'checkin': '2018-01-05', 'checkout': '2019-01-30'},
         'additionalneeds': 'Breakfast'}
info1_json = json.dumps(info1)

info2 = {'firstname': '',
         'lastname': '',
         'totalprice': '',
          'depositpaid': '',
         'bookingdates': {'checkin': '', 'checkout': ''},
         'additionalneeds': ''}

info2_json = json.dumps(info2)

info3 = {
         'lastname': 'Bryson',
         'totalprice': 230,
          'depositpaid': '',
         'bookingdates': {'checkin': '2018-01-05', 'checkout': '2019-01-30'},
         }

info3_json = json.dumps(info3)

replicate_info = {'firstname': 'Chole',
         'lastname': 'Bryson',
         'totalprice': 230, 'depositpaid': False,
         'bookingdates': {'checkin': '2018-01-05', 'checkout': '2019-01-30'},
         'additionalneeds': 'Breakfast'}

replicate_json = json.dumps(replicate_info)




class BookerApiGet(unittest.TestCase):

    def setUp(self):
        #self.url = "https://restful-booker.herokuapp.com"
        self.url = "http://192.168.100.5:3001"

    def test_create_new_booking(self):
        response = requests.post(self.url+"/booking", data=info1_json, headers=head)

        self.assertEqual(response.status_code, 200)

    def test_create_blank_info(self):
        response = requests.post(self.url+"/booking", data=info2_json, headers=head)

        self.assertEqual(response.status_code, 200)

    #status_code == 500, internal server error
    def test_create_flaw_info(self):
        response = requests.post(self.url + "/booking", data=info3_json, headers=head)
        print(response.status_code)

        self.assertEqual(response.status_code, 404)

    #status_code become 200
    def test_create_replicate_info(self):
        response = requests.post(self.url + "/booking", data=replicate_json, headers=head)
        print(response.status_code)

        self.assertEqual(response.status_code, 404)

