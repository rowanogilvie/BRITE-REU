#!/usr/local/bin/python3.3
import cgi 
import os
import cgitb
import pymysql
import datetime
from functions import get_cookies
cgitb.enable()
#unsure of purpose

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
    geneFile = form.getvalue("file")
    
    user="d4prdb17"
    passwd="d4prp455"

    def runQuery(name, location, des1, des2, des3, command, uname, cmid, wmid):
        connection = pymysql.connect(host="bioed.bu.edu", user="hjunming1", db="group9", passwd="BF768")
        cursor = connection.cursor()
        query1 = """INSERT INTO BEDfile (name, location, description1, description2, description3, 
        upload_date, bedtoolcommand, uploader, cmid, wmid)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, %s)
                    """%(name, location, des1, des2, des3, str(datetime.datetime.now())[:-7],
                         command, uname, int(cmid), int(wmid))
        cursor.execute(query1)
        connection.commit()
        cursor.close()
        connection.close()
    def runQuery2(bid,eid,uid):
        connection = pymysql.connect(host="bioed.bu.edu", user="hjunming1", db="group9", passwd="BF768")
        cursor = connection.cursor()
        query2 = """INSERT INTO ExperimentBEDfile(eid,bid)
              VALUES (%s,%s);"""%(eid,bid)
        #query3 = """ INSERT INTO ComputationalMethod (cmid, name, bid)
              #VALUES (%s, %s, %s)"""(cmid, cname, bid)
        #query4 = """ INSERT INTO WetlabMethod (bid, wimid, name)
              #VALUES (%s, %s, %s)"""(bid, wimid, cname)
        query5 = """ INSERT INTO UserBEDfile (uid, bid)
              VALUES (%s, %s)"""%(uid, bid)
        cursor.execute(query2)
        #cursor.execute(query3)
        #cursor.execute(query4)
        cursor.execute(query5)
        connection.commit()
        cursor.close()
        connection.close()

    def RunQuery(query, user, passwd):
        connection = pymysql.connect(host="localhost",db="group9",user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res


    print("Content-type: text/html\n")
    if geneFile == None:
        print("""
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js">
    </script>
    <script>
    function showstudies(str) {
                      if (str == "") {
                        document.getElementById("study").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("study").innerHTML = xmlhttp.responseText;
                                 document.getElementById("exp").innerHTML = "";
                        }
                      }
                       
                          xmlhttp.open("GET","getstudyinproject.py?prid="+str,true);
                      xmlhttp.send();
                    }
                };

    function showexps(str) {
                      if (str == "") {
                        document.getElementById("exp").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("exp").innerHTML = xmlhttp.responseText;
                        }
                      }
                       
                          xmlhttp.open("GET","getexperimentinstudy.py?sid="+str,true);
                      xmlhttp.send();
                    }
                };

    function showbeds(str) {
                      if (str == "") {
                        document.getElementById("bed").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("bed").innerHTML = xmlhttp.responseText;
                        }
                      }
                       
                          xmlhttp.open("GET","getbedinexperiment.py?eid="+str,true);
                      xmlhttp.send();
                    }
                };
    </script>
    """)

        q1 = """
        select prid, prname from Project
        where creator="%s"
        order by date desc, prname asc;
        """ % uname

        projects = RunQuery(q1, user, passwd)
        print("""
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
        	<title>DASR</title>
        	<meta charset="utf-8"/>
        	<link rel="stylesheet" href="/students_17/Group9/css/index.css" type="text/css" />
           <link rel="stylesheet" href="/students_17/Group9/css/table.css" type="text/css" />
        	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        </head>
        
        <body class = "body">
        	<header class = "mainheader">
             <a href = "https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/index.py">
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
             
             <li style="float: right;"><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/logout.py">Log out</a></li>
             </ul>
             </div>
        		<nav><ul>
        			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/index.py">Home</a></li>
        			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/help.py">Help</a></li>
                    <li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/about.py">About</a></li>
        		</ul></nav>
        	</header>
        
          <div class="colmask blogstyle">                            
                  <div class="col1">					
                  <h3>Manage</h3>
        			<ul>
        				<li><a class="" title="Manage Experiments" 
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showexperiment.py">Manage Experiments</a></li>
        				<li><a class="" title="Manage Studies" 
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showstudy.py">Manage Studies</a></li>
        				<li><a class="" title="Manage Projects"
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showproject.py">Manage Projects</a></li>
        				<li><a class="" title="Manage Platforms"
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showplatform.py">Manage Platforms</a></li>
        				<li><a class="" title="Manage Users" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showusers.py">Manage Users</a></li>
                        <li><a class="" title="Manage Computational Method"
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showComMethod.py">Manage Computational Method</a></li>
                        <li><a class="" title="Manage Wetlab Method"
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showWetMethod.py">Manage Wetlab Method</a></li>
    
        			</ul>
                </div>
        
            <div class="col2">
              <h3>BEDTools</h3>
    			<ul>
    				<li><a class="" title="Compare BEDFiles and store them in BED format in database" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/BEDfile.py">CompareBEDFiles</a></li>
            <li><a class="" title="Show BED file" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showBED.py">Show BED Files</a></li>
    			</ul>
            </div>
         
                <div class="col3">
                <h3>Upload</h3>
        			<ul>
        				<li><a class="" title="Upload data to a new experiment" 
            href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/upload_v0.1.py">Upload BEDfile</a></li>
        			</ul>	
                </div>
        </div>
        </br>
        """)
        
        
        print("""
        <div id="content"> 
             <h3>Upload BED file To A New Experiment</h3>
              <form method="post" action="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/upload_v0.1.py" enctype="multipart/form-data" >
              <dl>
                  <dt class="optional" id="file_dt"><label for="file">Upload BED File:
                      <br/><b style="color:red ! important";>Duplicate file names are not allowed!</b>
                      </label></dt>
                  
                  <input type="file" name="file" id="file">
                  <div><b>Description1:</b>
                      <input type="text" name = "des1">
                      </br>
                      <b>Description2:</b>
                      <input type="text" name = "des2">
                      </br>
                      <b>Description3:</b>
                      <input type="text" name = "des3">
                      </br>
                      <b>BEDtools command:</b><input type="text" name = "command">
                  </div></br>
                   <b>Project: </b><select name='project' id="project" onchange="showstudies(this.value)";>
                     <option>-- please select a project-- </option>""")
        for row in projects:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))

        print("""
    </select>
                  <a title="Click to add a new Project first" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showproject.py">(set up new project)</a>
                  <br />
                  <br />
                  <b>Studies: </b>
                  <select name='study' id="study" onchange="showexps(this.value)";>
                  <option>-- please select a study-- </option>
                  </select>
                  <a title="Click to add a new Study first" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showstudy.py">(set up new Study)</a>
                """)


        print("""
                  <br />
                  <br />
                  <b>Experiments: </b>
                  <select name='exp' id="exp" onchange="showbeds(this.value)";>
                  <option>-- please select a experiment--</option>
                  </select>
                  <a title="Click to add a new Experiment first" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showexperiment.py">(set up new experiment)</a>
                  <div id="bed"></div>
                """)
        q2 = """
        select cmid, name from ComputationalMethod
        """
        ComMethod = RunQuery(q2, user, passwd)

        print("""
                  <br />
                  <br />
                  <b>Computational method: </b>
                  <select name='Com' id="exp">
                  <option value=""> -- please select a computational method--</option>""")
        for row in ComMethod:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
        print(""" 
                  </select>
                  <a title="Click to add a new Computational Method first" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showComMethod.py">(set up new Computational Method)</a>
                  
                """)

        q3 = """
        select wmid, name from WetlabMethod
        """
        WetMethod = RunQuery(q3, user, passwd)

        print("""
                  <br />
                  <br />
                  <b>Wetlab method: </b>
                  <select name='Wet' id="exp";">
                  <option value="">-- please select a wetlab method--</option>""")
        for row in WetMethod:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
        print(""" 
                  </select>
                  <a title="Click to add a new Wetlab Method first" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showWetMethod.py">(set up new Wetlab Method)</a>
                  
                """)
        

        print("""<p><input type="submit" value="upload" /></p>
                  
              </dl> 
              </form>

        </div>    
    </br>

    <div class="footer">
            <ul>
                <li><a title="Boston University" href="http://www.bu.edu/">Boston University</a></li>
                <li>DASR version 2.0.0.</li>
                <li>%s</li>
            </ul>
    </div>
    </body>
    </html>
    """% str(datetime.datetime.now())[:-7])
    else:
         fileitem = form['file']
         des1 = form.getvalue("des1")
         des2 = form.getvalue("des2")
         des3 = form.getvalue("des3")
         command = form.getvalue("command")
         eid = form.getvalue("exp")
         cmid = form.getvalue('Com')
         wmid = form.getvalue('Wet')
         if fileitem.filename:
            fn = os.path.basename(fileitem.filename.replace("\\", "/" )).split('.')
            q3 = """
         	select bid from BEDfile
         	order by bid DESC
         	limit 1;
         	"""
            nbid = int(RunQuery(q3, user, passwd)[0][0])+1
            fn_new = fn[0] + "_" + str(nbid) + '.'+fn[1]
            open('/www/html/students_17/Group9/bedfiles/' + fn_new, 'wb').write(fileitem.file.read())
            message = 'The file "' + fn_new + '" was successfully uploaded'
            location = '/students_17/Group9/bedfiles/' + fn_new
            runQuery(nbid,fn[0] + "_" + str(nbid), location, des1, des2, des3, command,uname, cmid, wmid)
            runQuery2(nbid,eid, uid)
         else:
            message = 'No file was uploaded'
         print("""\
        <html>
        <head>
        <meta charset="utf-8">
        <title>upload file </title>
        </head>
        <body>
        <p>%s,%s</p>
        """ % (message,bid[0][0]))
else:
    print("Location: login.py")
    print("Content-type: text/html\n")
        


