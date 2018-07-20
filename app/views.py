#!/usr/bin/env python3
# coding: UTF-8
# file: mod.py
# author: walker

"""
2018-05-19: init

"""

import sys
import imp
import time
import json
import urllib
import logging
import flask
import traceback

from app import app
from lib import tool

logger = tool.Log().file_logger(__name__)

# API
@app.route('/<name>/<script>', methods=['GET','POST','PUT','DELETE','HEAD'])
def _api(name, script):
    reload()
    # Input
    req = flask.request
    args = {'reqH': '', 'reqD': '',}
    args['reqH'] = dict(req.headers)

    # application/json
    args['reqD'] = req.get_json()
    # application/x-www-form-urlencoded
    if not args['reqD']:
        args['reqD'] = {}
        # get
        for key, item in dict(req.args).items():
            args['reqD'][key] = item[0]
        # post
        for key, item in dict(req.form).items():
            args['reqD'][key] = item[0]
    # post json data
    if not args['reqD']:
        try:
            ags['reqD'] = json.loads(req.data)
        except Exception:
            pass
    # multi args
    if not args['reqD']:
        args['reqD'] = dict(urllib.parse.parse_qsl(req.data.decode('utf8')))

    mod = ''
    rspCode = ''
    try:
        attr = __import__('app.%s.%s'%(name,script), fromlist=True)
        imp.reload(attr)
        mod = attr.Mod(args, logger, req.method, req)
        data = mod.run()
        if hasattr(mod, 'rspCode'):
            rspCode = mod.rspCode
    except ImportError:
        error = traceback.format_exc()
        logger.info(error)
        rspCode = 404
        rspDict = {'status': rspCode, 'message': tool.http_msg[rspCode]}
        data = json.dumps(rspDict)
    except Exception:
        error = traceback.format_exc()
        logger.info(error)
        rspCode = 500
        rspDict = {'status': rspCode, 'message': tool.http_msg[rspCode]}
        data = json.dumps(rspDict)

    # Output
    rsp = flask.Response(data)

    # Default Header
    rsp.headers['Content-Type'] = 'application/json; chaset=utf-8'
    rsp.headers['Access-Control-Allow-Origin'] = '*'

    # Custom Header
    if hasattr(mod, 'rspH'):
        for key, value in mod.rspH.items():
            rsp.headers[key] = value
    
    # Respone Code
    if rspCode:
        return rsp, rspCode
    else:
        return rsp

def reload():
    global logger
    imp.reload(tool)
    if len(logger.handlers) > 0:
        handler = logger.handlers[-1]
        if isinstance(handler, logging.FileHandler):
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger = tool.Log().file_logger(__name__)



