import requests
import json
import unittest


class RestApiTest2(unittest.TestCase):
    headers = {}

    def setUp(self):
        self.url = "https://restful-booker.herokuapp.com/booking"



    def test_create_booking(self):
        headers = {'Content-Type': 'application/json'}
        data = {
                    "firstname": "Lilian",
                    "lastname": "Siege",
                    "totalprice": 130,
                    "depositpaid": "true",
                    "bookingdates": {
                        "checkin": "2019-03-04",
                        "checkout": "2019-05-06"
                    },
                    "additionalneeds": "Notes"
                }

        print(type(data))
        json_data = json.dumps(data) #dumps/convert dict to json format
        print(type(json_data))
        response = requests.post(self.url, data=json_data, headers=headers)
        print(response.text)
        print(response.status_code)

        #print(response_json)

        self.assertEqual(response.status_code, 200)







    def tearDown(self):
        print("-----test is over------")

if __name__ == "__main__":
    unittest.main()


