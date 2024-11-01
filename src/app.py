
from flask import Flask, render_template, request
import os

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def hello_world():
    return render_template("demo.html")

@app.route('/save', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        body = request.json
        print(body)
        return "saved"

if __name__ == '__main__':
    app.run()
