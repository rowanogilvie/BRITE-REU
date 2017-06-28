#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
#from functions import get_cookies
cgitb.enable()
#unsure of purpose- not being called on website

#cookie = get_cookies()
#if cookie:
#    print(cookie)
#    fname = cookie["fname"].value
#    lname = cookie["lname"].value
#    name = " ".join((fname, lname))
#    admin = cookie["admin"].value
#    uid = cookie["uid"].value
#    uname = cookie["uname"].value

form = cgi.FieldStorage()

email = form.getvalue("email")
fname = form.getvalue("fname")
lname = form.getvalue("lname")
uname = form.getvalue("uname")
    
user="d4prdb17"
passwd="d4prp455"
    
if email == None:
    email = ""
if fname == None:
    fname = ""
if lname == None:
    lname = ""
if uname == None:
    uname = ""
    
def runQuery(email, fname, lname, uname):
    connection = pymysql.connect(host="bioed.bu.edu", user="hjunming1", db="group9", passwd="BF768")
    cursor = connection.cursor()
    query = """INSERT INTO User (email, firstname, lastname, username) VALUES ("%s", "%s", "%s", "%s");"""%(email, fname, lname, uname)
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

#if len(email) != 0:
#    addUser(email, fname, lname, uname)
#    print("Location: registration2.py")

res1 = runQuery(email, fname, lname, uname)

print("Content-type: text/html\n")
print("""
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
    	<title>DASR</title>
    	<meta charset="utf-8"/>
    	<link rel="stylesheet" href="../../dapr_test/css/index.css" type="text/css" />
       <link rel="stylesheet" href="../../dapr_test/css/table.css" type="text/css" />
    	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    
    <body class = "body">
    	<header class = "mainheader">
         <a href = "http://128.197.87.29/cgi-bin/dapr_test/index.py">
    	    <img src="https://bioed.bu.edu/students_17/Group9/dasr_logo.png" /></a>
         <div class="alignright">
         <br/>
         
         <li style="float: right;"><a href="http://128.197.87.29/cgi-bin/dapr_test/logout.py">Log out</a></li>
         </ul>
         </div>
    		<nav><ul>
    			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/index.py">Home</a></li>
    			<li><a href="#">Help</a></li>
                <li><a href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</a></li>
    		</ul></nav>
    	</header>
     """)

print("""
    <p><b>Register:</b></p>
    (Remember to...)
    <br/>
    <br/>
    <form method="post" action="http://128.197.87.29/cgi-bin/dapr_test/registration2.py" enctype="multipart/form-data">
               Email Address:
                   <br/>
              	</br>
              	<input type="text" name="email" size="55" maxlength="255" title="Enter Email">
              	</br>
               <br/>
              	First Name:
                   <br/>
              	</br>
              	<input type="text" name="fname" size="55" maxlength="255" title="Enter First Name"> 
              </br>
               Last Name:
                   <br/>
              	</br>
              	<input type="text" name="lname" size="55" maxlength="255" title="Enter Last Name">
              	</br>
               Username:
                   <br/>
              	</br>
              	<input type="text" name="uname" size="55" maxlength="255" title="Enter Username">
              	</br>
               <br/>
               <br/>
              <p><input type="submit" value="Add" /></p>
          </form>""")

print("""
    </br>
    </br>
    	<div class="footer">
    	<link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
                <ul>
                    <li><a title="Boston University" href="http://www.bu.edu/">Boston University</a></li>
                    <li>DASR version 2.0.0.</li>
                    <li>%s</li>
                </ul>  
        </div>
    </body>
    </html>
    """ % str(datetime.datetime.now())[:-7])
    
#else:
#    print("Location: registration2.py")
#    print("Content-type: text/html\n")
