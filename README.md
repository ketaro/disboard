
Installation
------------

Create a virtual environment to run in:

  virtualenv env

Configure the virtual environment:

  Edit: env/bin/activate
  Add config variables at the bottom of the script:
  
    # Database (use mysql)
    export DATABASE_URI="mysql+mysqldb://user:password@localhost/aamgame_dev?charset=utf8"
    export TEST_DATABASE_URI="mysql+mysqldb://user:password@localhost/aamgame_test?charset=utf8"

    export PASSWORD_SALT='randomsalttext'

Activate the virtualenv:

  source env/bin/activate

  
Install python dependancies:

  pip install -r requirements.txt


Create Database Schema:

  python app.py db upgrade  



Database Updates
----------------

To create a new revision:

  python app.py db revision -m "Version Message" --autogenerate
  
To update the schema:
  
  python app.py db upgrade



 
Start Web Application (Developer Mode)
--------------------------------------

  source env/bin/activate
  python web.py




Server Installation Instructions
--------------------------------

Ubuntu

apt-get install libxml2-dev libxslt1-dev python-dev
apt-get install nginx mysql-server libmysqlclient-dev git python-virtualenv python-pip
apt-get install uwsgi uwsgi-plugin-python uwsgi-plugin-syslog

    ** make sure the development packages of libxml2 and libxslt are installed **


mkdir -p /var/vweb/aamgame.mydomain.com
cd /var/vweb/aamgame.mydomain.com
mkdir logs photos

chown -R uwsgi:uwsgi photos 
chown -R nginx logs


git clone ssh://git@cocoon.axcella.net:2202/aamgame flask


nginx Setup
-----------

server {
    listen       80;
    server_name  aamgame.mydomain.com;

    #charset koi8-r;
    access_log  /var/vweb/aamgame.mydomain.com/logs/access.log;
    error_log   /var/vweb/aamgame.mydomain.com/logs/error.log  warn;

    index  index.html index.htm;
    root /var/vweb/aamgame.mydomain.com/flask/app/static;

    # Deny access to all "dot" files (.htaccess, .svn, etc.)
    location ~ /\. { deny all; access_log off; log_not_found off; }

    location /static {
        alias /var/vweb/aamgame.mydomain.com/flask/app/static;
    }
    location /portal/assets {
        alias /var/vweb/aamgame.mydomain.com/flask/app/static;
    }

    # Route to Flask if required
    location / {
        include uwsgi_params;
        uwsgi_pass  unix:///var/run/uwsgi/uwsgi-aamgame.sock;
        #uwsgi_param SCRIPT_NAME /;
    }

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # Handles requests photos
    location ~ ^/static/photos/(.*)$ {
        root /var/vweb/aamgame.mydomain.com/photos;
    }

}


uwsgi Setup
-----------

Edit /etc/uwsgi/apps-available/aamgame.ini (and symlink to apps-enabled)

[uwsgi]
workers = 4
buffer-size = 8096
#daemonize = true
enable-threads = true
chdir = /var/vweb/aamgame.mydomain.com/flask
virtualenv = /var/vweb/aamgame.mydomain.com/flask/env
module = web 
callable = app
plugins = python

env = DATABASE_URI=mysql+mysqldb://dbuser:dbpasswd@localhost:3306/dbname?charset=utf8
env = PASSWORD_SALT=XXXXXXXXX
env = PHOTO_PATH=/var/vweb/aamgame.mydomain.com/photos




MySQL Setup
-----------

CREATE DATABASE aamgame;
CREATE DATABASE aamgame_test;

