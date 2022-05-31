# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:16:40 2020

@author: Joel
"""


from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers #our handlers function
