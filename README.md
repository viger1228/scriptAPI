# ScriptAPI

[![](https://img.shields.io/badge/powered%20by-walker-brightgreen.svg?style=flat-square)](https://github.com/viger1228) 

[English](https://github.com/viger1228/scriptAPI/blob/master/README.md) 

**ScriptAPI** is the easy way transfer your python script into RESTful API.

## Installing
First, you should install python3 and pip3 in your computer.

Clone from the github

    >> git clone git@github.com:viger1228/scriptAPI.git
Install requirement package

    >> cd scriptAPI
    >> pip3 install -r requirement.txt
Create the link for uwsgi3

    >> ln -s /usr/local/lib/python3/bin/uwsgi /usr/local/bin/uwsgi3

## Testing
There are two way to test your script.

Execute the script directly

    >> app/script/demo.py
    [2018-05-20 15:36:16,183][INFO][mod.py(line:35)] - [Req Head] - {}
    [2018-05-20 15:36:16,183][INFO][mod.py(line:67)] - [Rsp Data] - {"data": "Sun May 20 15:36:16 2018", "status": 200, "message": "OK", "rsp_time": "0.00 sec"}

Request the scriptAPI with the URL

execute run.py

    >> ./run.py
     * Running on http://0.0.0.0:9004/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 310-159-269 

curl -i 'http://127.0.0.1:9004/script/demo'

    >> curl -i 'http://127.0.0.1:9004/script/demo'
    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 92
    Access-Control-Allow-Origin: *
    
    {"data": "Sun May 20 15:43:01 2018", "status": 200, "message": "OK", "rsp_time": "0.00 sec"}

## Deployment
Deployment the web server by uwsgi & nginx

Run the uwsgi

    >> ./uwsgi.sh start
    >> netstat -lnpt | grep 9004
    tcp        0      0 0.0.0.0:9004            0.0.0.0:*               LISTEN      2769/uwsgi3

Setting the nginx

    >> vim /etc/nginx/conf.d/scriptAPI.conf
    server {
      listen 80;
      server_name _;
      location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:9004;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
        proxy_connect_timeout 60s;
      }
      access_log /var/log/nginx/scriptAPI_access.log;
      error_log /var/log/nginx/scriptAPI_error.log;
    }   
    >> nginx -s reload

## License

[MIT](https://github.com/viger1228/scriptAPI/blob/master/LICENSE) © Walker