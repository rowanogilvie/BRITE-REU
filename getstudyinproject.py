#!/usr/local/bin/python3.3

import cgi
import cgitb
import pymysql
from functions import get_cookies
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

form = cgi.FieldStorage()
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
    return res

prid = form.getvalue('prid')

q1 = """
select sid, sname from Study join ProjectStudy using(sid) 
where prid="%s" and creator = "%s"
order by date desc, sname asc;
""" % (prid, uname)


studies = runQuery(q1, user, passwd)

print("""<option value="-- please select a study--"></option>""")
for row in studies:
    print("<option value=%s>%s</option>" % (row[0], row[1]))


