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
    
    newpr = form.getvalue("prname")
    des1 = form.getvalue("description1")
    des2 = form.getvalue("description2")
    des3 = form.getvalue("description3")
    prid = form.getvalue("prid")
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if newpr == None:
        newpr = ""
    if des1 == None:
        des1 = ""
    if des2 == None:
        des2 = ""
    if des3 == None:
        des3 = ""
    if prid == None:
        prid = ""
    
    def addProject(prname, des1, des2, des3, uname, date):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """INSERT INTO Project (prname, description1, description2, description3,
        creator, date)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s");"""%(prname,des1, des2, des3, uname, date)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def delProject(prid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """delete from Project where prid = ("%s");""" %(prid)
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
    
    if len(newpr) != 0:
        addProject(newpr, des1, des2, des3, uname, str(datetime.date.today()))
        print("Location: showproject.py")
    elif len(prid) != 0:
        delProject(prid)
        print("Location: showproject.py")
         
    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")

    
    
    if admin == "1":
        print('<p class="lead">All projects:</p>')
        q1 = """
        select prid, prname, p.description1, p.description2, p.description3,
        p.creator, p.date, count(*)
        from Project p
        join ProjectStudy using(prid)
        group by prid
        order by date desc, prname asc;
        """ # get prid, prname, description1,2,3, creator, date, study #. Admin = 1
        
        q2 = """
        select prid, prname, description1, description2, description3, creator, date, 0
        from Project left join ProjectStudy using(prid)
        where sid is NULL
        order by date desc, prname asc;
        """ # admin = 1 study = 0
        
    else:
        print('<p class="lead">All projects for user <b>%s</b>:</p>' % name)
        q1="""
        select prid, prname, p.description1, p.description2, p.description3, 
        creator, p.date, count(*)
        from Project p
        join ProjectStudy using(prid)
        where creator = "%s"
        group by prid
        order by date desc, prname asc;
        """ % uname # admin = 0 and uid
        
        q2 ="""
        select prid, prname, p.description1, p.description2, p.description3, 
        creator, p.date, 0
        from Project p
        left join ProjectStudy using(prid)
        where creator = "%s" and sid is NULL
        order by date desc, prname asc;
        """ % uname # admin = 0 and 
    
    res1 = runQuery(q1, user, passwd)
    res2 = runQuery(q2, user, passwd)
    
    if len(res1) > 0 or len(res2) > 0:
        print("""
        
        
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>Project name</th>
                     <th>Description1</th>
                     <th>Description2</th>
                     <th>Description3</th>
                     <th>Creator</th>
                     <th>Create date</th>
                     <th># Studies</th>
                   </tr></thead><tbody>"""
                   )
        n1 = len(res1)
        n2 = len(res2)
        for i in range(n1 + n2):
            if i < n1 and n1 > 0:
                row = res1[i]
            else:
                row = res2[i-n1-1]
            print('<tr>')
            for j in range(len(row)):
                if j == 0 or j == 1:
                    print("""<td>
                    <a href="./showstudy.py?prid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("</tr>")
        print("</tbody></table></br></br>")
    
    print("""
    <p class="lead">Add a new project:</p>
    
    <form class="form-horizontal" method="post" action="./showproject.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-project" class="col-sm-2 control-label">Project:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter project name" name="prname">
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-des1" class="col-sm-2 control-label">Description 1:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" name="description1">
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-des2" class="col-sm-2 control-label">Description 2:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" name="description2">
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-des3" class="col-sm-2 control-label">Description 3:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" name="description3">
          </div>
        </div>
      </div>
    <div>
    <input type="submit" value="Add" class="btn btn-lg btn-default">
    </div>
    </form>""")

    print("""
    <br/>
    <p class="lead">Delete a Project:</p>
    <form method="post" action="./showproject.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-project" class="col-sm-2 control-label" style="padding-top: 5px;">Project ID:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter project ID" name="prid">
          </div>
        </div>
      </div>
    <br/><br/>
    <div>
    <input type="submit" value="Remove" class="btn btn-lg btn-default">
    </div>
    </form>
    </div>
    <br/>
    """)

    ptail()
    
else:
    print("Location: login.py")
    print("Content-type: text/html\n")