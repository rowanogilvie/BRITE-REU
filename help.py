#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import hashlib
from functions import get_cookies, phead, ptail
cgitb.enable()

cookie = get_cookies()

if cookie:
    print(cookie)
    fname = cookie["fname"].value
    lname = cookie["lname"].value
    name = " ".join((fname, lname))
    admin = cookie["admin"].value
    uid = cookie["uid"].value
    uname = cookie["uname"].value

print("Content-type: text/html\n")
phead(name, admin)
print("""<div class="container">""")

print("""
    <div class="lead">
    <h1 class="well">Help</h1>
    <p>more needs to be added</p>
    </div>
""")


ptail()

print("""
<br>
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
