import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = 'TEST'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FOOD_RECOGNITION_KEY = "9e549542cb924460bcea95b91f7c614c138a7071"
    MIGROS_USERNAME = "hackzurich2020"
    MIGROS_PASSWORD = "uhSyJ08KexKn4ZFS"
    MIGROS_AUTH = HTTPBasicAuth(MIGROS_USERNAME, MIGROS_PASSWORD)
    LOW_CARB_THR = 30
