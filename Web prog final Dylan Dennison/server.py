from bottle import route, get, post 
from bottle import run, debug
from bottle import request, response, redirect, template, default_app
from bottle import static_file
import dataset
import json
import random
import string
import hashlib
import os
import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#main page
@route("/")
def getChart():
    sess = getSession(request) # getting session from browser
    username = sess['username'] # getting username from session info
    chart_db = dataset.connect('sqlite:///chart.db') #connecting to data base
    chart = chart_db.get_table('chart') #get the table
    itemsInDatabase = chart.find() 
    itemsInDatabase = [ dict(x) for x in list(itemsInDatabase) if x['username'] == username ] #getting data from data base depending on the user
    temp = template("chart", itemsInDatabase=itemsInDatabase, message="Hello " + username, status=None) # template
    saveSession(response, sess) #saving session
    return temp #returning template






#-----------------chart functions for main page-----------------

#insert on chart
@get("/insert")
def getInsert():
    global message #message for the alert
    message = "A new feeding was added to the chart"
    return template("insert") #returns the insert page

@post("/insert")
def postInsert():
    #getting user input from form
    time = request.forms.get('time')
    length = request.forms.get('length')
    side = request.forms.get('side')
    poops = request.forms.get('poops')
    pees = request.forms.get('pees')

    s = getSession(request) #get session
    username = s['username'] # have to get user name from session to put into database
    try:
        #inputting data into database
        chart_db = dataset.connect('sqlite:///chart.db')
        chart = chart_db.get_table('chart')
        chart.insert({
            'username' : username,
            'time' : time.strip(),
            'length' : length.strip(),
            'side' : side.strip(),
            'poops' : poops.strip(),
            'pees' : pees.strip() 
        })
        #exception needed for bad request
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return redirect('/') #return to main 


#delete from chart
@route("/delete/<id>")
def getDelete(id):
    id = int(id) #getting chart id
    try:
        #deleting from database
        chart_db = dataset.connect('sqlite:///chart.db')
        chart = chart_db.get_table('chart')
        chart.delete(id=id)
        #exception for protection
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return template("deleted", id=id)#returns deleted template


#edit chart
@get("/edit/<id>")
def getEdit(id):
    try:
        #connect to database
        chart_db = dataset.connect('sqlite:///chart.db')
        chart = chart_db.get_table('chart')
        items = list(chart.find(id=id))
        if len(items) != 1: #if nothing was change output and error
            response.status="404 Not Found:"+str(id)
            return
        items = [ dict(x) for x in items ] #get items from data
        #throw exception for protection
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return template("edit", item=items[0])  #return edit template

@post("/edit")
def postEdit():
    #get data from form
    id = request.forms.get('id')
    id = int(id)
    time = request.forms.get('time')
    length = request.forms.get('length')
    side = request.forms.get('side')
    poops = request.forms.get('poops')
    pees = request.forms.get('pees')
    s = getSession(request) #get session
    username = s['username'] # have to get user name from session to put into database
    try:
        #update database
        chart_db = dataset.connect('sqlite:///chart.db')
        chart = chart_db.get_table('chart')
        chart.update({
            'username': username,
            'id' : id,
            'time' : time.strip(),
            'length' : length.strip(),
            'side' : side.strip(),
            'poops' : poops.strip(),
            'pees' : pees.strip()
        }, ['id'])
        #throw exception for protection
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return redirect('/')#return main page after edit







#-------------sign up--------------------
@get("/signup") #returns sign up page 
def getSignUp():
    return template("signup")

@post("/signup")
def postSignUp():
    s = getSession(request) #get session
    username = request.forms.get('username') #get username form page
    password = request.forms.get('password') #get password from page
    passwordRepeat = request.forms.get('password_again') #get password from page
    email = request.forms.get('email') #gets email from page
    if password != passwordRepeat: #makes sure the double password input is the same
        saveSession(response, s) 
        return redirect('/')    #will redirct to home page if not the same
    
    saveUser(username, { #saves user after signup
        'username':username,
        'credentials':generateCredentials(password),
        'email':email,
        'email_verified':False #will need to be verified 
    })
    sendVerificationEmail(username) #sends email for verificaiton 
    s['username'] = username #sets session user name to the new users name
    saveSession(response, s)
    return redirect('/') 






#-------------login------------------------
@get("/login") # returns template for login page
def getLogin(): 
    return template("login")

