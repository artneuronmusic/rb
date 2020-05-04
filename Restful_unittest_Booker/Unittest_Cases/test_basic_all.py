#I add session for this test due to adding cookie into the content
#open beginning and close in the end, it will be tested consistently

import requests
import json
import unittest
import jsonpath

head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
#head_json = json.dumps(head)



class BookerApiGet(unittest.TestCase):

    def setUp(self):
        #self.url = "https://restful-booker.herokuapp.com"
        self.url = "http://192.168.100.5:3001"

    #no verify the amount of books=>the data changed all the time
    def test_get_all(self):
        response = requests.get(self.url+"/booking")
        response_json = json.loads(response.text)
        amount_books = len(response_json)
        print("Total books: " + str(amount_books))
        print("Book list" + "\n" + str(response_json))
        print(response_json)


        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json)
        self.assertIsNotNone(amount_books)
        self.assertGreater(amount_books, 0)


    #check does id and info valid
    def test_get_book_by_id(self):
        response = requests.get(self.url+"/booking"+"/1")
        response_json = json.loads(response.text)
        res_first_name = jsonpath.jsonpath(response_json, "firstname")
        res_last_name = jsonpath.jsonpath(response_json, "lastname")
        res_totalprice = jsonpath.jsonpath(response_json, "totalprice")
        res_depositpaid= jsonpath.jsonpath(response_json, "depositpaid")
        res_bookingdates = jsonpath.jsonpath(response_json, "bookingdates")
        res_additionalneeds = jsonpath.jsonpath(response_json, "additionalneeds")
        print(response_json)
        #print(res_first_name)
        #print(res_last_name)
        #print(type(res_totalprice[0]))
        #print(res_depositpaid[0])
        #print(type(res_bookingdates[0]))
        #print(res_additionalneeds[0])

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_first_name)
        self.assertIsNotNone(res_last_name)
        self.assertTrue(res_totalprice[0], int)
        # Can't test, due to value changes often.
        #self.assertIs(res_depositpaid[0], False)
        self.assertTrue(res_bookingdates[0], dict)
        #self.assertEqual(res_additionalneeds[0], "Breakfast")


    #will be id 2
    #id 15 will be as the same as id 1?
    # When ID returns 404, no valid json is returned, causing below to fail.
    def test_not_exist_id(self):
        # Possibly better approach to find non-exist ID
        # get all /bookings
        # find last ID
        # get /booking/<id+1000>

        response = requests.get(self.url+"/booking"+"/99999999999")

        #response_json = json.loads(response.text)

        self.assertEqual(response.status_code, 404)

class BookerApiPost(unittest.TestCase):
    new_data = {
        "firstname": "Chole",
        "lastname": "Bryson",
        "totalprice": 230,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2018-01-05",
            "checkout": "2019-01-30"}, "additionalneeds": "Breakfast"}
    new_data_json = json.dumps(new_data)



    def setUp(self):
        # self.url = "https://restful-booker.herokuapp.com"
        self.url = "http://192.168.100.5:3001"

    def test_create_new_booking1(self):


        response = requests.post(self.url+"/booking", data=self.new_data_json, headers=head)
        self.assertEqual(response.status_code, 200)
        response.close()






























