#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import hashlib
cgitb.enable()

print("Content-type: text/html\n")

# Below is the header HTML

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
         
         <li style="float: right;"><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/logout.py">Log out</a></li>
         </ul>
         </div>
    		<nav><ul>
    			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/index.py">Home</a></li>
    			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/help.py">Help</a></li>
          <li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/about.py">About</a></li>
    		</ul></nav>
    	</header>
     """)

print("""
<div>
<h1>HELP</h1>
</div>
""")

print("""
<div id="footer">
<a title="Boston University" href="http://www.bu.edu/">Boston University</a>
DASR version 9.11
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
document.write(mymonth+"/"+myday+"/"+year);
</script></font>
</br>
</div>
</body>
</html>
""")
