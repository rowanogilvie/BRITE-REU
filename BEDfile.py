#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail, BEDintersect, BEDcopy

cgitb.enable()
#this is a test
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
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    db="group9"
    host="localhost"
    
    def runQuery(query, user, passwd):
        connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res
    def Copy(bid,name, location, des1, des2, des3, command, uname, cmid, wmid,stringency, source, eid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
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
    phead(name, admin)
    print("""<div class="container">""")
    
    #BEDintersect()
    print("""
    <p class="lead"><b>Bedtools Intersect:</b></p>
    <p><b style="color:red ! important">Note: You must be in a experiment to use this function!</b></p>
    <form method="post" action="./bedtools.py?eid=%s">
    File 1: <textarea name="f1" rows=10 cols=30 placeholder="e.g. Bcl6_fBcl6F-idr2-optimal_top3rd_.bed"></textarea>
    File 2: <textarea name="f2" rows=10 cols=30 placeholder="e.g. FOXA1_fFOXA1F-idr2-optimal_top3rd_.bed"></textarea>
    <p><input type="submit" value="Intersect BED files" class="btn btn-lg btn-default"></p>
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
        <div class="datagrid"><table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th></th>
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
                   </tr></thead><tbody>"""
                   )
        n1 = len(res1)
        for i in range(n1):
            row = res1[i]

            print("""<td><input type="checkbox"/></td>""")
            
            for j in range(len(row)):
                if j == 0 or j == 2:
                    print("""<td>
                    <a href="./bedinfo.py?bid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                elif j == 1:
                    pass
                else:
                    print("<td>%s</td>" % str(row[j]))
            
            print("""<td><a href="%s">Download</a></td></tr>""" % row[1])
        print("</tbody>")
        print("</table></div></br></br>")
    nuname = form.getvalue("uname")
    nbid = form.getvalue("bid")
    
    #BEDcopy()
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
        </div>
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
    ptail()
    

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
