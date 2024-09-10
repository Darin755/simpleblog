from flask import flask
app = Flask(__name__)

@app.route('/')
def hello_geek:
    return "<h1>Hello World!</h1>"
