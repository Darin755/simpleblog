# Route for handling the login page logic
from flask import Flask, render_template, redirect, url_for, request
import os
import fileprocessing


app = Flask(__name__, static_url_path='/static')

@app.route("/")

def hello_world():
    return render_template("login.html")




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = FilemanagementTest.login(request.form['username'], request.form['password'])
        print(result)
        if (result == 1):
            error = 'User not found.'
        elif(result == 2):
            error = 'Invalid Credentials. Please try again.'
        elif(result == 0):
            return render_template("demo.html")
    return render_template('login.html', error=error)
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        return render_template("newUser.html")
    
@app.route('/makeUser', methods=['GET', 'POST'])
def makeUser():
    if request.method == 'POST':
        result = FilemanagementTest.newUser(request.form['username2'], request.form['password2'], request.form['passwordCheck'])
        print(result)
        if (result == 1):
            error = 'Passwords must match!'
        elif(result == 2):
            error = 'Username already in use!'
        elif(result == 0):
            return render_template("demo.html")
        
    return render_template("newUser.html", error=error)
    
@app.route('/save', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        body = request.json
        print(body)
        return "saved"

if __name__ == '__main__':
    app.run()
