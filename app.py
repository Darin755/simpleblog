from flask import Flask
import datetime

app = Flask(__name__)

now = datetime.datetime.now()

@app.route("/")
def hello():
    return "<h1>Hello World! The time is "+str(now.time())+" on the server</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


