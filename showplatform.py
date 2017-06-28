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
    
    plname = form.getvalue("plname")
    des1 = form.getvalue("description")
    genoinfo = form.getvalue("genom")
    plid = form.getvalue("plid")
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if plname == None:
        plname = ""
    if des1 == None:
        des1 = ""
    if plid == None:
        plid = ""
    
    def addPlatform(plname, des1, genoinfo):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """INSERT INTO Platform (plname, description, genomeinfo)
                    VALUES ("%s", "%s","%s");"""%(plname, des1, genoinfo)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def delPlatform(plid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """delete from Platform where plid = ("%s");""" %(plid)
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

    if len(plname) != 0:
        addPlatform(plname, des1, genoinfo)
        print("Location: showplatform.py")
    elif len(plid) != 0:
        delPlatform(plid)
        print("Location: showplatform.py")
         
    print("Content-type: text/html\n")
    
    phead(name, admin)
    print("""<div class="container">""")
    print('<p class="lead">All Platform :</p>')
    q1="""
    select plid,plname, description, genomeinfo
    from Platform;
    """ 
    
    res1 = runQuery(q1, user, passwd)
    
    if len(res1) != 0 :
        print("""
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>Platform</th>
                     <th>Description</th>
                     <th>Genome Information</th>
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
            print('<tbody><tr>')
            if res1[i][2]== None:
                if res1[i][3] == None:
                    print("""<td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1])," "," "))
                else:
                    print("""<td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1])," ",str(res1[i][3])))
            elif res1[i][3]== None:
                print("""<td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1]),str(res1[i][2]), " "))
            else:
                print("""<td>%s</td><td>%s</td><td>%s</td><td>%s</td>""" % (str(res1[i][0]),str(res1[i][1]),str(res1[i][2]), str(res1[i][3])))
            print("</tr></tbody>")
        print("</table></table></br></br>")
    
    print("""
    <p class="lead">Add a new Platform:</p>
    (Remember to type in the Platform name!)
    <br/>
    <br/>
    <form class="form-horizontal" method="post" action="./showplatform.py" enctype="multipart/form-data">
      <div class="form-group"> 
        <div class="col-xs-8"> 
        <label for="input-Platform" class="col-sm-2 control-label">Platform name:</label>
        <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter Platform name" name="plname" size="55" maxlength="255" title="Enter Method Name">
         </div>
        </div>
      </div>
        <div class="form-group">
        <div class="col-xs-8">
        <label for="selectproject" class="col-sm-2 control-label">Description:</label>
         <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter Description" name="description" size="55" maxlength="255" title="Enter Description"> 
        </div>
        </div>
      </div>
        <div class="form-group">
        <div class="col-xs-8">
        <label for="selectproject" class="col-sm-2 control-label">Genome Information:</label>
         <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter Genome Information" name="genom" size="55" maxlength="255" title="Enter Description"> 
                     </div>
        </div>
      </div>
              <p><input type="submit" value="Add" class="btn btn-lg btn-default"></p>
          </form>""")

    print("""
    <p class="lead">Remove Platform:</p>
    (Remember to type in the Platform ID!)
    <br/>
    <br/>
    <form method="post" action="./showplatform.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
        <label for="input-des1" class="col-sm-2 control-label">Platform ID:</label>
          <div class="col-sm-10">
                <input class="form-control" placeholder="Please enter platform ID" type="text" name="plid" size="55" maxlength="255" title="Enter Platform ID">
          </div>
        </div>
      </div>
      </br>
      </br>
      </br>
              <p><input type="submit" value="Remove" class="btn btn-lg btn-default"></p>
          </form>
          </div>""")

    ptail()
    
else:
    print("Location: login.py")
    print("Content-type: text/html\n")
