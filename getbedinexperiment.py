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

eid = form.getvalue('eid')

#reduce reduncancy
user="d4prdb17"
passwd="d4prp455"
host="localhost"
db="group9"

qexname = "select title from Experiment where eid = '%s'" % eid

def runQuery(query, user, passwd):
    connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return res


if eid != "-- please select a experiment--":
    exname = runQuery(qexname, user, passwd)[0][0]

    q1 = """
    select b.bid, location, b.name, w.name, c.name, description1, description2, 
    description3, uploader, upload_date, bedtoolcommand
    from BEDfile b join ExperimentBEDfile using(bid)
    join WetlabMethod w using(wmid)
    join ComputationalMethod c using(cmid)
    where eid = "%s" and uploader = "%s"
    order by upload_date desc, b.name asc;
    """ % (eid,uname)
    
    beds = runQuery(q1, user, passwd)
    
    print('<p><font size="4">All BED files in experiment <b>%s</b>:</font></p>' % exname)
    print("""<div class="datagrid"><table border=1>
          <thead>
          <tr>
          <th>BED file</th>
          <th>Wetlab method</th>
          <th>Computational method</th>
          <th>Description1</th>
          <th>Description2</th>
          <th>Description3</th>
          <th>Uploader</th>
          <th>Upload time</th>
          <th>BEDtool command</th>
          <th>Download</th>
    </tr></thead>""")
    
    
    if len(beds) > 0:
        n1 = len(beds)
        for i in range(n1):
            row = beds[i]
            if i % 2 == 1:
                print("<tbody><tr class='alt'>")
            else:
                print("<tbody><tr>")
            for j in range(len(row)-2):
                j += 2
                if j == 2:
                    print("""<td>
                    <a href="./bedinfo.py?bid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("""<td><a href="%s">Download</a></td>""" % row[1])
            print("</tr></tbody>")
        print("</table></div><br/>")

