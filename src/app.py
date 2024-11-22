# Route for handling the login page logic
from flask import Flask, render_template, redirect, url_for, request
import os
import fileprocessing
import secrets
import time

app = Flask(__name__, static_url_path='/static')

# (user, key, time created)
authorized_cookies = []

@app.route("/")
def root():
    cookie = request.cookies.get('authcookie')
    auth = False
    if (not (cookie == None)) and (len(cookie) == 154):
        for c in authorized_cookies:
            if cookie == c[1]:
                auth = True
                break
    if auth:
        return render_template('demo.html')
    else:
        return redirect("/login", code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = fileprocessing.login(request.form['username'], request.form['password'])
        print(result)
        if (result == 1):
            errorReturned = 'User not found.'
        elif(result == 2):
            errorReturned = 'Invalid Credentials. Please try again.'
        elif(result == 0):
            authkey = str(secrets.randbits(512))
            authorized_cookies.append((request.form['username'], authkey, time.time()))
            resp = redirect("/", code=302)
            resp.set_cookie('authcookie', authkey)
            return resp

        return render_template('login.html', errorReturned=errorReturned)
    else:
        return render_template('login.html')



@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        result = fileprocessing.newUser(request.form['username2'], request.form['password2'], request.form['passwordCheck'])
        if (result == 1):
            error = 'Passwords must match!'
        elif(result == 2):
            error = 'Username already in use!'
        elif(result == 0):
            return redirect("/login", code=302)
    elif request.method == "GET":
        return render_template('newUser.html')

        
    return render_template("newUser.html", error=error)
    
@app.route('/save', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        body = request.json
        print(body)
        return "saved"

if __name__ == '__main__':
    app.run()
