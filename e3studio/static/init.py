import os
from pathlib import Path


class Env():
    # DEBUG = True
    DEBUG = False
    SECRET_KEY = '^k1p+y*k-3mvqa(k5+2#v9fe+u(_dx4rj^^f^b-u(&&+(-u5_m'
    BASE_DIR = Path(__file__).resolve().parent.parent
    URLJS = open(os.path.join(BASE_DIR, "src/url/MainUrl.js"),
                 "r").readlines()[:2]
    if URLJS[0][:2] != '//':  # // const MainUrl = 'http://www.e3studio.ca';
        DJANGO_ALLOWED_HOSTS = ['192.168.0.18', '127.0.0.1', 'localhost']
        DJANGO_CURRENT_HOST = 'localhost:8000'
        DJANGO_WHITELIST = ['http://localhost:8000', 'http://localhost:3000']

    if URLJS[1][:2] != '//':  # // const MainUrl = 'http://localhost:8000';
        DJANGO_ALLOWED_HOSTS = ['e3studio.herokuapp.com', 'www.e3studio.ca']
        DJANGO_CURRENT_HOST = 'www.e3studio.ca'
        DJANGO_WHITELIST = ['http://www.e3studio.ca',
                            'https://e3studio.herokuapp.com']

    # DJANGO_INDEX_HTML = 'index.html'
    # MAILGUN_API = '87a521ce1c66bb38e9d3a058ef1d8301-9b1bf5d3-32b24d94'
    # MAILGUN_DOMAIN = 'sandbox61fdce686c084c348f973b9e5817083d.mailgun.org'
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_USER = 'postmaster@sandbox61fdce686c084c348f973b9e5817083d.mailgun.org'
    EMAIL_PASSWORD = '6b4b13ecd8a27af7805f063be41efffe-9b1bf5d3-ea26e9f8'

    CLD_NAME = 'hckhaid02'
    CLD_API_KEY = '612344637657376'
    CLD_API_SECRET = 'vj_3DBK7d4qS3j8mqRSUkKz_1MQ'
