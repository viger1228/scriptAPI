#!/usr/bin/env python3
# coding: UTF-8

import os
import sys
import json
import logging
import traceback
import time
from datetime import datetime

sys.path.append('app')
sys.path.append(os.path.dirname(sys.path[0]))

from lib import tool
from lib import mod

class Mod(mod.REST):

    def __init__(self, *args, **kwargs):

        # Print request head & data
        kwargs['print_reqH'] = True
        kwargs['print_reqD'] = True
        mod.REST.__init__(self, *args, **kwargs)

        # Print response data
        self.print_rspD = True
 
        # is file?
        self.isfile = False
        #self.rspH = {'Content-Type': 'text/html; charset=utf-8'}      

        # self.reqH
        # self.reqD
        # self.logger
        # self.rspCode
        # self.rspD

    def get(self):
        args = tool.Args(self.reqD)
        try:
            args.parse('msg', datetime.now().strftime('%c'))
        except Exception:
            error = traceback.format_exc()
            self.logger.error(error)
            self.rspD['error'] = 'The parameter missing'
            self.rspCode = 400
            return

        msg = args['msg']
        self.rspCode = 200
        self.rspD['data'] = msg

    def post(self):
        self.rspCode = 405

    def put(self):
        self.rspCode = 405

    def delete(self):
        self.rspCode = 405

    def close(self):
        pass

if __name__ == '__main__':

    os.chdir(sys.path[0])
    logger = tool.Log().stream_logger('info')

    args = { 'reqH': {}, 'reqD': {},}

    mod = Mod(args, logger, 'GET')
    mod.run()