@post("/login")
def postLogin():
    s = getSession(request) #gets session from browser
    username = request.forms.get('username') #gets username
    password = request.forms.get('password') #gets password
    user = getUser(username) #checks to see if user is in data
    if not user:
        return redirect('/signup') #if not found will redirect user to signup page
    if 'credentials' not in user:
        return redirect('/signup')
    if not verifyPassword(password, user['credentials']):
        return redirect('/') #if password is wrong will redirect to home page
    s['username'] = username #gives user name to session
    saveSession(response, s) #saves the session
    return redirect('/') #will redirect to home page with the user being logged in 




#-------------log out-----------------------
@get("/logout")
def getLogout():
    s = getSession(request) #get session
    s['username'] = '' #change session info to no username
    saveSession(response, s) #save session
    return redirect('/') #redirect to main page





#---------------session functions------------------------
def getSession(request):
    
    def newSession(): #creates new session dic
        sessionId = newSessionId()
        s = { #creating dic
            "session_id" : sessionId,
            "username" : ''
        }
        return s #returning data

    sessionId = request.get_cookie("session_id", default=None) #asking for browser given data
    if sessionId == None:
        s = newSession() #if none found create new
    else: # if found, get it 
        try:
            s= read(sessionId) 
        except: # exception for proctection
            s = newSession()
    return s #return session 

#saving session 
def saveSession(response, session):
    write(session['session_id'], session) #write through json
    response.set_cookie("session_id", session['session_id'], path="/") # sets session 

#uses token function to get new session ID
def newSessionId():
    return createToken()

#create token for session ID
def createToken(k=32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k)) #creates random string





#---------------------json file functions---------------------------------------
def write(key, data):
    assert type(data) is dict
    with open(f"data/session.{key}.json", "w") as f: #writes to json file
        json.dump(data,f) #dumb for write
    return

def read(key):
    with open(f"data/session.{key}.json", "r") as f: #reads from json file
        data = json.load(f) #load for read
    assert type(data) is dict #make sure it is a dict data type
    return data

def getUser(name):
    try:
        with open(f"data/user.{name}.json", "r") as f: #reads from json file to find username
            data = json.load(f) #load for read
        assert type(data) is dict #makes sure is dic data ype
        return data
    except:
        return None

def saveUser(name, data):
    assert type(data) is dict #make sure it is a dict data type
    with open(f"data/user.{name}.json", "w") as f: #writes data to json file 
        json.dump(data,f) #dump for write
    return







#------------------------Credential functions---------------------
#function for hashing process
def bytesToString(byte):
    string = str(codecs.encode(byte,"hex"),"utf-8") #using utf-8 to change bytes to a string
    assert type(string) is str #making sure its a string
    return string
#function for hashing process
def stringToBytes(string):
    byte = codecs.decode(bytes(string,"utf-8"),"hex") #changing from string to bytes
    assert type(byte) is bytes #making sure its bytes
    return byte

#The hashing function 
def generateCredentials(Userpassword):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        Userpassword.encode('utf-8'), #Makes password byes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
    return {  #returns hash
        'salt':bytesToString(salt), 
        'key' :bytesToString(key),
    }

