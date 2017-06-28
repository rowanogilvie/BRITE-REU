#!/usr/local/bin/python3.3
import cgi 
import os
import cgitb
import pymysql
cgitb.enable()

#unsure of purpose

fname = cookie["fname"].value
lname = cookie["lname"].value
name = " ".join((fname, lname))
admin = cookie["admin"].value
uid = cookie["uid"].value
uname = cookie["uname"].value
form = cgi.FieldStorage()
geneFile = form.getvalue("file")


def runQuery(name, location, description,command):
    connection = pymysql.connect(host="bioed.bu.edu", user="d4prdb17", db="group9", passwd="d4prp455")
    cursor = connection.cursor()
    query1 = """INSERT INTO BEDfile (name, location, description, upload_date, bedtoolcommand)
                VALUES ("%s", "%s", "%s", now(), "%s");"""%(name, location, description,command)
    cursor.execute(query1)
    connection.commit()
    cursor.close()
    connection.close()


print("Content-type: text/html\n")
if geneFile == None:
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
      <li><a href="#">Help</a></li>
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
        <li><a class="" title="Manage Platforms" href="#">Manage Platforms</a></li>
        <li><a class="" title="Manage Users" href="#">Manage Users</a></li>
      </ul>
        </div>

        <div class="col2">
          <h3>BEDTools</h3>
      <ul>
        <li><a class="" title="Compare BEDFiles and store them in BED format in database" 
    href="http://128.197.87.29/cgi-bin/dapr_test/showbedajax.py">CompareBEDFiles</a></li>
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
    
    
    print("""
    <div id="content"> 
         <h3>Upload Data To A New Experiment</h3>
          <form method="post" action="http://128.197.87.29/cgi-bin/dapr_test/upload_v0.1.py" enctype="multipart/form-data" >
          <dl>
              <dt class="optional" id="file_dt"><label for="file">Upload Data File:</label></dt>
              <input type="file" name="file" id="file">
              <div>Description:
                  <input type="text" name = "description">
                  </br>
                  BEDtools command:<input type="text" name = "command">
              </div></br>
              <input type="hidden" id="uid" value="%s">
               <b>Project: </b><select name='project' id="project" onchange="showstudies(this.value);">
                 <option value="">-- please select a project-- </option>""" % uid)
    for row in projects:
      print("""     <option value="%s">%s</option>""" % (row[0], row[0]))

    print("""
</select>
              <a title="Click to add a new Project first" href="">(set up new project)</a>
              <br />
              <br />
              <b>Studies: </b>
              <select name='study' id="study" onchange="showexps(this.value);">
              
              </select>
              <a title="Click to add a new Study first" href="">(set up new Study)</a>
            """)


    print("""
              <br />
              <br />
              <b>Experiments: </b>
              <select name='exp' id="exp" onchange="showbeds(this.value, getElementById('uid').value);">
              <option value="-- please select a experiment--"></option>
              </select>
              <a title="Click to add a new Experiment first" href="">(set up new experiment)</a>
              
            """)


    print("""<p><input type="submit" value="upload" /></p>
              
          </dl> 
          </form>

    </div>    
  <div class="footer">
  <link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
        <ul>
            <li><a title="Boston University" href="http://www.bu.edu/">Boston University</li></a>
            <li><a>DASR version 2.0</a></li>
    </ul>     
    </div>
</br>

<font size="3"><script language="JavaScript" type="text/JavaScript">
var day="";
var month="";
var ampm="";
var ampmhour="";
var myweekday="";
var year="";
mydate=new Date();
myweekday=mydate.getDay();
mymonth=mydate.getMonth()+1;
myday= mydate.getDate();
myyear= mydate.getYear();
year=(myyear > 200) ? myyear : 1900 + myyear;
var currentdata = mymonth+"/"+myday+"/"+year
document.write(currentdata);
</script></font>
</br>
</div>
</body>
</html>
""")
else:
     fileitem = form['file']
     description = form.getvalue("description")
     command = form.getvalue("command")
     eid = form.getvalue("exp")
     if fileitem.filename:
        fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
        open('/www/html/students_17/Group9/bedfiles/' + fn, 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was successfully uploaded'
        location = '/students_17/Group9/bedfiles/' + fn
        runQuery(fn.split('.')[0], location, description,command)
        q2 = """
        select bid from BEDfile 
        where name="%s"
        order by upload_date DESC
        limit 1;
        """ % fn.split('.')[0]
        bid = RunQuery(q2, "exampleUsername", "BF768")
        runQuery2(bid[0][0],eid)
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

</br>

<font size="3"><script language="JavaScript" type="text/JavaScript">
var day="";
var month="";
var ampm="";
var ampmhour="";
var myweekday="";
var year="";
mydate=new Date();
myweekday=mydate.getDay();
mymonth=mydate.getMonth()+1;
myday= mydate.getDate();
myyear= mydate.getYear();
year=(myyear > 200) ? myyear : 1900 + myyear;
var currentdata = mymonth+"/"+myday+"/"+year
document.write(currentdata);
</script></font>
</br>
</div>
    </body>
    </html>
    """ % (message,bid[0][0]))
    


