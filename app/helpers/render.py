# Author: Alex Ksikes 

import web

from app.models import functions

from config import view

import random

def layout(page, **kwargs):
    popular= []
    _random = functions.getRandom()
    by = 'Gonzalo Cobos'
    return view.layout(page, popular, _random, by, **kwargs)