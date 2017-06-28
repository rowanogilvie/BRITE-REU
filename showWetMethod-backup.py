#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies
cgitb.enable()
#backup
cookie = get_cookies()
if cookie:
    print(cookie)
    fname = cookie["fname"].value
    lname = cookie["lname"].value
    name = " ".join((fname, lname))
    admin = cookie["admin"].value
    uid = cookie["uid"].value
    uname = cookie["uname"].value
    
    
    form = cgi.FieldStorage()
    
    new = form.getvalue("wetname")
    des1 = form.getvalue("description")
    wmid = form.getvalue("wmid")
    
    user="d4prdb17"
    passwd="d4prp455"
    
    if new == None:
        new = ""
    if des1 == None:
        des1 = ""
    if wmid == None:
        wmid = ""
    
    def addwetMethod(name, des1):
        connection = pymysql.connect(host="localhost", user="d4prdb17", db="group9", passwd="d4prp455")
        cursor = connection.cursor()
        query = """INSERT INTO WetlabMethod (name, description)
                    VALUES ("%s", "%s");"""%(name, des1)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def delwetMethod(wmid):
        connection = pymysql.connect(host="localhost", user="d4prdb17", db="group9", passwd="d4prp455")
        cursor = connection.cursor()
        query = """delete from WetlabMethod where wmid = ("%s");""" %(wmid)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    
    def runQuery(query, user, passwd):
        connection = pymysql.connect(host="localhost",db="group9",user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res
    if len(new) != 0:
        addwetMethod(new, des1)
        print("Location: showWetMethod.py")
    elif len(wmid) != 0:
        delwetMethod(wmid)
        print("Location: showWetMethod.py")
         
    print("Content-type: text/html\n")
    print("""
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
    	<title>DASR</title>
    	<meta charset="utf-8"/>
    	<link href="../../dapr_test/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
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
         <ul>
         <li>Logged in as <a href=#>%s</a></li>
         <br/>
         """ % name)
    if admin == "1":
        print('<li style="float: right; color:red ! important;">admin</li><br/>')
    
    print("""
         
         <li style="float: right;"><a href="http://128.197.87.29/cgi-bin/dapr_test/logout.py">Log out</a></li>
         </ul>
         </div>
    		<nav><ul>
    			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/index.py">Home</a></li>
    			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/help.py">Help</a></li>
                <li><a href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</a></li>
    		</ul></nav>
    	</header>
    
      <div class="colmask blogstyle">                            
              <div class="col1">					
              <h3>Manage</h3>
    			<ul>
    				<li><a class="" title="Manage Experiments" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showexperiment.py">Manage Experiments</a></li>
    				<li><a class="" title="Manage Studies" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showstudy.py">Manage Studies</a></li>
    				<li><a class="" title="Manage Projects"
        href="http://128.197.87.29/cgi-bin/dapr_test/showproject.py">Manage Projects</a></li>
    				<li><a class="" title="Manage Platforms" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showplatform.py">Manage Platforms</a></li>
    				<li><a class="" title="Manage Users" href="http://128.197.87.29/cgi-bin/dapr_test/showusers.py">Manage Users</a></li>
                    <li><a class="" title="Manage Computational Method"
        href="http://128.197.87.29/cgi-bin/dapr_test/showComMethod.py">Manage Computational Method</a></li>
                    <li><a class="" title="Manage Wetlab Method"
        href="http://128.197.87.29/cgi-bin/dapr_test/showWetMethod.py">Manage Wetlab Method</a></li>

    			</ul>
            </div>
    
            <div class="col2">
              <h3>BEDTools</h3>
    			<ul>
    				<li><a class="" title="Compare BEDFiles and store them in BED format in database" 
        href="http://128.197.87.29/cgi-bin/dapr_test/BEDfile.py">CompareBEDFiles</a></li>
    			</ul>
            </div>
     
            <div class="col3">
            <h3>Upload</h3>
    			<ul>
    				<li><a class="" title="Upload data to a new experiment" 
        href="http://128.197.87.29/cgi-bin/dapr_test/upload_v0.1.py">Upload BEDfile</a></li>
    			</ul>	
            </div>
    </div>
    </br>
    """)
    

    print('<p><font size="4">All Wetlab Method for user <b>%s</b>:</font></p>'%name)
    q1="""
    select wmid, name, description
    from WetlabMethod;
    """ 
    
    res1 = runQuery(q1, user, passwd)
    
    if len(res1) != 0 :
        print("""
        <div class="datagrid"><table border=1>
          <thead>
                 <tr>
                     <th>wmid</th>
                     <th>Wetlab Method</th>
                     <th>Description</th>
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
          print('<tbody><tr>')
          if str(res1[i][1])== None:
            print("""<td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1])," "))
          else:
            print("""<td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1]),str(res1[i][2])))
          print("</tr></tbody>")
        print("</table></div></br></br>")
    
    print("""
    <p><b>Add a new Wetlab Method:</b></p>
    (Remember to type in the Method name!)
    <br/>
    <br/>
    <form method="post" action="http://128.197.87.29/cgi-bin/dapr_test/showWetMethod.py" enctype="multipart/form-data">
               Method name:
                   <br/>
              	</br>
              	<input type="text" name="wetname" size="55" maxlength="255" title="Enter Method Name">
              	</br>
               <br/>
              	Description:
                   <br/>
              	</br>
              	<input type="text" name="description" size="55" maxlength="255" title="Enter Description"> 
              </br>
              <p><input type="submit" value="Add" /></p>
          </form>""")

    print("""
    <p><b>Remove Wetlab Method:</b></p>
    (Remember to type in the Wetlab wmid!)
    <br/>
    <br/>
    <form method="post" action="http://128.197.87.29/cgi-bin/dapr_test/showWetMethod.py" enctype="multipart/form-data">
              Wetlab wmid:
                   <br/>
              	</br>
              	<input type="text" name="wmid" size="55" maxlength="255" title="Enter Wetlab wmid">
              	</br>
              <p><input type="submit" value="Remove" /></p>
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
    
else:
    print("Location: login.py")
    print("Content-type: text/html\n")
