from pathlib import Path
import bcrypt
'''
Pathlib is a python library that allows for proper path navigation throughout files
bcrypt is a python library that allows for encryption of strings 
'''
#create needed dirs on startup

if not (Path.cwd() / 'users').exists():
    (Path.cwd() / 'users').mkdir(exist_ok=False)


def login(username, password):
    userPath = Path.cwd() / 'users' #gets the current working path plus users
    passwordInput = password.encode('utf-8') #get password
    #checks if user exists
    if(username != "" and (userPath / username).exists()):
        usernamePath = userPath / username
        #user exists and is checking password
        passfile = usernamePath / 'password.txt'
        #opens the password file
        #checks the password given with the password in the file
        if(bcrypt.checkpw(passwordInput, passfile.read_bytes())):
            #correct password
            return 0
        else:
            #login failed
            return 1
    else:
        #login failed
        return 1



#if no users exist return true
def noUsers():
    return not any(Path(Path.cwd() / "users").iterdir())

            
def newUser(username, password, passwordcheck, admincheck, auth):
# create a user
    print("check is"+str(admincheck))
    #input the name for the user
    userPath = Path.cwd() / 'users' #gets the current working path plus user

    #check if user is authorized
    if admincheck != None:
        if auth == username:
            if not admincheck:
                return "You can not strip your own admin access"
        else:
            if not checkAdmin(auth):
                return "You do not have permission"

    if(password == passwordcheck):
        #passwords did match
        # put both passwords through the salt to properly encrpyt
        passwordInput = password.encode('utf-8')
        passwordcheck = passwordcheck.encode('utf-8')
        salt = bcrypt.gensalt(rounds=15)
        hashedPass = bcrypt.hashpw(passwordInput, salt)

        #username path
        usernamePath = userPath / username

        #check to see if username is already being used
        if(usernamePath.exists()):
            #create password file if it doesn't exist'
            passfile = usernamePath / 'password.txt'
            passfile.touch()
            passfile.write_bytes(hashedPass)
            #create userData
            if not (usernamePath / 'userData').exists():
                (usernamePath / 'userData').mkdir()
            #add to admin if needed
            if admincheck == True:
                makeAdmin(username)
            elif admincheck == False:
                removeAdmin(username)
            return "Updated user"
            #user is already in use but password updated
        else:
            #create a user with filename = to input
            usernamePath.mkdir(exist_ok=False)
            #create a password file
            passfile = usernamePath / 'password.txt'
            passfile.touch()
            #put hashed password into file
            passfile.write_bytes(hashedPass)
            (usernamePath / 'userData').mkdir()

            #if admin
            if admincheck or auth == False:
                makeAdmin(username)
            return "Created user"
    else:
        #passwords did not match
        return 1

#recursive function to delete
def rmDir(dirpath):
    if dirpath.is_file():
        dirpath.unlink()
    else:
        for child in dirpath.iterdir():
            rmDir(child)
        dirpath.rmdir()


#delete a user
def deleteUser(user):
    usernamePath = Path.cwd() / 'users' / user
    if usernamePath.exists():
        rmDir(usernamePath)
        return "deleted user"
    else:
        return "user does not exist"

#make a user admin
def makeAdmin(user):
    print("making "+user+" admin")
    usernamePath = Path.cwd() / 'users' / user
    (usernamePath / "admin.txt").touch()

#remove admin
def removeAdmin(user):
    print("stripping "+user+" of admin")
    usernamePath = Path.cwd() / 'users' / user
    if (usernamePath / "admin.txt").exists():
        (usernamePath / "admin.txt").unlink()


#check if admin
def checkAdmin(user):
    if user != False:
        usernamePath = Path.cwd() / 'users' / user
        if (usernamePath / "admin.txt").exists():
            return True
        else:
            return False


def displayAll():
    returnList = []
    if not (Path.cwd() / 'public').exists():
        (Path.cwd() / 'public').mkdir(exist_ok=False)
    for i in (Path.cwd() / 'public'):
        returnList += i
    #returns a list of public post names
    return returnList

def displayAllUsers(username):
    returnList = []
    for i in (Path.cwd() / 'users' / username):
        returnList += i
    #returns a list of users
    return returnList


def saved(title, text, username):
    q = Path.cwd()

    p = q  / 'users' / username
    #gets proper directory

    #saves using username_title as convention
    title = username + '_' + title + '.txt'
    textfile = p / title
    #create file
    textfile.touch()
    #write to file
    textfile.write_text(text)

def getText(mode, fileToGet):
    q = Path.cwd()
    #if method was from user profile
    if(mode == 1):
        p = q  / 'users' / username / fileToGet
    else:
        #if method was from public
        p = q  / 'public' / fileToGet
    return p.read_text

def writePage(url,html):
    #The html var is the output from render_template
    return True#just a place holder
