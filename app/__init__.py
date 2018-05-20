#!/usr/bin/env python3
# coding: UTF-8
# file: __init__.py
# author: walker

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import flask
app = flask.Flask(__name__)

from app import views
