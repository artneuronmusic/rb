import requests
import json
import unittest


#firstname, lastname, totalprice, depositpaid, bookingdates, checkin, checkout, additionalneeds

class BookerApiTest1(unittest.TestCase):


    def setUp(self):
        self.url = "https://restful-booker.herokuapp.com"
        #self.auth = "ttps://restful-booker.herokuapp.com/auth"

    #how many books in this collection? show bookingId
    def test_get_all(self):
        response = requests.get(self.url+"/booking")
        response_text = response.text
        response_json = json.loads(response.text)
        total_books = len(response_json)
        print(total_books)
        print("all_books")
        print(response_json)

        self.assertEqual(response.status_code, 200)

        self.assertTrue("bookingid" in response_text)


    #bookId includes all info
    def test_get_book_id(self):
        response = requests.get(self.url +"/3")
        response_json = json.loads(response.text)
        print("book_id")
        print(response_json)

        self.assertEqual(response.status_code, 200)


    #show bookId
    def test_get_first_last_name(self):
        response = requests.get(self.url + "?firstname=Jim&lastname=Brown")
        response_json = json.loads(response.text)
        print("first_last_name")
        print(response_json)

        self.assertEqual(response.status_code, 200)

    #show bookId
    def test_checkin_checkout(self):
        response = requests.get(self.url + "?checkin=2019-07-14&checkout=2019-12-26")
        response_json = json.loads(response.text)
        print("checkin_checkout")
        print(response_json)

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        print("-----test is over------")


if __name__ == "__main__":
    unittest.main()

