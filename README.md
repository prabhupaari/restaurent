# restaurent
Restaurent revenue system

Steps to setup

1. Clone this repo
2. create venv `python3 -m venv venv`
3. Activate Env `source venv/bin/activate`
4. install requirements `pip install -r requirements.txt`
5. Added existing sqlite file. Otherwise run migrations `cd server;python3 manage.py migrate`
6. added postman collection to test API. collection name `restaurent_api_collection.json`
