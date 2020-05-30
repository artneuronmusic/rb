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

id_json = check_data.get_data()

def _get_item(id):
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

# collection = DataResource.get_all()


@app.route('/')
def home_page():
    return 'Project for mocking flask from Restful Booking'

#will return all ids
#@app.route('/booking')
@app.route('/booking', methods=['GET'])
def get_all_id():

    return jsonify(id_json), 200


@app.route('/booking/<int:id>', methods=['GET'])
def get_id_with_info(id):
    item = _get_item(id)

    if not item:
        abort(404)

    else:
        for i in id_json:
            if i["booking id"] == int(id):
                return jsonify(i), 200


# #no limitations for repeated/similar booking
# @app.route('/booking', methods=['POST'])
# def create_new_booking():
#
#
#
#     firstname = request.get_json('firstname')
#     if firstname is None:
#         abort(500)
#     lastname = request.get_json('lastname')
#     if lastname is None:
#         abort(500)
#     totalprice = request.get_json('totalprice')
#     if totalprice is None:
#         abort(500)
#     depositpaid = request.get_json('depositpaid')
#     if depositpaid is None:
#         abort(500)
#     bookingdates = request.get_json({"bookingdates"})
#     if bookingdates is None:
#         abort(500)
#     additionalneeds = request.get_json("additionalneeds")
#     if additionalneeds is None:
#         abort(500)
#
#
#     booking_id = id_json[-1].get("booking id") + 1
#
#     new = {'firstname': firstname, 'lastname': lastname, 'totalprice': totalprice, 'depositpaid': depositpaid,
#            'bookingdates': bookingdates, 'additionalneeds': additionalneeds,
#           'booking id': booking_id}
#     data = id_json.append(new)
#     print(data)
#
#     return jsonify(data), 200
#
#
# # @app.route('/booking/<int:id>', methods=['PUT'])
# # def update_booking(id):
# #     item = _get_item(id)
# #
# #     if len(item) == 0:
# #         abort(404)
# #
# #     if not request.json:
# #         abort(400)
# #
# #
# #     firstname = request.json.get('firstname', item[0]['firstname'])
# #     lastname = request.json.get('lastname', item[0]['lastname'])
# #     totalprice = request.json.get('totalprice', item[0]['totalprice'])
# #     depositpaid = request.json.get('depositpaid', item[0]['depositpaid'])
# #     bookingdates = request.json.get('bookingdates', item[0]['bookingdates'])
# #     additionalneeds = request.json.get('additionalneeds', item[0]['additionalneeds'])
# #
# #     item[0]['firstname'] = firstname
# #     item[0]['lastname'] = lastname
# #     item[0]['totalprice'] = totalprice
# #     item[0]['depositpaid'] = depositpaid
# #     item[0]['bookingdates'] = bookingdates
# #     item[0]['addiotnalneeds'] = additionalneeds
# #
# #
# #     return jsonify(item[0]), 200
# #
# #
# # @app.route('/booking/<int:id>', methods=['DELETE'])
# # def delete_booking(id):
# #     item = _get_item(id)
# #     if len(item) == 0:
# #         abort(404)
# #     id_json.remove(item[0])
# #
# #     return jsonify(item), 201
# #
# #
# #
# #
# #
#
# if __name__ == "__main__":
#     #app.run(host='127.0.0.1', port='3001', debug=True)
#     app.run(debug=True)