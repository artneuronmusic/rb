"""
*the final goal is to make codes neat and clean and reusable
*put those tests together will encounter failures most of time, because the data will changed by different functions,
*after this, i would suggest to use pytest or BDD testing or regression testing to solve the order issue
*or try mock flask


Features:
    - Common get/post function to
        * Print every request and response in a API output file
        * Append common headers
"""
import requests
import json
import unittest
import logging
import os
import inspect
import sys


#this one can help ur unittest not run in order
#unittest.TestLoader.sortTestMethodsUsing = None
#import jsonpath


# logging.basicConfig(filename='/path/to/file.log', filemode='w', level=logging.DEBUG)

if sys.version_info[0] < 3:
    raise Exception("Requires Python 3 or above please.")

#set beginning for debug, info, warning, error, crititcal
LOG_LEVEL = logging.INFO

#scripts-->logs -->run

# root_path is parent folder of Scripts folder (one level up)
root_path = os.path.dirname( os.path.dirname(os.path.realpath(__file__)))

# create formatter
common_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

# Note: To create multiple log files, must use different logger name.
def setup_logger(log_file, level=logging.INFO, name='', formatter=common_formatter):

    handler = logging.FileHandler(log_file, mode='w')  # default mode is append
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# logger ofr default debug
debug_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
debug_log_filename = root_path + os.sep + 'Logs' + os.sep + 'debug.log'
log = setup_logger(debug_log_filename, LOG_LEVEL,'log', formatter=debug_formatter)


# logger for API outputs
api_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
api_outputs_filename = root_path + os.sep + 'Logs' + os.sep + 'api_outputs.log'
log_api = setup_logger(api_outputs_filename, LOG_LEVEL,'log_api', formatter=api_formatter)

head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
#head_json = json.dumps(head, indent=4)
auth_value = {
    "username": "admin",
    "password": "password123"
}
json_auth_value = json.dumps(auth_value)


