#!/usr/bin/env pytest -vv -s
import requests
import json
import unittest
import base64



#credentials = '{}:{}'.format('admin', 'password123')
#encoded_credentials = base64.b64encode(credentials.encode('ascii'))
#base64string = base64.b64encode('username:admin', 'password:password123').decode('utf-8')
#auth_value = "Basic {}".format(encoded_credentials.decode('ascii'))

head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)

updating_info_all = {
    "firstname": "James",
    "lastname": "Brown",
    "totalprice": 200,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-12-01",
        "checkout": "2019-01-30"
    },
    "additionalneeds": "Notebook and computer"
}
json_updating_info_all = json.dumps(updating_info_all)


class TestAuth(unittest.TestCase):


    def setUp(self):

        self.url = "https://restful-booker.herokuapp.com"

    def test_get_auth(self):
        response = requests.post(self.url + '/auth', data=json_auth_value, headers=head)
        json_response = json.loads(response.text)
        print(type(json_response['token']))
        new_cookie = 'Cookie: token={}'.format(json_response['token'])
        print(new_cookie)

        self.assertEqual(response.status_code, 200)

    def test_update_info(self):

        # auth request
        response = requests.post(self.url + '/auth', data=json_auth_value, headers=head)
        print("resp_code: " + str(response.status_code))
        print("resp_head: " + str(response.headers))
        print("resp_text: " + response.text)

        json_response = json.loads(response.text)
        print("json_response: " + str(json_response))
        new_cookie = 'token={}'.format(json_response['token'])
        print("new_cookie: " + new_cookie)

        #new_cookie_json = {"Cookie": 'token={}'.format(json_response)}
        #print(new_cookie_json)
        #print(type(new_cookie_json))

        # booking update
        head2 = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Cookie': new_cookie}

        print("req_headers: " + str(head2))

        response2 = requests.put(self.url + '/booking' + '/10', data=json_updating_info_all, headers=head2)

        print("resp2_code: " + str(response2.status_code))
        print("resp2_head: " + str(response2.headers))
        print("resp2_text: " + response2.text)

        self.assertEqual(response2.status_code, 200)






    def tearDown(self):
        print("-----test is over------")

if __name__ == "__main__":
    unittest.main()
