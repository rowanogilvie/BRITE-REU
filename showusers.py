#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail
cgitb.enable()
"""
The following issues need to be addressed:
-need to add approve user and remove user functions
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

    email = form.getvalue("email")
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    uname = form.getvalue("uname")
    
    sid = form.getvalue('sid')
    
    qsname = "select uid, email, firstname, lastname, username from User;"
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if email == None:
        email = ""
    if fname == None:
        fname = ""
    if lname == None:
        lname = ""
    if uname == None:
        uname = ""

    def showUser(email, fname, lname, uname):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query1 = """select uid, email, firstname, lastname, username from User;"""
        cursor.execute(query1)
        connection.commit()
        qgeteid = """select uid, email, firstname, lastname, username from User;"""
        geteid = runQuery(qgeteid, user, passwd)
        eid = geteid[0][0]
        connection.commit()
        cursor.close()
        connection.close()

    def runQuery(query, user, passwd):
        connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res

    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")
    
    if admin == "1":
        print('<li style="float: right; color:red ! important;">admin</li><br/>')
    
    
    q1 = """select uid, email, firstname, lastname, username from User;"""

    if admin == "1" and sid == None:
        print('<p class="lead">All Users ADMIN = 1 SID = NONE</font></p>')
        q1 = """select uid, email, firstname, lastname, username from User;"""


    '''
    elif admin == "1" and sid:
        sname = runQuery(qsname, user, passwd)[0][0]
        print('<p class="lead">All Users ADMIN = 0, SID<b>%s</b>:</font></p>' % sname)
        q1 = """select """
        
        q2 = """"""
    
    elif admin == "0" and sid == None:
        print('<p class="lead">All Users ADMIN=0, SID=NONE</font></p>')
        q1 = """"""
        
        q2 = """"""
        
    else:
        sname = runQuery(qsname, user, passwd)[0][0]
        print('<p class="lead">All experiments in study <b>%s</b>:</font></p>' % sname)
        q1 = """"""
        
        q2 = """"""
    '''
    res1 = runQuery(q1, user, passwd)
    
    if len(res1) != 0 :
        print("""
        <div><table id="example" class="display" border=1>
          <thead>
                 <tr>
                     <th>uid</th>
                     <th>Email</th>
                     <th>First Name</th>
                     <th>Last Name</th>
                     <th>Username</th>
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
          print('<tbody><tr>')
          print("""<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1]),str(res1[i][2]),str(res1[i][3]),str(res1[i][4])))
          print("</tr></tbody>")
        print("</table></div></br></br>")

    ptail()

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
