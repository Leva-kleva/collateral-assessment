import json
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.exceptions import abort
import conf

app = Flask(__name__)
app.config['SECRET_KEY'] = conf.secret_key


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template("request/request.html")


if __name__ == '__main__':
    app.run(debug=conf.debug, port=conf.port, host=conf.host)