class BookerApiAll(unittest.TestCase):
    jar = requests.cookies.RequestsCookieJar()
    session = requests.session()
    content_type = {'Content-Type': 'application/json'}
    accept = {'Accept': 'application/json'}

    def setUp(self):
        log.debug('To load test data.')
        self.port = "3001"
        self.site = "192.168.100.5"
        self.base_url = "http://" + self.site + ":" + self.port
        self.session.headers.update(self.content_type)
        self.session.headers.update(self.accept)


    #We can get all booking collection
    def test_get_all(self):
        print("1. GET ALL")
        response = requests.get(self.base_url+"/booking")
        response_json = json.loads(response.text)
        amount_books = len(response_json)
       # print("Total books: " + str(amount_books))
        #print("Book list" + "\n" + str(response_json))
        print(response_json)
        print("Total bookings: " + str(amount_books))
        print("*****************")


        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json)
        self.assertIsNotNone(amount_books)
        self.assertGreater(amount_books, 0)
        log.info('Test %s passed.' % inspect.stack()[0][3])


    #checking valid booking id:1
    def test_get_book_by_valid_id(self):
        print("2. Get book info by id")
        response = requests.get(self.base_url+"/booking"+"/1")
        response_json = json.loads(response.text)
        print(response_json)


        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json['firstname'])
        self.assertIsNotNone(response_json['lastname'])
        self.assertTrue(response_json['totalprice'], int)
        self.assertIsInstance(response_json['depositpaid'], bool)
        self.assertIsInstance(response_json['bookingdates'], dict)
        self.assertFalse('additionalneeds' in response_json.keys())
        log.info('Test %s passed.' % inspect.stack()[0][3])


    #invalid id: 99999
    def test_get_book_by_not_exist_id(self):
        print("3. Get book info by invalid id")
        response = requests.get(self.base_url + "/booking"+"/99999")
        print(response.status_code)

        self.assertEqual(response.status_code, 404)
        log.info('Test %s passed.' % inspect.stack()[0][3])



    def test_create_valid_booking(self):
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
        log.info('Test %s passed.' % inspect.stack()[0][3])


    #same last&first name can be double booking, there is no restriction for this
    def test_create_replicated_booking(self):
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
        log.info('Test %s passed.' % inspect.stack()[0][3])


    #the system will not take the request with some missing info
    def test_create_booking_with_missing_info(self):
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

        response = requests.post(self.base_url+ "/booking", data=json_updating_with_flaw, headers=head)
        self.assertEqual(response.status_code, 500)
        log.info('Test %s passed.' % inspect.stack()[0][3])


    def test_create_booking_some_empty_info(self):
        print("7. Booking: empty_info")
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
        json_with_some_empty = json.dumps(updating_info_with_some_empty)

        response = requests.post(self.base_url+ "/booking", data=json_with_some_empty, headers=head)
        self.assertEqual(response.status_code, 500)
        log.info('Test %s passed.' % inspect.stack()[0][3])


    def test_auth_token(self):
        print("8. get Auth for cookies")

        response = self.session.post(self.base_url+"/auth", cookies=self.jar, data=json_auth_value)
        response_token = json.loads(response.text)['token']
        cookie_obj = requests.cookies.create_cookie(domain=self.site, name="token", value=response_token)

        self.jar.set_cookie(cookie_obj)
        print(str(self.jar))
        self.assertEqual(response.status_code, 200)
        log.info('Test %s passed.' % inspect.stack()[0][3])



    #id:3
    def test_update_info_valid_id(self):
        print("9. update_for valid_id")
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

        response_get = requests.get(self.base_url+"/booking"+"/2")
        get_json = json.loads(response_get.text)
        print(get_json)

        print(str(self.jar))
        response_update = self.session.put(self.base_url + "/booking/3", cookies=self.jar, data=json_updating_info_all)
        update_json = json.loads(response_update.text)
        print(update_json)

        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(update_json["firstname"], "Judie")
        self.assertEqual(update_json["lastname"], "Duches")
        log.info('Test %s passed.' % inspect.stack()[0][3])



    #id:4
    def test_update_valid_id_some_empty_info(self):
        print("10. update")

        updating_info_with_some_empty = {
            "firstname": "",
            "lastname": "Duches",
            "totalprice": "",
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": ""
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }
        json_with_some_empty = json.dumps(updating_info_with_some_empty)
        response = self.session.put(self.base_url + "/booking/4", cookies=self.jar, data=json_with_some_empty )
        update_json = json.loads(response.text)


        self.assertEqual(response.status_code, 200)
        log.info('Test %s passed.' % inspect.stack()[0][3])


    #id:99
    #needs explanation for error return instead of just fails

    def test_update_with_invalid_id(self):
        print("11. update for invalid_id")
        updating_info_all = {
            "firstname": "Williams",
            "lastname": "Dretch",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-01-05"
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }
        json_with_some_empty = json.dumps(updating_info_all)

        response = self.session.put(self.base_url + "/booking/99", cookies=self.jar, data=json_with_some_empty)
        #update_json = json.loads(response.text)
        #print("Update with invalid id: "+update_json)

        self.assertEqual(response.status_code, 405)
        log.info('Test %s passed.' % inspect.stack()[0][3])

    #id:1
    def test_partial_update(self):
        print("12. partial update")
        partial_updating = {
            "firstname": "Lisa",
            "lastname": "Morrison"}
        json_partial = json.dumps(partial_updating)

        response = self.session.patch(self.base_url + "/booking/1", cookies=self.jar, data=json_partial)
        update_json = json.loads(response.text)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_json["firstname"], "Lisa")
        log.info('Test %s passed.' % inspect.stack()[0][3])

    #id: 5
    def test_remove_with_id(self):
        print("13. delete id")
        print("Cookies:" + str(self.jar))
        response = self.session.delete(self.base_url + "/booking/5", cookies=self.jar)
        print(response.text)
        self.assertEqual(response.status_code, 201)
        log.info('Test %s passed.' % inspect.stack()[0][3])

    #id: 9999
    def test_remove_with_invalid_id(self):
        print("Cookies:" + str(self.jar))
        response = self.session.delete(self.base_url + "/booking/9999", cookies=self.jar)
        print(response.text)
        self.assertEqual(response.status_code, 405)
        log.info('Test %s passed.' % inspect.stack()[0][3])

    def tearDown(self):
        print("                \n")
        print("This test is done")



if __name__ == "__main__":
    unittest.main()
























