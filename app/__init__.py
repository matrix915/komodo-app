# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:29:27 2020

Based on: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

@author: Joel
"""

# Get Modules
from flask import Flask
#import os

from config import Config
from authlib.integrations.flask_client import OAuth

# Create instance of extensions: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
## none at the moment
auth0 = None

# Create application instance
def create_app(config_class=Config):
    global auth0
    
    application = Flask(__name__) 
    
    # Load Config settings
    application.config.from_object(Config)

    # Attached extension instance to applciation: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure    ## none at the moment

    ###
    # Register Configure Auth0
    ###
    oauth = OAuth(application)    
    # auth0 = oauth.register(
    #         'auth0',
    #         client_id='9ccbfMd8ADHJF5gj4AhAnz4DREPgP2ZQ',
    #         client_secret='WBUWdHO262zH0sUgEtXyXGL2ERTMeksTPMSHriGwOF_TrdCIpTF2-pwTUrV1fIge',
    #         api_base_url='https://dev-jaxdqe55.us.auth0.com',
    #         access_token_url='https://dev-jaxdqe55.us.auth0.com/oauth/token',
    #         authorize_url='https://dev-jaxdqe55.us.auth0.com/authorize',
    #         client_kwargs={
    #             'scope': 'openid profile email',
    #         },
    #     )
    auth0 = oauth.register(
            'auth0',
            client_id=application.config['AUTH0_CLIENT_ID'],
            client_secret=application.config['AUTH0_CLIENT_SECRET'],
            api_base_url=application.config['AUTH0_BASE_URL'],
            access_token_url=application.config['AUTH0_BASE_URL'] + '/oauth/token',
            authorize_url=application.config['AUTH0_BASE_URL'] + '/authorize',
    
            client_kwargs={
                'scope': 'openid profile email',
            },
        )
    # Register Blueprints
    ###
    # Error blueprint
    from app.errors import bp as errors_bp
    application.register_blueprint(errors_bp)
    
    # Main blueprint
    from app.main import bp as main_bp
    application.register_blueprint(main_bp)

    # Auth blueprint

    from app.oauth import bp as auth_bp
    application.register_blueprint(auth_bp)

    return application

# Import routes at the end
#from app import routes