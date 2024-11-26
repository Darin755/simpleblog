# Route for handling the login page logic
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import os
import fileprocessing
import secrets
import time

print("starting up")

app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)

# (user, key, time created)
authorized_cookies = []

#check cookie to see if user is logged in
def checkAuth(cookie):
    auth = False
    if (not (cookie == None)) and (len(cookie) == 154):
        #loop though cookies to see if one matches
        for c in authorized_cookies:
            if cookie == c[1]:
                auth = c[0]
                print("authenticated "+auth+" with cookie")
                break
    return auth #return user

print("creating routes")

#root route
@app.route("/")
def root():
    #if no users exist prompt to create one
    if fileprocessing.noUsers():
        return redirect("/newuser", code=302)
    else:
        #check if signed in
        cookie = request.cookies.get('authcookie')
        auth = checkAuth(cookie)
        if not auth == False:
            #we are signed in
            return render_template('dash.html')
        else:
            #login please
            return redirect("/login", code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #if we are logged in go to root
    if checkAuth(request.cookies.get('authcookie')) == False:
        #new user redirect on first run
        if not fileprocessing.noUsers():
            if request.method == 'POST':
                result = fileprocessing.login(request.form['username'], request.form['password'])
                print(result)
                if (result == 1):
                    errorReturned = 'User not found.'
                elif(result == 2):
                    errorReturned = 'Invalid Credentials. Please try again.'
                elif(result == 0):
                    print("authentication successful for "+request.form['username'])
                    authkey = str(secrets.randbits(512))
                    authorized_cookies.append((request.form['username'], authkey, time.time()))
                    resp = redirect("/", code=302)
                    resp.set_cookie('authcookie', authkey)
                    print("set cookie for "+request.form['username'])
                    return resp

                return render_template('login.html', errorReturned=errorReturned)
            else:
                #this is a GET
                return render_template('login.html')
        else:
            return redirect("/newuser", code=302)
    else:
        print("logged in")
        return redirect("/", code=302)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #find cookie and then delete it
    print("logging out")
    cookie = request.cookies.get('authcookie')
    if cookie:
        for i,c in enumerate(authorized_cookies):
            if c[1] == cookie:
                del(authorized_cookies[i])
                print("logged out")
    return redirect("/login", code=302)


@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    #only allow user creation if no users exist
    if fileprocessing.noUsers():
        print("prompting to create new user")
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
    else:
        return redirect("/login", code=302)
    return render_template("newUser.html", error=error)

#save
@app.route('/save', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        cookie = request.cookies.get('authcookie')
        auth = checkAuth(cookie)
        if not auth == False:
            body = request.json
            print(body)
            return "saved"

if __name__ == '__main__':
    app.run()
