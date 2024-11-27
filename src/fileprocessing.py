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
    q = Path.cwd() #gets the current working path
    
    p = q / 'users'
    
    passwordInput = password.encode('utf-8')
    #encrpyts password
    p = p / username
    #moves to the user
    
    #checks if user exists
    if(not p.exists()):
        return 1
        #user does not exist
    else:
        
        #user exists and is checking password
        passfile = p / 'password.txt'
        #opens the password file
        result = bcrypt.checkpw(passwordInput, passfile.read_bytes())
        #checks the password given with the password in the file
        if(result == False):
            return 2
            #invalid password
        else:
            
            #password works
            p = p / 'userData'
            return 0
              
def noUsers():
    return not any(Path(Path.cwd() / "users").iterdir())

            
def newUser(username, password, passwordcheck):
# create a user
    
    #input the name for the user
    q = Path.cwd() #gets the current working path
  
    p = q / 'users'

    print(password,passwordcheck)

    if(password == passwordcheck):
        #passwords did match
        # put both passwords through the salt to properly encrpyt
        passwordInput = password.encode('utf-8')
        passwordcheck = passwordcheck.encode('utf-8')
        salt = bcrypt.gensalt(rounds=15)
        hashedPass = bcrypt.hashpw(passwordInput, salt)

        #set path
        p = p / username
       
        #check to see if username is already being used
        if(p.exists()):
            return 2
            #user is already in use
        else:
            #create a user with filename = to input
            p.mkdir(exist_ok=False)
            #create a password file
            passfile = p / 'password.txt'
            passfile.touch()
            #put hashed password into file
            
            passfile.write_bytes(hashedPass)
            p = p / 'userData'
            print(p)
            p.mkdir(exist_ok=False)
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
        

