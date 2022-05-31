# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:25:24 2020

@author: Ambition
"""

from flask import Blueprint

bp = Blueprint('oauth', __name__)

from app.oauth import routes
