# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:25:24 2020

@author: Joel
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
