from pathlib import Path
import bcrypt
from datetime import datetime
'''
Pathlib is a python library that allows for proper path navigation throughout files
bcrypt is a python library that allows for encryption of strings 
'''
#create needed dirs on startup

if not (Path.cwd() / 'users').exists():
    (Path.cwd() / 'users').mkdir(exist_ok=False)

if not (Path.cwd() / 'public').exists():
    (Path.cwd() / 'public').mkdir(exist_ok=False)


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
    #input the name for the user
    userPath = Path.cwd() / 'users' #gets the current working path plus user

    #check if user is authorized
    if admincheck != None:
        if auth == username:
            if not admincheck:
                print(auth+" can not strip there own admin access")
                return "You can not strip your own admin access"
        else:
            if not checkAdmin(auth):
                print("Non admin user "+auth+" tried to change user "+username)
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
            return "Updated user "+username
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

            #create default page
            savePage(username+"_index", username+"'s page")

            #if admin
            if admincheck or auth == False:
                makeAdmin(username)
            return "Created user "+username
    else:
        #passwords did not match
        return "Password need to match"

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
        return "deleted user "+user
    else:
        return user+" does not exist thus it can't be deleted"

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
            print(user+" is a admin")
            return True
        else:
            print(user+"is not an admin")
            return False


def displayAll():
    returnList = []
    files = [f for f in (Path.cwd()  / 'public').iterdir() if (not f.is_dir()) and (f.name.endswith(".html"))]
    for file in files:
        returnList.append(file.name)
    return returnList

def displayAllUsersHelper(username):
    returnArray = []
    files = (Path.cwd()  / 'users' / username / 'userData').iterdir()
    for filename in files:
        try:
            tupleToAdd = ()
            nameArray = filename.name.split("_")
            #[0] is username
            tupleToAdd += (nameArray[0],)
            #[1] is title
            tupleToAdd += (nameArray[1].split(".")[0],)
            #[2] is last modification
            editTime = (Path.cwd()  / 'users' / username / 'userData' / filename).stat().st_mtime
            tupleToAdd += (datetime.fromtimestamp(editTime).ctime(),)
            #published information
            if((Path.cwd() / 'public' / filename.name).exists()):
                tupleToAdd += (filename.name,)
                editTimePublished = (Path.cwd() / 'public' / filename.name).stat().st_mtime
                tupleToAdd += (datetime.fromtimestamp(editTimePublished).ctime(),)
            else:
                tupleToAdd += ("Not Published",)
                tupleToAdd += ("N/A",)
            returnArray.append(tupleToAdd)
        except Exception as e:
            print(e)
            print("failed to parse "+str(filename))
    return returnArray

def displayAllUsers(username, admin):
    print("fetching page list for "+username+"'s dashboard")
    returnList = []
    try:
        if not admin:
            returnList = displayAllUsersHelper(username)
        else:
            for user in [f for f in (Path.cwd()  / 'users').iterdir() if f.is_dir()]:
                returnList += displayAllUsersHelper(user)
    except Exception as e:
        print("failed to get pages")
        print(e)



    #returns a list of users
    return returnList

def publish(title, text):
    username = title.split("_")[0]
    #saves using username_title as convention
    textfile = Path.cwd()  / 'public' /  (title+".html")
    #create file
    textfile.touch()
    #write to file
    textfile.write_text(text)
    print("published page "+title)
  
def savePage(title, text):
    username = title.split("_")[0]
    #saves using username_title as convention
    textfile = Path.cwd()  / 'users' /  username / 'userData' / (title+".html")
    #create file
    textfile.touch()
    #write to file
    if text != -1:
        textfile.write_text(text)
    print("saved changes to "+title)

def getText(fileToGet):
    print("serving page "+fileToGet)
    fileToGet+=".html"
    filePath = (Path.cwd()  / 'users' / fileToGet.split("_")[0] / 'userData' / fileToGet)
    if filePath.exists():
        return (Path.cwd()  / 'users' / fileToGet.split("_")[0] / 'userData' / fileToGet).read_text()
    else:
        return "not found"

def deletePage(name):
    filePath = (Path.cwd()  / 'users' / name.split("_")[0] / 'userData' / (name+".html"))
    if (len(name) > 0) and filePath.exists():
        filePath.unlink()
    else:
        print(name+" not deleted because it doesn't exist")
    print("deleted page "+name)

def allUsers():
    rtnStr= ""
    for user in [f for f in (Path.cwd()  / 'users').iterdir() if f.is_dir()]:
        rtnStr+=user.name+" "
    return rtnStr
