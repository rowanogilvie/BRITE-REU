#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail
cgitb.enable()
"""
The following issues need to be addressed:
-remove study
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
    
    newst = form.getvalue("stname")
    plid = form.getvalue("plname")
    prid2 = form.getvalue("prname")
    des1 = form.getvalue("description1")
    des2 = form.getvalue("description2")
    des3 = form.getvalue("description3")
    study_to_delete = form.getvalue("study_to_delete")
    
    prid = form.getvalue('prid')
    
    qprname = "select prname from Project where prid = '%s'" % prid
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if newst == None:
        newst = ""
    if plid == None:
        plid = ""
    if des1 == None:
        des1 = ""
    if des2 == None:
        des2 = ""
    if des3 == None:
        des3 = ""
    
    
    def addStudy(stname, plid, prid, des1, des2, des3, uname, date):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query1 = """INSERT INTO Study (sname, plid, description1, description2, description3,
        creator, date) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")
        ;""" % (stname, plid, des1, des2, des3, uname, date)
        
        cursor.execute(query1)
        connection.commit()
        
        qgetsid = """select sid from Study where sname = "%s" """ % stname
        getsid = runQuery(qgetsid, user, passwd)

        sid = getsid[0][0]

        query2 = """insert into ProjectStudy (prid, sid) values ("%s", "%s")""" % (prid, sid)
        cursor.execute(query2)
        connection.commit()
        cursor.close()
        connection.close()
        
    def delStudy(plid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """delete from Study where sid = ("%s");""" %(plid)
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
        
    if len(newst) != 0 and len(plid) != 0 and prid2 != None:
        addStudy(newst, plid, prid2, des1, des2, des3, uname, str(datetime.date.today()))
        print("Location: showstudy.py")
    elif study_to_delete != None:
        delStudy(study_to_delete)
        
        
    
        
    

    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")
    

    if admin == "1" and prid == None:
        print('<p class="lead">All studies:</p>')
        q1 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, count(*)
        from Study s join Platform using(plid)
        join StudyExperiment using(sid)
        group by sid
        order by s.date desc, sname asc;
        """  # get sid, sname, plname, description1,2,3, creator, date, exp#. Admin = 1


        q2 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, 0
        from Study s join Platform using(plid)
        left join StudyExperiment using(sid)
        where eid is NULL
        order by date desc, sname asc;
        """ # admin = 1 exp = 0
    elif admin == "1" and prid:
        prname = runQuery(qprname, user, passwd)[0][0]
        print('<p class="lead">All studies in project <b>%s</b>:</p>' % prname)
        q1 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, count(*)
        from Study s join Platform using(plid)
        join StudyExperiment using(sid)
        join ProjectStudy using(sid)
        where prid = "%s"
        group by sid
        order by s.date desc, sname asc;
        """ % prid
        
        q2 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, 0
        from Study s join Platform using(plid)
        join ProjectStudy using(sid)
        left join StudyExperiment using(sid)
        where eid is NULL and prid = "%s"
        order by date desc, sname asc;
        """ % prid
        
    elif admin == "0" and prid == None:
        print('<p class="lead">All studies:</p>')
        q1 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, count(*)
        from Study s join Platform using(plid)
        join StudyExperiment using(sid)
        where s.creator = "%s"
        group by sid
        order by s.date desc, sname asc;
        """ % uname
        
        q2 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, 0
        from Study s join Platform using(plid)
        left join StudyExperiment using(sid)
        where eid is NULL and s.creator = "%s"
        order by date desc, sname asc;
        """ % uname
    else:
        prname = runQuery(qprname, user, passwd)[0][0]
        print('<p class="lead">All studies in project <b>%s</b>:</p>' % prname)
        q1 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, count(*)
        from Study s join Platform using(plid)
        join StudyExperiment using(sid)
        join ProjectStudy using(sid)
        where s.creator = "%s" and prid="%s"
        group by sid
        order by s.date desc, sname asc;
        """ % (uname, prid)
        
        q2 = """
        select sid, sname, plname, s.description1, s.description2, s.description3, s.creator, s.date, 0
        from Study s join Platform using(plid)
        join ProjectStudy using(sid)
        left join StudyExperiment using(sid)
        where s.creator = "%s" and prid="%s" and eid is NULL
        order by s.date desc, sname asc;
        """ % (uname, prid)
    
    res1 = runQuery(q1, user, passwd)
    res2 = runQuery(q2, user, passwd)

    if len(res1) > 0 or len(res2) > 0:
        print("""
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>Study</th>
                     <th>Platform</th>
                     <th>Description1</th>
                     <th>Description2</th>
                     <th>Description3</th>
                     <th>Creator</th>
                     <th>Create date</th>
                     <th># experiments</th>
                   </tr></thead><tbody>"""
                   )
        n1 = len(res1)
        n2 = len(res2)
        for i in range(n1 + n2):
            if i < n1 and n1 > 0:
                row = res1[i]
            else:
                row = res2[i-n1-1]
            print("<tr>")
            for j in range(len(row)):
                if j == 0 or j == 1:
                    print("""<td>
                    <a href="./showexperiment.py?sid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("</tr>")
        print("</tbody></table></br></br>")
    
    print("""
    <p class="lead">Add a new study:</p>
    
    <form class="form-horizontal" method="post" action="./showstudy.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-project" class="col-sm-2 control-label">Study:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter study name" name="stname">
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <div class="col-xs-8">
          <label for="selectproject" class="col-sm-2 control-label">Project:</label>
          <div class="col-sm-10">
          <select class="form-control" name="prname">
            <option>-- Please select a project --</option>
      """)
    
    if admin == "1":
        getprs = """select prid, prname from Project"""
    else:
        getprs = """select prid, prname from Project
        where creator = "%s" """ % uname
    prnames = runQuery(getprs, user, passwd)
    for row in prnames:
        print("""<option value="%s">%s</option>""" % (row[0], row[1]))
        
    print("""
          </select>
          </div>
        </div>
      </div>
    """)
    
    print("""
      <div class="form-group">
          <div class="col-xs-8">
            <label for="selectplatform" class="col-sm-2 control-label">Platform:</label>
            <div class="col-sm-10">
            <select class="form-control" name="plname">
              <option>-- Please select a platform --</option>
        """)
    
    getpls = """select plid, plname from Platform"""
    plnames = runQuery(getpls, user, passwd)
    for row in plnames:
        print("""<option value="%s">%s</option>""" % (row[0], row[1]))
        
    print("""
          </select>
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
    </form>
    <br/>
    """)
    print("""
    <br/>
    <p class="lead">Delete a Study:</p>
    <form class="form-horizontal" method="post" action="./showstudy.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-study" class="col-sm-2 control-label" style="padding-top: 5px;">Study ID:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter study ID" name="study_to_delete">
          </div>
        </div>
      </div>
    </br>
    <div>
    <input type="submit" value="Remove" class="btn btn-lg btn-default">
    </div>
    </form>
    </div>
    </div>
    <br/>
    """)
    
    
    ptail()

else:
    print("Location: login.py")
    print("Content-type: text/html\n")