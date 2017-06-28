#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail

cgitb.enable()

cookie = get_cookies()

if cookie:
#     print(cookie)
#     fname = cookie["fname"].value
#     lname = cookie["lname"].value
#     name = " ".join((fname, lname))
#     admin = cookie["admin"].value
#     uid = cookie["uid"].value
#     uname = cookie["uname"].value
    
    
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
    def Copy(bid,name, location, des1, des2, des3, command, uname, cmid, wmid,stringency, source,eid):
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
   # phead(name, admin)
    print("""<div class="container">""")
    
    #BEDintersect()
    #BEDcopy()
    
    
   # ptail()
    

else:
    print("Location: login.py")
    print("Content-type: text/html\n")



def BEDintersect(): 
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
def BEDcopy():    
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
