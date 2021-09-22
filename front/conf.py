import os

debug = os.environ.get('DEBUG') if os.environ.get('DEBUG') else True
if debug == "False":
    debug = False

host = "0.0.0.0"
port = os.environ.get('FRONT_PORT') if os.environ.get('FRONT_PORT') else 5000

secret_key = os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else "secret"

back_host = os.environ.get('BACK_HOST') if os.environ.get('BACK_HOST') else "localhost"
back_port = os.environ.get('BACK_PORT') if os.environ.get('BACK_PORT') else 5002

if debug: url_back = "http://localhost/api/v1/back"
else: url_back = "http://{0}:8000/back".format(back_host)
