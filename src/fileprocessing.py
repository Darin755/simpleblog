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

            
def newUser(username, password, passwordcheck):
# create a user
    
    #input the name for the user
    userPath = Path.cwd() / 'users' #gets the current working path plus user

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
            return 2
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
            return 0
    else:
        #passwords did not match
        return 1

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


def publish(title, text):
    #check to make sure public exists
    if not (Path.cwd() / 'public').exists():
        (Path.cwd() / 'public').mkdir(exist_ok=False)
    q = Path.cwd() / 'public'
    #move to public
    title = username + '_' + title + '.txt'
    #naming convention of username_title.txt
    q = q / title
    q.touch()
    #create file
    q.write_text(text)
    #write to file

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
