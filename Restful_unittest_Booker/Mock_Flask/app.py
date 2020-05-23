from flask import Flask, jsonify, abort, make_response, request
import json
import jsonpath
import check_data
from flask import request
from flask import jsonify

import time


app = Flask(__name__)

NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'
INTERNAL_FAIL = "Internal failure"


def _get_item(id):
    id_json = check_data.get_data()
    #with open('/Users/yuchienhuang/PycharmProjects/python_api_testing/Restful_unittest_Booker/Mock_Flask/Data/book_list.json','r') as f:
     #   id_json = json.load(f)
    #id_json = check_data.get_data()
    for i in id_json:
        if i["booking id"] == id:
            return i


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.errorhandler(500)
def bad_request(error):
    return make_response(jsonify({'error': INTERNAL_FAIL}), 500)


@app.route('/')
def home_page():
    return 'Project for mocking flask from Restful Booking'

#will return all ids
#@app.route('/booking')
@app.route('/booking', methods=['GET'])
def get_all_id():
    id_json = check_data.get_data()

    return jsonify(id_json), 200


@app.route('/booking/<int:id>', methods=['GET'])
def get_id_with_info(id):
    id_json = check_data.get_data()
    item = _get_item(id) #get info for this item

    if not item:
        print("The id is not existing")
        abort(404)

    else:
        for i in id_json:
            if i["booking id"] == int(id):
                return jsonify(i), 200


#no limitations for repeated/similar booking
@app.route('/booking', methods=['POST'])
def create_new_booking():

    data = request.get_json()
    print(data)
    if not "firstname" in data:
        abort(404)
    if not "lastname" in data:
        abort(404)
    if not "totalprice" in data:
        abort(404)
    if not "depositpaid" in data:
        abort(404)
    if not "bookingdates" in data:
        abort(404)
    if not "additionalneeds" in data:
        abort(404)

    id_json = check_data.get_data()
    booking_id = id_json[-1]["booking id"] + 1

    data.update({'booking id': booking_id})

    print("my final data")
    # print(type(data))
    check_data.create_data(data)
    id_json = check_data.get_data()

    return jsonify(id_json[-1]), 200


#how to deal with the cookie thing
@app.route('/booking/<int:id>', methods=['PUT'])
def update_booking(id):
    id_json = check_data.get_data()

    data = request.get_json()
    #print(data['firstname'])

    for i in id_json:
        if i["booking id"] == id:
            i['firstname'] = data['firstname']
            i['lastname'] = data['lastname']
            i['totalprice'] = data['totalprice']
            i['depositpaid'] = data['depositpaid']
            i['bookingdates'] = data['bookingdates']
            i['addiotnalneeds'] = data['additionalneeds']
            i['booking id'] = data['booking id']


    check_data.update_data(id_json)
    update_info = _get_item(id)

    return jsonify(update_info), 200


@app.route('/booking/<int:id>', methods=['DELETE'])
def delete_booking(id):
    id_json = check_data.get_data()
    for i in id_json:
         if i["booking id"] == id:
            id_json.remove(i)

    check_data.update_data(id_json)

    return jsonify(id_json), 201


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port='3001', debug=True)
    app.run(debug=True)