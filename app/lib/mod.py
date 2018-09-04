#!/usr/bin/env python3
# coding: UTF-8
# file: mod.py
# author: walker

"""
2018-05-19: init

"""

import os
import sys
import time
import json
import traceback
from datetime import datetime

import tool

class REST(object):

    def __init__(self, args, logger, method, req='', print_reqH=True, print_reqD=True):
        self.logger = logger
        self.reqH = args['reqH']
        self.reqD = args['reqD']
        self.method = method

        self.print_rspD = True
        
        # Print Request Info
        if req:
            self.req = req
            self.logger.info('%s %s %s'%(req.remote_addr, req.method, req.url))
        if print_reqH:
            self.logger.info('[Req Head] - ' + json.dumps(args['reqH']))
        if print_reqD and self.reqD:
            self.logger.info('[Req Body] - ' + json.dumps(args['reqD']))

        # Define Response Header
        self.rspH = {
            #'Content-Type': 'text/html; charset=utf-8',
            'Content-Type': 'application/json; charset=utf-8'
        }

        self.rspCode = 200
        self.rspD = {}

    def run(self):
        sTime = time.time()
        try:
            func = getattr(self, self.method.lower())
            func()
        except Exception:
            error = traceback.format_exc()
            self.logger.info(error)
            self.rspCode = 500
        eTime = time.time()

        msg = str(self.rspD)
        if isinstance(self.rspD, dict):
            self.rspD['status'] = self.rspCode
            self.rspD['message'] = tool.http_msg[int(self.rspCode)]
            self.rspD['rsp_time'] = '%0.2f sec'%(eTime-sTime)
            msg = json.dumps(self.rspD)
        self.close()
        if self.print_rspD:
            self.logger.info('[Rsp Data] - ' + msg)
        return msg

    def get(self):
        msg = datetime.now().strftime('%c')
        self.rspD['data'] = msg

    def post(self):
        self.rspCode = 405

    def put(self):
        self.rspCode = 405

    def delete(self):
        self.rspCode = 405

    def head(self):
        self.rspCode = 200

    def close(self):
        pass

