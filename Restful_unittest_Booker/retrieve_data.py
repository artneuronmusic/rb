import requests
import json

response = requests.get("https://restful-booker.herokuapp.com"+"/booking")
response_json = json.loads(response.text)
total_book_id = len(response_json)

books_list = []
for i in range(total_book_id):
    i+=1

    detail_response = requests.get("https://restful-booker.herokuapp.com"+"/booking"+"/"+"{}".format(i))
    id_input = {"booking_id": str(i)}
    id_json = json.dumps(id_input)
    new_detail = id_json + "," + detail_response.text
    #detail_json = json.loads(detail_response.text)



    books_list.append(new_detail)

books_list_new = str(books_list)
print(books_list_new)


with open("/Users/yuchienhuang/PycharmProjects/python_api_testing/Restful_unittest_Booker/Data/book_list.txt", 'w') as book:
    book.write(books_list_new)
















