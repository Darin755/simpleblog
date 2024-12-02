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