#passwords need to be verified. We need to hash and compare to see if its verifiable 
def verifyPassword(Userpassword, Usercredentials):
    salt = stringToBytes(Usercredentials['salt']) #get salt
    key  = stringToBytes(Usercredentials['key'])  #get key
    
    newKey = hashlib.pbkdf2_hmac( #process to hash the password to compare
        'sha256', # The hash digest algorithm for HMAC
        Userpassword.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
    return newKey == key #returns bool to see if they match





#-------------------------email functions --------------------

#verify email
def sendVerificationEmail(username):
    user = getUser(username) #get user from json file
    email = user['email'] #get email
    token = createToken() #create a token
    user['token'] = token # place the user token as the new token just created
    saveUser(username, user)

    verifyUrl = f"http://localhost:8080/verify/{token}" 

    # send_message(email, message)
    sender = "<app@example.com>"
    receiver = f"{username}<{email}>"

    #sending raw text file
    text = f"""\

        Please verify your email.
        You will need to be in your browser.
        
        {verifyUrl}

        Thank you,
        -Admin Dylan Dennison    
    """
    #sending html file
    html = f"""\
        <html>
        <body>
        <p>Thank you for signing up!<br/></p>
        <p>Please verify your email by clicking the link here.<br/></p>

        <p><a href="{verifyUrl}">{verifyUrl}</a><br/></p>

        <p>Thank you,<br>-Admin Dylan Dennison</p>
        </body>
        </html>
    """
    #setting email attributes 
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Verification"
    message["From"] = sender
    message["To"] = receiver

    #attaching the files above
    message.attach(MIMEText(text,"plain"))
    message.attach(MIMEText(html,"html"))

    #using mailtrap
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("f4a16f7c435447", "e1029eafd6dd17")
        server.sendmail(sender, receiver, message.as_string())

    return

#reset password email
def sendResetEmail(username):
    user = getUser(username) #get user from json file
    email = user['email'] #get email
    token = createToken() #create a token
    user['reset_token'] = token # place the token created as the reset token in the data file
    saveUser(username, user) #save data


    resetUrl = f"http://localhost:8080/reset/{username}/{token}"

    # send_message(email, message)
    sender = "<app@example.com>"
    receiver = f"{username}<{email}>"

    text = f"""\
        Please reset you password.
        You will need to be in your browser.
        
        {resetUrl}

        Thank you,
        -Admin Dylan Dennison
    """

    html = f"""\
        <html>
        <body>
        <p>Sorry for the Issue.<br/></p>
        <p>Please reset you password by clicking the link here.<br/></p>

        <p><a href="{resetUrl}">{resetUrl}</a><br/></p>

        <p>Thank you,<br>-Admin Dylan Dennison</p>
        </body>
        </html>
    """
    #setting email attributes
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = sender
    message["To"] = receiver

    #attaching the files above
    message.attach(MIMEText(text,"plain"))
    message.attach(MIMEText(html,"html"))

    #using mailtrap
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("f4a16f7c435447", "e1029eafd6dd17")
        server.sendmail(sender, receiver, message.as_string())

    return




#-------------verify functions-----------------
@get("/verify/<token>")
def getVerify(token):
    s = getSession(request) #save session 
    username = s['username'] #get user name
    user = getUser(username) #get user name from data file
    if token == user['token']: # if the tokens match verify the email
        user['email_verified'] = True
        saveUser(username, user) #save the user in json file




#-----------password recovery page----------
@get("/recovery") #returns password recovery template
def getSignup():
    return template("recovery")

@post("/recovery") 
def postSignup():
    username = request.forms.get('username') #gets username from webpage
    user = getUser(username) #gets user from json data
    if user['email_verified']: #if the email has been verified it will send a reset link via email 
        sendResetEmail(username)
    return redirect('/') #returns to the main page





#---------------reset password page--------------------
@get("/reset/<username>/<reset_token>")
def getReset(username, reset_token):
    s = getSession(request) #get session
    s['csrf_token'] = createToken() #make token for csrf
    user = getUser(username) #get user from data

    if reset_token == user['reset_token']: #if reset token matches it will return the reset page
        saveSession(response, s)
        return template("reset", username=username, reset_token=reset_token, csrf_token=s['csrf_token'])
    return redirect('/')

@post("/reset/<username>/<reset_token>")
def postReset(username, reset_token):
    s = getSession(request) #get session
    if 'csrf_token' not in s: # if the csrf token is not in the session data, redirect to main page
        redirect('/')
    # check the csrf token
    if request.forms.get('csrf_token') != s['csrf_token']: 
        redirect('/')
    s['csrf_token'] = None #empty csrf token
    user = getUser(username) #get user data
    
    if reset_token != user['reset_token']: #if reset tokens do not match redirect to main page again
        return redirect('/')
    user['reset_token'] = None #wipe reset token
    # get new password
    password = request.forms.get('password') # get pass word
    passwordRepeat = request.forms.get('password_again') # get password again 
    if password != passwordRepeat: #make sure they match
        saveSession(response, s) #save the session data
        return redirect('/') #redirect to main
    user['credentials'] = generateCredentials(password) # if everything checks out, save the new password 
    saveUser(username, user) #save the data to the json file
    return redirect('/login') #redirect to the login page 



#----------------------static pictures--------------------------
#these allow a photo on a dynamic website
@route("/static/png/<filename:re:.*\.png>")
@route("/image/<filename:re:.*\.png>")
def get_image(filename):
    return static_file(filename=filename, root="static/images", mimetype="image/png")

@route("/static/<filename:path>")
def get_static(filename):
    return static_file(filename=filename, root="static")




if __name__ == "__main__":
    debug(True)
    run(host="localhost", port=8080)
else:
    application = default_app()