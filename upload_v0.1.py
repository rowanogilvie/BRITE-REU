#!/usr/local/bin/python3.3
import cgi 
import os
import cgitb
import pymysql
import datetime
from functions import get_cookies,phead, ptail
cgitb.enable()
"""
The following issues need to be addressed:
-autofill platform from study
-runQuery issue when form unfilled/partially filled
-where the files are being put doesn't exist
-design is ugly
"""

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
#     sid = form.getvalue("study")
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"

    def runQuery(bid,name, location, des1, des2, des3, command, uname, cmid, wmid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query1 = """INSERT INTO BEDfile (bid,name, location, description1, description2, description3, 
        upload_date, bedtoolcommand, uploader, cmid, wmid)
                    VALUES (%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, %s)
                    """%(int(bid),name, location, des1, des2, des3, str(datetime.datetime.now())[:-7],
                         command, uname, int(cmid), int(wmid))
        cursor.execute(query1)
        connection.commit()
        cursor.close()
        connection.close()
    def runQuery2(bid,eid,uid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
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
        connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
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
        phead(name, admin)
        
        
        print("""
        <div id="content" align = "center"> 
             <h2 class="lead">Upload BED file To A New Experiment</h2>
             <h5 class="lead" style="color:red ! important;">* = required field</h5>
              <form method="post" action="./upload_v0.1.py" enctype="multipart/form-data" >
              <dl>
                  <dt class="optional" id="file_dt" align="center"><label for="file">* Upload BED File:
                      </label></dt>
                  <input type="file" name="file" id="file">
                  </br>
                  <div><b>Description 1:</b>
                      <input type="text" name = "des1">
                      <br />
                      <br />
                      <b>Description 2:</b>
                      <input type="text" name = "des2">
                      <br />
                      <br />
                      <b>Description 3:</b>
                      <input type="text" name = "des3">
                      <br />
                      <br />
                      <b>BEDtools command:</b><input type="text" name = "command">
                  </div></br>
                   <b>* Project: </b><select name='project' id="project" onchange="showstudies(this.value)";>
                     <option>-- please select a project-- </option>""")
        for row in projects:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))

        print("""
    </select>
                  <a title="Click to add a new Project first" href="./showproject.py">(set up new project)</a>
                  <br />
                  <br />
                  <b>* Studies: </b>
                  <select name='study' id="study" onchange="showexps(this.value)";>
                  <option>-- please select a study-- </option>
                  </select>
                  <a title="Click to add a new Study first" href="./showstudy.py">(set up new Study)</a>
                """)
        q6 = """
        select plid, plname from Platform
        """
        Platform = RunQuery(q6, user, passwd)
        
#         q6 = """
#         select plid, plname from Platform 
#         where sid ="%s"
#         """ % sid
        
        print("""
                  <br />
                  <br />
                  <b>* Experiments: </b>
                  <select name='exp' id="exp" onchange="showbeds(this.value)";>
                  <option>-- please select a experiment--</option>
                  </select>
                  <a title="Click to add a new Experiment first" href="./showexperiment.py">(set up new experiment)</a>
                  <!--div id="bed"></div-->
                  </br>
                """)

        print("""
                  </br>
                  <b>* Platform: </b>
                  <select name='plt' id="plt">
                  <option value=""> -- please select a Platform--</option>""")
        for row in Platform:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
           
          
        print(""" 
                  </select>
                  <a title="Click to add a new Platform first" href="./showplatform.py">(set up new Platform)</a>
                  
                """)



        
        q2 = """
        select cmid, name from ComputationalMethod
        """
        ComMethod = RunQuery(q2, user, passwd)

        print("""
                </br>
                  <br />
                  <b>* Computational method: </b>
                  <select name='Com' id="exp">
                  <option value=""> -- please select a computational method--</option>""")
        for row in ComMethod:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
        print(""" 
                  </select>
                  <a title="Click to add a new Computational Method first" href="./showComMethod.py">(set up new Computational Method)</a>
                  
                """)

        q3 = """
        select wmid, name from WetlabMethod
        """
        WetMethod = RunQuery(q3, user, passwd)

        print("""
                  <br />
                  <br />
                  <b>* Wetlab method: </b>
                  <select name='Wet' id="exp";">
                  <option value="">-- please select a wetlab method--</option>""")
        for row in WetMethod:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
        print(""" 
                  </select>
                  <a title="Click to add a new Wetlab Method first" href="./showWetMethod.py">(set up new Wetlab Method)</a>
                  
                """)
        

        print("""
    </br>
    </br>
    <p><input type="submit" value="upload" class="btn btn-lg btn-default"/></p>
                  
              </dl> 
              </form>

        </div>    
    </br>
    """)
        ptail()

    else:
         fileitem = form['file']
         des1 = form.getvalue("des1")
         des2 = form.getvalue("des2")
         des3 = form.getvalue("des3")
         command = form.getvalue("command")
         eid = form.getvalue("exp")
         cmid = form.getvalue('Com')
         wmid = form.getvalue('Wet')
         sid = form.getvalue('study')
         plid = form.getvalue('plt')
         if cmid == None:
          cmid = 0
         if wmid == None:
          wmid == 0
         q5 = """select plid from Platform join Study using(plid) where sid="%s" Group by  plid order by date desc;""" %sid
         in_platform = [i for i in RunQuery(q5, user, passwd)[0]]
         if fileitem.filename:
          if int(plid) in in_platform:
              fn = os.path.basename(fileitem.filename.replace("\\", "/" )).split('.')
              q3 = """
            select bid from BEDfile
            order by bid DESC
            limit 1;
            """
              nbid = int(RunQuery(q3, user, passwd)[0][0])+1
              fn_new = fn[0] + "_" + str(nbid) + '.'+fn[1]
              open('/var/www/dapr_test/bedfiles/' + fn_new, 'wb').write(fileitem.file.read())
              message = 'The file "' + fn_new + '" was successfully uploaded'
              location = '/dapr_test/bedfiles/' + fn_new
              runQuery(nbid,fn[0] + "_" + str(nbid), location, des1, des2, des3, command,uname, cmid, wmid)
              runQuery2(nbid,eid, uid)
          else:
            message = "please choose the right platform"
            print(in_platform, plid)
         else:
          message = 'No file was uploaded'
         print("""\
        <html>
        <head>
        <meta charset="utf-8">
        <title>upload file </title>
        </head>
        <body>
        <p>%s</p>
        """ % message)
else:
    print("Location: login.py")
    print("Content-type: text/html\n")
        


