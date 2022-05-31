# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:14:14 2020

@author: Joel
"""


from app import create_app


# Create application. Elasticbeanstalk looks for a callable application object: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
application = create_app()


# Run the application
if __name__ == "__main__":
    application.run(host= '0.0.0.0')
