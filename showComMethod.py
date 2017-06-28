#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail
cgitb.enable()
#no current known errors
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
    
    new = form.getvalue("comname")
    des1 = form.getvalue("description")
    cmid = form.getvalue("cmid")
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if new == None:
        new = ""
    if des1 == None:
        des1 = ""
    if cmid == None:
        cmid = ""

    
    def addComMethod(name, des1):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """INSERT INTO ComputationalMethod (name, description)
                    VALUES ("%s", "%s");"""%(name, des1)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def delComMethod(cmid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """delete from ComputationalMethod where cmid = ("%s");""" %(cmid)
        cursor.execute(query)
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
    if len(new) != 0:
        addComMethod(new, des1)
        print("Location: showComMethod.py")
    elif len(cmid) != 0:
        delComMethod(cmid)
        print("Location: showComMethod.py")
         
    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")
    

    print('<p class="lead">All Computational Method for user <b>%s</b>:</p>'%name)
    q1="""
    select cmid, name, description
    from ComputationalMethod;
    """ 
    
    res1 = runQuery(q1, user, passwd)
    
    if len(res1) != 0 :
        print("""
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>cmid</th>
                     <th>Computational Method</th>
                     <th>Description</th>
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
          print('<tbody><tr>')
          if str(res1[i][2])== None:
            print("""<td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1])," "))
          else:
            print("""<td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1]),str(res1[i][2])))
          print("</tr></tbody>")
        print("</table></table></br></br>")
    
    print("""
    <p class="lead">Add a new Computational Method:</p>
    (Remember to type in the Method name!)
    <br/>
    <br/>
    <form class="form-horizontal"method="post" action="./showComMethod.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
        <label for="input-project" class="col-sm-2 control-label">Method name:</label>
            <div class="col-sm-10">
              	<input class="form-control" type="text" placeholder="Please enter name" name="comname" size="55" maxlength="255" title="Enter Method Name">
          </div>
        </div>
      </div>
            <div class="form-group">
        <div class="col-xs-8">
        <label for="input-project" class="col-sm-2 control-label">Description:</label>
        <div class="col-sm-10">
              	<input class="form-control" type="text" placeholder="Please enter Description" name="description" size="55" maxlength="255" title="Enter Description"> 
          </div>
        </div>
      </div>
    <div>
    <input type="submit" value="Add" class="btn btn-lg btn-default">
    </div>
          </form>""")
    
    print("""
    </br>
    </br>
    </br>
     <p class="lead">Remove a Computational Method</p>
    (Remember to type in the Method cmid!)
    <br/>
    <br/>
    <form class="form-horizontal" method="post" action="./showComMethod.py" enctype="multipart/form-data">
          <div class="form-group">
        <div class="col-xs-8">
    <label for="input-project" class="col-sm-2 control-label">Method cmid:</label>
            <div class="col-sm-10">
              	<input class="form-control" type="text" placeholder="Please enter cmid"name="cmid" size="55" maxlength="255" title="Enter Method cmid">
          </div>
        </div>
      </div>
                <p><input type="submit" value="Remove" class="btn btn-lg btn-default"></p></form>

          </div>""")
    
    ptail()
else:
    print("Location: login.py")
    print("Content-type: text/html\n")
