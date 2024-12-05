# Route for handling the login page logic
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import os
import fileprocessing
import secrets
import time

print("starting up")

app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap5(app)

# (user, key, time created)
authorized_cookies = []

#check cookie to see if user is logged in
def checkAuth(cookie):
    auth = False
    if (not (cookie == None)):
        #loop though cookies to see if one matches
        for c in authorized_cookies:
            if cookie == c[1]:
                auth = c[0]
                print("authenticated "+auth+" with cookie")
                break
    if auth == False:
        print("cookie invalid")
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
        if not (auth == False):
            print("serving dashboard to "+auth)
            #we are signed in
            isAdmin = fileprocessing.checkAdmin(auth)
            return render_template('dash.html', pages=fileprocessing.displayAllUsers(str(auth), isAdmin), username=auth, showAdminCheck=isAdmin, users=fileprocessing.allUsers(), published=fileprocessing.displayAll())
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
                if(fileprocessing.login(request.form['username'], request.form['password']) == 0):
                    print("authentication successful for "+request.form['username'])
                    authkey = str(secrets.randbits(512))
                    authorized_cookies.append((request.form['username'], authkey, time.time()))
                    resp = redirect("/", code=302)
                    resp.set_cookie('authcookie', authkey)
                    print("set cookie for "+request.form['username'])
                    return resp
                else:
                    errorReturned = 'Invalid Credentials. Please try again.'
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
    resp = redirect("/login", code=302)
    resp.set_cookie('authcookie', "", expires=0)
    return resp


@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    #only allow user creation if no users exist or logged in
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    #no users is true on first run
    noUsers = fileprocessing.noUsers()
    #check if allowed
    if not auth == False or noUsers:
        #check for admin
        isAdmin = fileprocessing.checkAdmin(auth)
        #should we show the admin options
        showAdminCheck = (not noUsers) and (isAdmin)
        if request.method == 'POST':
            #delete checkmark
            if "deletecheck" in request.form:
                #only allow admins
                if isAdmin:
                    #don't delete ourselves'
                    if request.form['username2'] != auth:
                        returnMsg = fileprocessing.deleteUser(request.form['username2'])
                    else:
                        returnMsg = "You can not delete yourself"
                else:
                    returnMsg = "You do not have permition to delete users"
            else:
                if showAdminCheck:
                    if "admincheck" in request.form:
                        returnMsg = fileprocessing.newUser(request.form['username2'], request.form['password2'], request.form['passwordCheck'], True, auth)
                    else:
                        returnMsg = fileprocessing.newUser(request.form['username2'], request.form['password2'], request.form['passwordCheck'], False, auth)
                else:
                    returnMsg = fileprocessing.newUser(request.form['username2'], request.form['password2'], request.form['passwordCheck'], None, auth)

            #returnMsg is the message displayed to the user

            admin = fileprocessing.checkAdmin(auth)
            if noUsers:
                if not fileprocessing.noUsers():
                    return redirect("/login", code=302)
                else:
                    return render_template("newUser.html", error=returnMsg, users=fileprocessing.allUsers(), showAdminCheck=admin)
            else:
                return render_template('dash.html', error=returnMsg, tab="user", pages=fileprocessing.displayAllUsers(str(auth), admin), username=auth, showAdminCheck=admin, users=fileprocessing.allUsers(), published=fileprocessing.displayAll())


        elif request.method == "GET":
            return render_template('newUser.html', showAdminCheck=showAdminCheck, users=fileprocessing.allUsers())
    else:
        return redirect("/login", code=302)

@app.route('/getpage/<page>', methods=['GET'])
def returnPage(page):
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    if not auth == False:
        if (fileprocessing.checkAdmin(auth) or (auth in page)):
            return fileprocessing.getText(page)
        else:
            return "not permitted"
    else:
        return redirect("/login", code=302)

#save page
@app.route('/savepage', methods=['POST'])
def handle_post():
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    if not auth == False:
        body = request.json
        if (fileprocessing.checkAdmin(auth) or (auth in page)):
            fileprocessing.savePage(body["name"], body["body"])
            return "saved"
        else:
            return "not permitted"
    else:
        return redirect("/login", code=302)

#create
@app.route('/createpage', methods=['POST'])
def handle_create():
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    if not auth == False:
        body = request.json
        name = auth+"_"+body["name"]
        fileprocessing.savePage(name, -1)
        return "created"
    else:
        return redirect("/login", code=302)

#delete
@app.route('/deletepage', methods=['POST'])
def handle_delete():
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    if not auth == False:
        if (fileprocessing.checkAdmin(auth) or (auth in page)):
            body = request.json
            fileprocessing.deletePage(body["name"])
            return "deleted"
        else:
            return "not permitted"
    else:
        return redirect("/login", code=302)
#publish
@app.route('/publish', methods=['POST'])
def handle_publish():
    cookie = request.cookies.get('authcookie')
    auth = checkAuth(cookie)
    if not auth == False:
        if (fileprocessing.checkAdmin(auth) or (auth in page)):
            body = request.json
            contents = fileprocessing.getText(body["name"])
            fileprocessing.publish(body["name"], render_template('published.html', contents=contents))
            return "published"
        else:
            return "not permitted"
    else:
        return redirect("/login", code=302)


if __name__ == '__main__':
    app.run()
