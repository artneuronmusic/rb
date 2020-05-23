import requests
import json
import unittest
import logging
import os
import inspect
import sys


head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
#head_json = json.dumps(head, indent=4)
auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)



class Monolithic(unittest.TestCase):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()
    content_type = {'Content-Type': 'application/json'}
    accept = {'Accept': 'application/json'}



    def setUp(self):

        self.port = "3001"
        self.site = "192.168.100.5"
        # self.site = "127.0.0.1"
        # self.site = ""
        self.base_url = "http://" + self.site + ":" + self.port
        self.session.headers.update(self.content_type)
        self.session.headers.update(self.accept)

    def step_testName1(self):

        print("1. GET ALL")
        response = requests.get(self.base_url + "/booking")
        response_json = json.loads(response.text)
        amount_books = len(response_json)
        # print("Total books: " + str(amount_books))
        # print("Book list" + "\n" + str(response_json))
        print(response_json)
        print("Total bookings: " + str(amount_books))
        print("*****************")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json)
        self.assertIsNotNone(amount_books)
        self.assertGreater(amount_books, 0)



    def step_testName2(self):

        print("2. Get book info by id")
        response = requests.get(self.base_url + "/booking" + "/1")
        response_json = json.loads(response.text)
        print(response_json)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json['firstname'])
        self.assertIsNotNone(response_json['lastname'])
        self.assertTrue(response_json['totalprice'], int)
        self.assertIsInstance(response_json['depositpaid'], bool)
        self.assertIsInstance(response_json['bookingdates'], dict)
        # self.assertFalse('additionalneeds' in response_json.keys())



    def step_testName3(self):

        print("3. Get book info by invalid id")
        response = requests.get(self.base_url + "/booking" + "/99999")
        print(response.status_code)

        self.assertEqual(response.status_code, 404)



    def step_testName4(self):
        print("4. Booking with complete info")

        new_data = {
            "firstname": "Chole",
            "lastname": "Bryson",
            "totalprice": 230,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2018-01-05",
                "checkout": "2018-01-07"}, "additionalneeds": "extra water bottles"}
        new_data_json = json.dumps(new_data)

        print("******************")

        response = requests.post(self.base_url + "/booking", data=new_data_json, headers=head)
        response_json = json.loads(response.text)
        print("New booking id: " + str(response_json["bookingid"]))
        self.assertEqual(response.status_code, 200)



    def step_testName5(self):

        print("5. Booking with replicated info")
        new_data = {
            "firstname": "Chole",
            "lastname": "Bryson",
            "totalprice": 230,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2018-01-05",
                "checkout": "2018-01-07"}, "additionalneeds": "extra water bottles"}
        new_data_json = json.dumps(new_data)

        response = requests.post(self.base_url + "/booking", data=new_data_json, headers=head)
        response_json = json.loads(response.text)
        print("New booking id: " + str(response_json["bookingid"]))
        self.assertEqual(response.status_code, 200)



    def step_testName6(self):

        print("6. Booking: missing_info")
        updating_info_with_flaw = {
            "lastname": "Duches",
            "totalprice": 500,
            "bookingdates": {
                "checkin": "2019-01-01",
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }
        json_updating_with_flaw = json.dumps(updating_info_with_flaw)

        response = requests.post(self.base_url + "/booking", data=json_updating_with_flaw, headers=head)
        self.assertEqual(response.status_code, 500)



    def step_testName7(self):
        print("7. Booking: empty_info")

        updating_info_with_some_empty = {
            "firstname": "",
            "lastname": "Duches",
            "totalprice": "",
            "depositpaid": None,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": ""
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }
        json_with_some_empty = json.dumps(updating_info_with_some_empty)

        response = requests.post(self.base_url + "/booking", data=json_with_some_empty, headers=head)
        self.assertEqual(response.status_code, 500)


    #this one go first??? why????
    def step_testName8(self):

        print("8. get Auth for cookies")

        response = self.session.post(self.base_url + "/auth", cookies=self.jar, data=json_auth_value)
        response_token = json.loads(response.text)['token']
        cookie_obj = requests.cookies.create_cookie(domain=self.site, name="token", value=response_token)

        self.jar.set_cookie(cookie_obj)
        print(str(self.jar))


        self.assertEqual(response.status_code, 200)



    def step_testName9(self):
        print("9. update_for valid_id")

        updating_info_all = {
            "firstname": "Antha",
            "lastname": "ruben",
            "totalprice": 500,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-01-05"
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }

        json_updating_info_all = json.dumps(updating_info_all)

        response_get = requests.get(self.base_url + "/booking" + "/2")
        get_json = json.loads(response_get.text)
        print(get_json)
        print("UPDATE SECTION 8")
        print(str(self.jar))
        # response_update = self.session.put(self.base_url + "/booking/8", cookies=self.jar, data=json_updating_info_all)
        # update_json = json.loads(response_update.text)
        # print(update_json)
        #
        # self.assertEqual(response_update.status_code, 200)


    '''
    this step way,  does not work since step10-step14
    
    '''


    def step_testName10(self):
        print("10")
        updating_info_all = {
            "firstname": "",
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
        print("SECTION 9")
        print(str(self.jar))

        # print(str(self.jar))
        # response_update = self.session.put(self.base_url + "/booking/19", cookies=self.jar, data=json_updating_info_all)
        # print("ITS TEN")
        # print(response_update.text)
        # update_json = json.loads(response_update.text)
        # print(update_json)
        #
        # #self.assertEqual(response_get.status_code, 200)
        # self.assertEqual(response_update.status_code, 200)



    # def step11_testName11(self):
    #     print("11. update for invalid_id")
    #
    #     updating_info_all = {
    #         "firstname": "Williams",
    #         "lastname": "Dretch",
    #         "totalprice": 100,
    #         "depositpaid": True,
    #         "bookingdates": {
    #             "checkin": "2019-01-01",
    #             "checkout": "2019-01-05"
    #         },
    #         "additionalneeds": "Room services: water bottles and some snacks"
    #     }
    #     json_with_some_empty = json.dumps(updating_info_all)
    #
    #     response = self.session.put(self.base_url + "/booking/99", cookies=self.jar, data=json_with_some_empty)
    #     # update_json = json.loads(response.text)
    #     # print("Update with invalid id: "+update_json)
    #
    #     self.assertEqual(response.status_code, 405)
    #
    #

    # def step12_testName12(self):
    #     print("12. partial update")
    #
    #     partial_updating = {
    #         "firstname": "Lisa",
    #         "lastname": "Morrison"}
    #     json_partial = json.dumps(partial_updating)
    #
    #     response = self.session.patch(self.base_url + "/booking/1", cookies=self.jar, data=json_partial)
    #     update_json = json.loads(response.text)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(update_json["firstname"], "Lisa")
    #

    #
    # def step13_testName13(self):
    #
    #     print("13. delete id")
    #     print("Cookies:" + str(self.jar))
    #     response = self.session.delete(self.base_url + "/booking/5", cookies=self.jar)
    #     print(response.text)
    #     self.assertEqual(response.status_code, 201)
    #
    #
    #
    # def step14_testName14(self):
    #     print("Cookies:" + str(self.jar))
    #
    #     response = self.session.delete(self.base_url + "/booking/9999", cookies=self.jar)
    #     print(response.text)
    #     self.assertEqual(response.status_code, 405)


    #
    # def tearDown(self):
    #     print("                \n")
    #
    #     print("This test is done")
    #     # requests.session(config={'keep_alive': False})


    def _steps(self):

        '''
        Generates the step methods from their parent object
        '''
        for name in sorted(dir(self)):
             if name.startswith('step'):

                  yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()

            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))
        # for name, step in self._steps():
        #     try:
        #         step()
        #     except Exception as e:
        #         self.fail("{} failed ({}: {})".format(step, type(e), e))
    #     '''
    #           Run the individual steps associated with this test
    #     '''
    #     # Create a flag that determines whether to raise an error at
    #     # the end of the test
    #     failed = False
    #
    #     # An empty string that the will accumulate error messages for
    #     # each failing step
    #     fail_message = ''
    #     for name, step in self.steps():
    #         try:
    #             step()
    #         except Exception as e:
    #             # A step has failed, the test should continue through
    #             # the remaining steps, but eventually fail
    #             failed = True
    #
    #             # get the name of the method -- so the fail message is
    #             # nicer to read :)
    #             name = name.split('_')[1]
    #             # append this step's exception to the fail message
    #             fail_message += "\n\nFAIL: {}\n {} failed ({}: {})".format(name, step, type(e),e)
    #
    #
    #     # check if any of the steps failed
    #     if failed is True:
    #         # fail the test with the accumulated exception message
    #         self.fail(fail_message)