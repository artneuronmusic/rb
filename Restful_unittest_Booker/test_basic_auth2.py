import requests
import json
import unittest


#head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)

updating_info_all = {
    "firstname": "James",
    "lastname": "Brown",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-12-01",
        "checkout": "2019-01-30"
    },
    "additionalneeds": "Notebook and computer"
}
json_updating_info_all = json.dumps(updating_info_all)


class TestAuth(unittest.TestCase):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()

    def setUp(self):
        self.site = "restful-booker.herokuapp.com"
        self.base_url = "https://" + self.site
        self.session.headers.update({"Accept": "application/json"})
        self.session.headers.update({"Content-Type": "application/json"})

    def test_create_auth(self):
        response = self.session.post(self.base_url + "/auth", cookies=self.jar, data=json_auth_value)
        response_token = json.loads(response.text)['token']
        print(type(response_token))

        # set cookie with authentication token
        print("resp_token: " + response_token)
        cookie_obj = requests.cookies.create_cookie(domain=self.site, name="token", value=response_token)
        self.jar.set_cookie(cookie_obj)

        print("cookie_obj: " + str(cookie_obj))

        self.assertEqual(response.status_code, 200)


    def test_update_booking(self):
        print(str(self.jar))
        response1 = self.session.get(self.base_url + "/booking/1", cookies=self.jar)
        print("resp1_text: " + response1.text)

        response = self.session.put(self.base_url + "/booking/1", cookies=self.jar, data=json_updating_info_all)

        response2 = self.session.get(self.base_url + "/booking/1", cookies=self.jar)
        print("resp2_text: " + response2.text)

        self.assertEqual(response.status_code, 200)


    def test_delete_booking(self):
        print(self.jar.get("restful-booker.herokuapp.com"))
        response = self.session.delete(self.base_url + "/booking/2", cookies=self.jar)
        self.assertEqual(response.status_code, 201)

    def test_get_booking(self):
        #print(self.jar.get("restful-booker.herokuapp.com"))
        response = self.session.delete(self.base_url + "/booking/2")
        print(response.text)
        self.assertNotEqual(response.status_code, 200)






    def tearDown(self):
        self.session.close()
        print("----test is over----")




if __name__=="__main__":
    unittest.main()
