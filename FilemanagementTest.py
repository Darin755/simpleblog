from pathlib import Path
import bcrypt
'''
Pathlib is a python library that allows for proper path navigation throughout files
bcrypt is a python library that allows for encryption of strings 
'''

q = Path.cwd() #gets the current working path
print(q)
p = q / 'users'
print(p)

#gets signin or create account for user
mode = str(input("sign in (S) or create account (C)"))

#if mode is signin
if(mode == 's' or mode == 'S'):

    #gets the username, which is tied to a filename
    filecreate =  str(input("input file "))
    #gets the password to encrypt
    passwordInput = str(input("input a password "))
    
    passwordInput = passwordInput.encode('utf-8')
#	#encrpyts password
    p = p / filecreate
    #moves to the user
    print(p)
    #checks if user exists
    test = p.exists()
    if(test == False):
        print("username not found")
        #user does not exist
    else:
        print("file already exists, checking password")
        #user exists and is checking password
        passfile = p / 'password.txt'
        #opens the password file
        result = bcrypt.checkpw(passwordInput, passfile.read_bytes())
        #checks the password given with the password in the file
        if(result == False):
            print("passwords do not match!!")
            #invalid password
        else:
            print("hello", filecreate)
            #password works
            p = p / 'userData'
            obj = p.iterdir()
            for item in obj:
                print(f"File:...... {item.name}")
                #prints all items in the directory
            
            

# create a user
elif(mode == 'C' or mode == 'c'):
    #input the name for the user
    filecreate =  str(input("input file "))
    #input the password
    passwordInput = str(input("input a password "))
    #encypt the password
    passwordInput = passwordInput.encode('utf-8')
    #input a conformation
    confirmPass =  str(input("confirm Password "))
    #encrypt the confirmation
    confirmPass = confirmPass.encode('utf-8')
    # put both passwords through the salt to properly encrpyt
    salt = bcrypt.gensalt(rounds=15)
    hashedPass = bcrypt.hashpw(passwordInput, salt)
    hashConfirm = bcrypt.hashpw(confirmPass, salt)
    #check the passwords with each other to see if they match
    checker = bcrypt.checkpw(confirmPass, hashedPass)
   
    if(checker == False):
        print("passwords must match")
        #passwords did not match
    else:
        #passwords did match
        p = p / filecreate
        
        print(p)

        test = p.exists()
        #check to see if username is already being used
        
        if(test == True):
            print("username in use")
            #user is already in use
        else:
            #create a user with filename = to input
            p.mkdir(exist_ok=False)
            #create a password file
            passfile = p / 'password.txt'
            passfile.touch()
            #put hashed password into file
            print(hashedPass)
            passfile.write_bytes(hashedPass)
            p = p / 'userData'
            p.mkdir(exist_ok=False)
    
#for incorrect inputs
else:
    print("please only enter a S or a C")
    