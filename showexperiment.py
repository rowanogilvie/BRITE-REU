#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail
cgitb.enable()
"""
The following issues need to be addressed:
-add an experiment; no error thrown, data just isn't added
-remove an experiment; does something weird, unexplainable- no error thrown
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
    
    exp = form.getvalue("exname")
    sid2 = form.getvalue("stname")
    des1 = form.getvalue("description1")
    des2 = form.getvalue("description2")
    des3 = form.getvalue("description3")
    doe = form.getvalue("doe")
    
    sid = form.getvalue('sid')
    
    qsname = "select sname from Study where sid = '%s'" % sid
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    if exp == None:
        exp = ""
    if des1 == None:
        des1 = ""
    if des2 == None:
        des2 = ""
    if des3 == None:
        des3 = ""
        
    
    def addExp(exp, sid, des1, des2, des3, doe, uname, date):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query1 = """INSERT INTO Experiment (title, description1, description2, description3,
        exp_date, creator, create_date) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")
        ;""" % (exp, des1, des2, des3, doe, uname, date)
        
        cursor.execute(query1)
        connection.commit()
        
        qgeteid = """select eid from Experiment where title = "%s" """ % exp
        geteid = runQuery(qgeteid, user, passwd)
        
        eid = geteid[0][0]
        
        query2 = """insert into StudyExperiment (sid, eid) values ("%s", "%s")""" % (sid, eid)
        cursor.execute(query2)
        connection.commit()
        cursor.close()
        connection.close()
        print(query1)
        print(query2)
        
    def delExperiment(eid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query = """delete from Experiment where eid = ("%s");""" %(eid)
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
        
    if len(exp) != 0 and sid2 != None and doe!= None:
        try:
            datetime.datetime.strptime(doe, '%Y-%m-%d')
        except ValueError:
            print("Location: errordate.py")
            print("Content-type: text/html\n")
        else:
            addExp(exp, sid2, des1, des2, des3, doe, uname, str(datetime.date.today()))
            print("Location: showexperiment.py")

    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")
    
    

    if admin == "1" and sid == None:
        print('<p class="lead">All experiments:</p>')
        q1 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, count(*)
        from Experiment e
        join ExperimentBEDfile using(eid)
        group by eid
        order by create_date desc, title asc;
        """  # get eid, ename, description1,2,3, creator, expdate, createdate, exp#. Admin = 1

        q2 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, 0
        from Experiment e
        left join ExperimentBEDfile using(eid)
        where bid is NULL
        order by create_date desc, title asc;
        """
        
    elif admin == "1" and sid:
        sname = runQuery(qsname, user, passwd)[0][0]
        print('<p class="lead">All experiments in study <b>%s</b>:</p>' % sname)
        q1 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, count(*)
        from Experiment e
        join ExperimentBEDfile using(eid)
        join StudyExperiment using(eid)
        where sid = "%s"
        group by eid
        order by create_date desc, title asc;
        """ % sid
        
        q2 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, 0
        from Experiment e
        join StudyExperiment using(eid)
        left join ExperimentBEDfile using(eid)
        where sid = "%s" and bid is NULL
        order by create_date desc, title asc;
        """ % sid
    
    elif admin == "0" and sid == None:
        print('<p class="lead">All experiments:</p>')
        q1 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, count(*)
        from Experiment e
        join ExperimentBEDfile using(eid)
        where e.creator = "%s"
        group by eid
        order by create_date desc, title asc;
        """ % uname
        
        q2 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, 0
        from Experiment e
        left join ExperimentBEDfile using(eid)
        where e.creator = "%s" and bid is NULL
        order by create_date desc, title asc;
        """ % uname
        
    else:
        sname = runQuery(qsname, user, passwd)[0][0]
        print('<p class="lead">All experiments in study <b>%s</b>:</p>' % sname)
        q1 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, count(*)
        from Experiment e
        join ExperimentBEDfile using(eid)
        join StudyExperiment using(eid)
        where sid = "%s" and e.creator = "%s"
        group by eid
        order by create_date desc, title asc;
        """ % (sid, uname)
        
        q2 = """
        select eid, title, e.description1, e.description2, e.description3, 
        e.creator, exp_date, create_date, 0
        from Experiment e
        join StudyExperiment using(eid)
        left join ExperimentBEDfile using(eid)
        where sid = "%s" and e.creator = "%s" and bid is NULL
        order by create_date desc, title asc;
        """ % (sid, uname)
        
    res1 = runQuery(q1, user, passwd)
    res2 = runQuery(q2, user, passwd)
    
    if len(res1) > 0 or len(res2) > 0:
        print("""
        <table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>Experiment</th>
                     <th>Description1</th>
                     <th>Description2</th>
                     <th>Description3</th>
                     <th>Creator</th>
                     <th>Date of experiment</th>
                     <th>Create date</th>
                     <th># BED files</th>
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
                    <a href="./BEDfile.py?eid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("</tr>")
        print("</tbody></table></br></br>")
        
        
    print("""
    <p class="lead">Add a new experiment:</p>
    
    <form class="form-horizontal" method="post" action="./showexperiment.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-project" class="col-sm-2 control-label">Experiment:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter experiment name" name="exname">
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <div class="col-xs-8">
          <label for="selectstudy" class="col-sm-2 control-label">Study:</label>
          <div class="col-sm-10">
          <select class="form-control" name="stname">
            <option>-- Please select a study --</option>
      """)
    
    if admin == "1":
        getsts = """select sid, sname from Study"""
    else:
        getsts = """select sid, sname from Study
        where creator = "%s" """ % uname
    
    stnames = runQuery(getsts, user, passwd)
    for row in stnames:
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
    </br>
    <div>
    <p class="lead">Delete an Experiment:</p>
    <form method="post" action="./showexperiment.py" enctype="multipart/form-data">
      <div class="form-group">
        <div class="col-xs-8">
          <label for="input-study" class="col-sm-2 control-label" style="padding-top: 5px;">Experiment ID:</label>
          <div class="col-sm-10">
            <input class="form-control" type="text" placeholder="Please enter experiment ID" name="sid">
          </div>
        </div>
      </div>
    </br>
    </br>
    </br>
    <div>
    <input type="submit" value="Remove" class="btn btn-lg btn-default">
    </div>
    </form>
    </div>
    <br/>
    </div>
    </div>
    """)
    
    ptail()

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
