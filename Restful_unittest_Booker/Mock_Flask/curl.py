#updated the version in the curl script

import os

tests = """
# get all bookings
curl -i http://127.0.0.1:5000/booking 

# get id 2 and info
curl -i http://127.0.0.1:5000/booking/2


# get id 3 and info
curl -i http://127.0.0.1:5000/booking/3

# error: non-existing id get id 5 and 
curl -i http://127.0.0.1:5000/booking/5


# err: non-existing id and out of range, will not be able to connect
curl -i http://127.0.0.1:5000/booking/999999

      

"""





for line in tests.strip().split('\n'):
    print('\n{}'.format(line))
    if not line.startswith('#'):
        cmd = line.strip()
        os.system(cmd)



"""



 
#create new booking with additional item
curl --header "Content-Type: application/json" --request POST --data'{"firstname": "Tiffany", "lastname": "Lai", "totalprice": 230, "depositpaid": False,"bookingdates": {"checkin": "2018-01-05", "checkout": "2018-01-07"}, "additionalneeds": "extra water bottles"}' http://127.0.0.1:5000/booking
      
            
#create the same booking content
curl -i -H "Content-Type: application/json" -X POST -d '{"firstname": "Chole", "lastname": "Bryson", "totalprice": 230, "depositpaid": False,
            "bookingdates": {"checkin": "2018-01-05","checkout": "2018-01-07"}, 
            "additionalneeds": "extra water bottles"}' http://127.0.0.1:3001/booking
            

#err: create new booking with missing items
curl -i -H "Content-Type: application/json" -X POST -d '{"lastname": "Bryson", "totalprice": 230,
            "bookingdates": { "checkin": "2018-01-05","checkout": "2018-01-07"}, 
            "additionalneeds": "extra water bottles"}}' http://127.0.0.1:3001/booking
            
            
#err: create new booking with missing value
curl -i -H "Content-Type: application/json" -X POST -d '{"firstname": "", "lastname": "Bryson", "totalprice": 230, "depositpaid": None,
            "bookingdates": { "checkin": "","checkout": ""}, 
            "additionalneeds": "extra water bottles"}}' http://127.0.0.1:3001/booking
            

#create auth and token
curl -i -H "Content-Type: application/json" -X POST -d '{"username" : "admin", "password" : "password123"}'  http://127.0.0.1:3001/auth


# update with valid id and valid info
curl -i -H "Content-Type: application/json" -H 'Accept: application/json' \ -H 'Cookie: token=abc123 -X PUT -d  '{
            "firstname": "Judie",
            "lastname": "Duches",
            "totalprice": 500,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-01-05"
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }' http://127.0.0.1:3001/booking/6



# update with valid id and empty info
curl -i -H "Content-Type: application/json" -H 'Accept: application/json' \ -H 'Cookie: token=abc123 -X PUT -d  '{
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
           
        }' http://127.0.0.1:3001/booking/4
        
        
#err: update with invalid id
curl -i -H "Content-Type: application/json" -H 'Accept: application/json' \ -H 'Cookie: token=abc123 -X PUT -d  '{
             
            "firstname": "Williams",
            "lastname": "Dretch",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2019-01-01",
                "checkout": "2019-01-05"
            },
            "additionalneeds": "Room services: water bottles and some snacks"
        }'
            http://127.0.0.1:3001/booking/99


# partial update
curl -i -H "Content-Type: application/json" -H 'Accept: application/json' \ -H 'Cookie: token=abc123 -X PATCH -d  '{
             
            "firstname": "Lisa",
            "lastname": "Morrison"}'    
            http://127.0.0.1:3001/booking/1

#delete existing id
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:3001/booking/5


#delete nonexisting id
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:3001/booking/999

"""
