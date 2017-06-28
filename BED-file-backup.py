#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
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
    
    
    form = cgi.FieldStorage()
    
    eid = form.getvalue('eid')
    
    qexname = "select title from Experiment where eid = '%s'" % eid
    
    user="d4prdb17"
    passwd="d4prp455"
    
    def runQuery(query, user, passwd):
        connection = pymysql.connect(host="localhost",db="group9",user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res
    def Copy(bid,name, location, des1, des2, des3, command, uname, cmid, wmid,stringency, source,eid):
        connection = pymysql.connect(host="localhost", user="d4prdb17", db="group9", passwd="d4prp455")
        cursor = connection.cursor()
        query1 = """INSERT INTO BEDfile (bid,name, location, description1, description2, description3, 
        upload_date, bedtoolcommand, uploader, cmid, wmid,stringency, source)
                    VALUES (%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, %s,%s,%s)
                    """%(int(bid),name, location, des1, des2, des3, str(datetime.datetime.now())[:-7],
                         command, uname, int(cmid), int(wmid),stringency, source)
        query2 = """INSERT INTO ExperimentBEDfile (eid,bid) VALUES(%s,%s)"""%(bid,eid)
        cursor.execute(query1)
        cursor.execute(query2)
        connection.commit()
        cursor.close()
        connection.close()
    
    print("Content-type: text/html\n")
    print("""
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
    	<title>DASR</title>
    	<meta charset="utf-8"/>
    	<link rel="stylesheet" href="../../dapr_test/css/index.css" type="text/css" />
       <link rel="stylesheet" href="../../dapr_test/css/table.css" type="text/css" />
    	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    
    <body class = "body">
    	<header class = "mainheader">
         <a href = "http://128.197.87.29/cgi-bin/dapr_test/index.py">
    	    <img src="https://bioed.bu.edu/students_17/Group9/dasr_logo.png" /></a>
         <div class="alignright">
         <br/>
         <ul>
         <li>Logged in as <a href=#>%s</a></li>
         <br/>
         """ % name)
    if admin == "1":
        print('<li style="float: right; color:red ! important;">admin</li><br/>')
    
    print("""
         
         <li style="float: right;"><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/logout.py">Log out</a></li>
         </ul>
         </div>
    		<nav><ul>
    			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/index.py">Home</a></li>
    			<li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/help.py">Help</a></li>
                <li><a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/about.py">About</a></li>
    		</ul></nav>
    	</header>
    
      <div class="colmask blogstyle">                            
              <div class="col1">					
              <h3>Manage</h3>
    			<ul>
    				<li><a class="" title="Manage Experiments" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showexperiment.py">Manage Experiments</a></li>
    				<li><a class="" title="Manage Studies" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showstudy.py">Manage Studies</a></li>
    				<li><a class="" title="Manage Projects"
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showproject.py">Manage Projects</a></li>
    				<li><a class="" title="Manage Platforms" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showplatform.py">Manage Platforms</a></li>
    				<li><a class="" title="Manage Users" href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showusers.py">Manage Users</a></li>
                    <li><a class="" title="Manage Computational Method"
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showComMethod.py">Manage Computational Method</a></li>
                    <li><a class="" title="Manage Wetlab Method"
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/showWetMethod.py">Manage Wetlab Method</a></li>

    			</ul>
            </div>
    
            <div class="col2">
              <h3>BEDTools</h3>
    			<ul>
    				<li><a class="" title="Compare BEDFiles and store them in BED format in database" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/BEDfile.py">CompareBEDFiles</a></li>
    			</ul>
            </div>
     
            <div class="col3">
            <h3>Upload</h3>
    			<ul>
    				<li><a class="" title="Upload BED file to a experiment" 
        href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/upload_v0.1.py">Upload BEDfile</a></li>
    			</ul>	
            </div>
    </div>
    </br>
    """)
    
    print("""
    <p><b>Bedtools Intersect:</b></p>
    <p><b style="color:red ! important">Note: You must be in a experiment to use this function!</b></p>
    <form method="post" action="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/bedtools.py?eid=%s">
    File 1: <textarea name="f1" rows=10 cols=30 placeholder="e.g. Bcl6_fBcl6F-idr2-optimal_top3rd_.bed"></textarea>
    File 2: <textarea name="f2" rows=10 cols=30 placeholder="e.g. FOXA1_fFOXA1F-idr2-optimal_top3rd_.bed"></textarea>
    <p><input type="submit" value="Intersect BED files"/></p>
    </form>
    <br/>
    """ % eid)
    

    if admin == "1" and eid == None:
        print('<p><font size="4">All BED files:</font></p>')
        q1 = """
        select bid, location, b.name, w.name, c.name, description1, description2, 
        description3, uploader, upload_date, bedtoolcommand
        from BEDfile b join WetlabMethod w using(wmid)
        join ComputationalMethod c using(cmid)
        order by upload_date desc, b.name asc;
        """
    elif admin == "1" and eid:
        exname = runQuery(qexname, user, passwd)[0][0]
        print('<p><font size="4">All BED files in experiment <b>%s</b>:</font></p>' % exname)
        q1 = """
        select b.bid, location, b.name, w.name, c.name, description1, description2, 
        description3, uploader, upload_date, bedtoolcommand
        from BEDfile b join ExperimentBEDfile using(bid)
        join WetlabMethod w using(wmid)
        join ComputationalMethod c using(cmid)
        where eid = "%s"
        order by upload_date desc, b.name asc;
        """ % eid
    elif admin == "0" and eid == None:
        print('<p><font size="4">All BED files:</font></p>')
        q1 = """
        select bid, location, b.name, w.name, c.name, description1, description2, 
        description3, uploader, upload_date, bedtoolcommand
        from BEDfile b join WetlabMethod w using(wmid)
        join ComputationalMethod c using(cmid)
        where uploader = "%s"
        order by upload_date desc, b.name asc;
        """ % uname
    else:
        exname = runQuery(qexname, user, passwd)[0][0]
        print('<p><font size="4">All BED files in experiment <b>%s</b>:</font></p>' % exname)
        q1 = """
        select b.bid, location, b.name, w.name, c.name, description1, description2, 
        description3, uploader, upload_date, bedtoolcommand
        from BEDfile b join ExperimentBEDfile using(bid)
        join WetlabMethod w using(wmid)
        join ComputationalMethod c using(cmid)
        where eid = "%s" and uploader = "%s"
        order by upload_date desc, b.name asc;
        """ % (eid,uname)

    res1 = runQuery(q1, user, passwd)
    
    if len(res1) > 0:
        print("""
        <div class="datagrid"><table border=1>
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>BED file</th>
                     <th>Wetlab method</th>
                     <th>Computational method</th>
                     <th>Info1</th>
                     <th>Info2</th>
                     <th>Info3</th>
                     <th>Uploader</th>
                     <th>Upload time</th>
                     <th>bedtools command</th>
                     <th>Download</th>
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
            row = res1[i]

            if i % 2 == 1:
                print('<tbody><tr class="alt">')
            else:
                print('<tbody><tr>')
            for j in range(len(row)):
                if j == 0 or j == 2:
                    print("""<td>
                    <a href="https://bioed.bu.edu/cgi-bin/students_17/Group9/BEDDB/bedinfo.py?bid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                elif j == 1:
                    pass
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("""<td><a href="%s">Download</a></td>""" % row[1])
            print("</tr></tbody>")
        print("</table></div></br></br>")
    nuname = form.getvalue("uname")
    nbid = form.getvalue("bid")
    print("""
        <br/>
        <p class="lead"><b>Copy the BEDfile:</b></p>
        <form method="post" action="./BED.py" enctype="multipart/form-data">
          <div class="form-group">
            <div class="col-xs-8">
              <label for="input-project" class="col-sm-2 control-label" style="padding-top: 5px;">BEDfile ID:</label>
              <div class="col-sm-10">
                <input class="form-control" type="text" placeholder="Please enter BEDfile ID" name="bid">
              </div>
              </br>
              <label for="input-project" class="col-sm-2 control-label" style="padding-top: 5px;">Username:</label>
              <div class="col-sm-10">
                                <input class="form-control" type="text" placeholder="Please enter username" name="uname">
              </div>
              </br>
              <label for="input-project" class="col-sm-2 control-label" style="padding-top: 5px;">Experiment title:</label>
              <div class="col-sm-10">
                                <input class="form-control" type="text" placeholder="Please enter experiment" name="exp">
              </div>
            </div>
          </div>
        <br/><br/>
        <div>
        <input type="submit" value="copy" class="btn btn-lg btn-default">
        </div>
        </form>
        </div>
        <br/>
        """)
    if nbid != None:
        q2 = """select wmid,cmid,name,location,description1,description2,description3,bedtoolcommand, stringency, source from BEDfile where bid = "%s";"""%bid
        q3 = """select bid from BEDfile order by bid DESC limit 1;"""
        q4 = """select eid from Experiment where title = "%s";"""%exp
        add_new = runQuery(q2,user,passwd)
        nbid = runQuery(q3,user,passwd)
        neid = runQuery(q4,user,passwd)
        name = add_new[0][2] + "_" + str(nbid)
        Copy(nbid,name, add_new[0][3], add_new[0][4], add_new[0][5], add_new[0][6], add_new[0][7], nuname, add_new[0][1], add_new[0][0],add_new[0][8], add_new[0][9],neid)

    print("""

        </br>
        </br>
        	<div class="footer">
                    <ul>
                        <li><a title="Boston University" href="http://www.bu.edu/">Boston University</a></li>
                        <li>DASR version 2.0.0.</li>
                        <li>%s</li>
                    </ul>  
            </div>
        </body>
        </html>
        """ % str(datetime.datetime.now())[:-7])

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
