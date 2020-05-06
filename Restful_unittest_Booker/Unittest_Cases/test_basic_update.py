import requests
import json
import unittest
import jsonpath

#credentials = '{}:{}'.format('admin', 'password123')
#encoded_credentials = base64.b64encode(credentials.encode('ascii'))
#base64string = base64.b64encode('username:admin', 'password:password123').decode('utf-8')
#auth_value = "Basic {}".format(encoded_credentials.decode('ascii'))

head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
head_json = json.dumps(head)

auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)

updating_info_all = {
    "firstname": "Judie",
    "lastname": "Duches",
    "totalprice": 500,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2019-01-01",
        "checkout": "2019-01-05"
    },
    "additionalneeds": "Room services: water bottles and some snacks"
}
json_updating_info_all = json.dumps(updating_info_all)

updating_info_with_flaw = {
    "firstname": "Judie",
    "lastname": "Duches",
    "totalprice": 500,
    "bookingdates": {
        "checkin": "2019-01-01",
    },
    "additionalneeds": "Room services: water bottles and some snacks"
}
json_updating_with_flaw = json.dumps(updating_info_with_flaw)

updating_info_with_some_empty = {
    "firstname": "",
    "lastname": "Duches",
    "totalprice": "",
    "bookingdates": {
        "checkin": "2019-01-01",
        "checkout": ""
    },
    "additionalneeds": "Room services: water bottles and some snacks"
}
json_with_some_empty =json.dumps(updating_info_with_some_empty)



#try to update info and
class TestUpdateWithCookie(unittest.TestCase):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()

    def setUp(self):
        self.port = "3001"
        self.site = "192.168.100.5"
        self.base_url = "http://" + self.site + ":" + self.port
        self.session.headers.update({'Content-Type': 'application/json'})
        self.session.headers.update({'Accept': 'application/json'})

        print(self.base_url)


    def test_get_auth2(self):
        global response_token
        response = self.session.post(self.base_url + "/auth", cookies=self.jar, data=json_auth_value)
        response_token = json.loads(response.text)['token']
        print(response.status_code)
        print(response_token)
        cookie_obj = requests.cookies.create_cookie(domain=self.site, name="token", value=response_token)
        self.jar.set_cookie(cookie_obj)
        print(str(self.jar))
        self.assertEqual(response.status_code, 200)

    def test_update_info_valid_id(self):
        print(str(self.jar))

        response = self.session.put(self.base_url + "/booking/3", cookies=self.jar, data=json_updating_info_all)
        print(response.text)

        self.assertEqual(response.status_code, 200)

    #show 400 code with not complete info + bad request
    def test_update_valid_id_with_some_empty_info(self):
        print(str(self.jar))

        response = self.session.put(self.base_url + "/booking/4", cookies=self.jar, data=json_with_some_empty)
        print(response.text)

        self.assertEqual(response.status_code, 400)

    #it will be 400 insteqd of 500
    def test_update_valid_id_with_flaw_info(self):
        print(str(self.jar))

        response = self.session.put(self.base_url + "/booking/5", cookies=self.jar, data=json_updating_with_flaw)
        print(response.text)

        self.assertEqual(response.status_code, 400)


    #method is not allowed, and the error will be 405
    def test_update_invalid_id_with_info(self):
        print(str(self.jar))

        response = self.session.put(self.base_url + "/booking/99999", cookies=self.jar, data=json_updating_info_all)
        print(response.text)

        self.assertEqual(response.status_code, 405)






