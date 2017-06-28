#!/usr/local/bin/python3.3

"""
Created on Wed Apr 12 19:08:38 2017

@author: Zhe
"""
#unsure of purpose

import cgi
import cgitb
import pymysql

cgitb.enable()

print("Content-type: text/html\n")

form = cgi.FieldStorage()

def runQuery(query, user, passwd):
    connection = pymysql.connect(host="localhost",db="group9",user=user,passwd=passwd)
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return res

    
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
     <!-- a href = "http://128.197.87.29/cgi-bin/dapr_test/index.py"-->
	    <img src="https://bioed.bu.edu/students_17/Group9/dasr_logo.png" />
		<nav><ul>
			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/index.py">Home</a></li>
			<li><a href="#">Help</a></li>
            <li><a href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</a></li>
			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/login.py">LogOut</a></li>
		</ul></nav>
	</header>


<div id="wrapper">
  <div class="colmask blogstyle">    
    <div class="colmid">        
      <div class="colleft">            
        <div class="col1wrap">                
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
    </div>
  </div>
</div>
""")

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
                   
                      xmlhttp.open("GET","getstudyinproject.py?project="+str,true);
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
                   
                      xmlhttp.open("GET","getexperimentinstudy.py?study="+str,true);
            			xmlhttp.send();
            		}
        		};

function showbeds(str1, str2) {
               		if (str1 == "" || str2 == "") {
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
                   
                      xmlhttp.open("GET","getbedinexperiment.py?exp="+str1+"&uid="+str2,true);
            			xmlhttp.send();
            		}
        		};
</script>
""")

uid = form.getvalue('uid')
user="d4prdb17"
passwd="d4prp455"

q1 = """
select prname, description1, date from User join UserProject using(uid) 
join Project using(prid) 
where uid="%s";
""" % uid

projects = runQuery(q1, user, passwd)


print("""    
             <form>
             <input type="hidden" id="uid" value="%s">
             </form>
             <h2>Browse BEDfiles</h2>
             <hr />
             <form>
               <b>Project: </b><select name='project' id="project" onchange="showstudies(this.value);">
                 <option value="">-- please select a project-- </option>""" % uid)

for row in projects:
	print("""<option value="%s">%s</option>""" % (row[0], row[0]))

print("""
</select>
              <br />
              <br />
              </form>
              <form>
              <b>Studies: </b>
              <select name='study' id="study" onchange="showexps(this.value);">
              
              </select>
              </form>
""")


print("""
              <br />
              <br />
              <form>
              <b>Experiments: </b>
              <select name='exp' id="exp" onchange="showbeds(this.value, getElementById('uid').value);">
              <option value="-- please select a experiment--"></option>
              </select>
              </form>
              <div id="bed"></div>
""")




print("""
</br>
</br>
	<div class="footer">
	<link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
        <ul>
            <li><a title="Boston University" href="http://www.bu.edu/">Boston University</li></a>
            <li><a>DASR version 2.0</a></li>
		</ul>     
    </div>
	
<script language="JavaScript" type="text/JavaScript">
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
</script>
</div>

</body>
</html>
""")

