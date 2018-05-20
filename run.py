#!/usr/bin/env python3
# coding: UTF-8

from app import app
from app import views
from app.lib import tool

if __name__ == '__main__':
    
    for handler in views.logger.handlers:
        views.logger.removeHandler(handler)
    #views.logger = tool.Log().print_logger()
    views.logger = tool.Log().stream_logger()

    app.run(host='0.0.0.0', port=9004, debug=True, threaded=True)
