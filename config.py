# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:33:14 2020

Based on: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

@author: Joel
"""

import os

from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
class Config(object):
    # Secret key, used in WTFFOrms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    
    # Development + Autorelate settings
    #TEMPLATES_AUTO_RELOAD = True
    #TESTING = True
    #ENV = 'development'
    
    # Auth0 Config
    AUTH0_CLIENT_ID=os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_DOMAIN=os.environ.get('AUTH0_DOMAIN')
    AUTH0_CLIENT_SECRET=os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_CALLBACK_URL=os.environ.get('AUTH0_CALLBACK_URL')
    AUTH0_BASE_URL = 'https://' + str(os.environ.get('AUTH0_DOMAIN'))
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')

#app.config['TEMPLATES_AUTO_RELOAD'] = True# Auto reload when change is detected
#app.config['TESTING'] = True
#app.config['ENV'] = 'development'
