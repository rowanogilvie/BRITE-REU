#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import hashlib
import http.cookies as Cookie
from functions import get_cookies

cgitb.enable()
"""
The following issues need to be addressed:
-reset password 
-create account
"""


#reduce redundancy
user="d4prdb17"
passwd="d4prp455"
host="localhost"
db="group9"

def runQuery(query, user, passwd):
    connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(res) > 0:
        return res
    else:
        return None

#get the form data (it will all be "nonetype" until someone hits 'submit')
form = cgi.FieldStorage()

cookie = get_cookies()

if cookie != None:
    print("Location: home.py")
    print("Content-type: text/html\n")
else:
    #extract specific fields from the form
    uname = form.getvalue("uname")
    pword = form.getvalue("pword")

    if pword != None:
        pword = hashlib.md5(pword.encode()).hexdigest()

    
    
    q1 = """select uid, username, pword_hash, firstname, lastname, admin, approved from User 
    WHERE username LIKE '%s' and pword_hash LIKE '%s';""" %(uname, pword)

    if uname == None or pword == None:
        print("Content-type: text/html\n")
        
        print("""
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
        	<title>DASR</title>
        	<meta charset="utf-8"/>
        	<link rel="stylesheet" href="../../dapr_test/css/login.css" type="text/css" />
         <link rel="stylesheet" href="../../dapr_test/css/table.css" type="text/css" />
        	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        </head>""")
        print("""
        <body class="body">
            <header class = "mainheader">
            <img src="https://bioed.bu.edu/students_17/Group9/dasr_logo.png"/>
        <div class="login-page">
            <div class="form">
            <form class="register-form" action='http://128.197.87.29/cgi-bin/dapr_test/login.py' method ='post'>
              <input type="text" placeholder="name"/>
              <input type="password" placeholder="password"/>
              <input type="text" placeholder="email address"/>
              <button>create</button>
              <p class="message">Already registered? <a href="#">Sign In</a></p>
            </form>
            <form class="login-form" action='http://128.197.87.29/cgi-bin/dapr_test/login.py' method ='post'>
              <input type="text" placeholder="username" name="uname"/>
              <input type="password" placeholder="password" name="pword"/>
              <button><input type="submit" name="login" value="Login" title="Click to sign in to DASR" id="login"/></button>
        	    <p class="message">Forgot password? <a href="./error.py">Reset password</a></p>
              <p class="message">New to DASR? <a href="#">Create an account</a></p>
            </form>
            </div>
        </div>
          
          	<div class="footer">
          	<link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
                <ul><li><a title="About" href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</li></a>
                    <li><a title="Boston University" href="http://www.bu.edu/" target="_blank">Boston University</li></a>
                    <li><a>DASR version 2.0</a></li>
        		</ul>     
            </div>
        </body>
        </html>
        """)

    else:
        validuser = runQuery(q1, user, passwd)
        if validuser == None:
            print("Content-type: text/html\n")
            print("Content-type: text/html\n")
            print("""
            <!DOCTYPE html>
            <html lang="en">
            
            <head>
                <title>DASR</title>
                <meta charset="utf-8"/>
                <link rel="stylesheet" href="../../dapr_test/css/login.css" type="text/css" />
             <link rel="stylesheet" href="../../dapr_test/css/table.css" type="text/css" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>""")
            print("""
            <body class="body">
                <header class = "mainheader">
                <img src="https://bioed.bu.edu/students_17/Group9/dasr_logo.png"/>
            <div class="login-page">
                <div class="form">
                <form class="register-form" action='http://128.197.87.29/cgi-bin/dapr_test/login.py' method ='post'>
                  <input type="text" placeholder="name"/>
                  <input type="password" placeholder="password"/>
                  <input type="text" placeholder="email address"/>
                  <button>create</button>
                  <p class="message">Already registered? <a href="#">Sign In</a></p>
                </form>
                <form class="login-form" action='http://128.197.87.29/cgi-bin/dapr_test/login.py' method ='post'>
                  <input type="text" placeholder="username" name="uname"/>
                  <input type="password" placeholder="password" name="pword"/>
                  <button><input type="submit" name="login" value="Login" title="Click to sign in to DASR" id="login"/></button>
                  <p class="message" style="color:red ! important;"><b>Invalid username or password!</b></p>
                    <p class="message">Forgot password? <a href="http://128.197.87.29/cgi-bin/dapr_test/error.py">Reset password</a></p>
                  <p class="message">New to DASR? <a href="#">Create an account</a></p>
                </form>
                </div>
            </div>
              
                  <div class="footer">
                  <link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
                    <ul><li><a title="About" href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</li></a>
                        <li><a title="Boston University" href="http://www.bu.edu/">Boston University</li></a>
                        <li><a>DASR version 2.0</a></li>
                    </ul>     
                </div>
            </body>
            </html>
            """)
        else:
            cookie = Cookie.SimpleCookie()
            cookie["uid"] = validuser[0][0]
            cookie["uid"]["max-age"] = 2*60*60
            
            cookie["uname"] = validuser[0][1]
            cookie["uname"]["max-age"] = 2*60*60
            
            cookie["pword"] = validuser[0][2]
            cookie["pword"]["max-age"] = 2*60*60
            
            cookie["fname"] = validuser[0][3]
            cookie["fname"]["max-age"] = 2*60*60
            
            cookie["lname"] = validuser[0][4]
            cookie["lname"]["max-age"] = 2*60*60
            
            cookie["admin"] = validuser[0][5]
            cookie["admin"]["max-age"] = 2*60*60
            
            cookie["appro"] = validuser[0][6]
            cookie["appro"]["max-age"] = 2*60*60
            
            print(cookie)
            print("Location: home.py")
            print("Content-type: text/html\n")
