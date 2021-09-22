import os

debug = os.environ.get('DEBUG') if os.environ.get('DEBUG') else True
if debug == "False":
    debug = False

host = "0.0.0.0"
port = os.environ.get('AUTH_PORT') if os.environ.get('AUTH_PORT') else 5002

secret_key = os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else "secret"
