import requests
import json
import unittest



auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)


#try to update info and
class TestDeleteWithCookie(unittest.TestCase):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()

    def setUp(self):
        self.port = "3001"
        self.site = "192.168.100.5"
        self.base_url = "http://" + self.site + ":" + self.port
        self.session.headers.update({'Content-Type': 'application/json'})
        #self.session.headers.update({'Accept': 'application/json'})

        print(self.base_url)


    def test_get_auth2(self):
        global response_token
        response = self.session.post(self.base_url + "/auth", cookies=self.jar, data=json_auth_value)
        response_token = json.loads(response.text)['token']

        cookie_obj = requests.cookies.create_cookie(domain=self.site, name="token", value=response_token)
        self.jar.set_cookie(cookie_obj)
        print(str(self.jar))
        self.assertEqual(response.status_code, 200)

    def test_remove_with_id(self):
         print("Cookies:"+ str(self.jar))
         response = self.session.delete(self.base_url + "/booking/8", cookies=self.jar)
         print(response.text)
         self.assertEqual(response.status_code, 201)

    def test_remove_with_invalid_id(self):
        print("Cookies:" + str(self.jar))
        response = self.session.delete(self.base_url + "/booking/15", cookies=self.jar)
        print(response.text)
        self.assertEqual(response.status_code, 405)




    def test_get_info(self):
        print("GET INFO")
        response = self.session.get(self.base_url + "/booking", cookies=self.jar)
        print(response.text)

        self.assertEqual(response.status_code, 200)

    # def test_delete_valid_id(self):
    #     print(str(self.jar))
    #     response = self.session.delete(self.base_url + "/booking/10", cookies=self.jar)
    #     print(response.text)
    #
    #     self.assertEqual(response.status_code, 201)
