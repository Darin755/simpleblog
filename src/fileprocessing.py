from pathlib import Path
import bcrypt
'''
Pathlib is a python library that allows for proper path navigation throughout files
bcrypt is a python library that allows for encryption of strings 
'''

def login(username, password):
    q = Path.cwd() #gets the current working path
    
    p = q / 'users'
    
    passwordInput = password.encode('utf-8')
    #encrpyts password
    p = p / username
    #moves to the user
    
    #checks if user exists
    test = p.exists()
    if(test == False):
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
              
            
            
def newUser(username, password, passwordcheck):
# create a user
    
    #input the name for the user
    q = Path.cwd() #gets the current working path
  
    p = q / 'users'
    passwordInput = password.encode('utf-8')
    #encrpyts password
    passwordcheck = passwordcheck.encode('utf-8')
    #encrypt the confirmation
    
    # put both passwords through the salt to properly encrpyt
    salt = bcrypt.gensalt(rounds=15)
    hashedPass = bcrypt.hashpw(passwordInput, salt)
    checker = bcrypt.checkpw(passwordcheck, hashedPass) 
    #check the passwords with each other to see if they matchchecker = bcrypt.checkpw(confirmPass, hashedPass)

    if(checker == False):
        return 1
        #passwords did not match
    else:
        #passwords did match
        p = p / username
        
       

        test = p.exists()
        #check to see if username is already being used
        
        if(test == True):
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
            p.mkdir(exist_ok=False)
            return 0


