#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
from subprocess import call
import datetime
from functions import get_cookies, phead, ptail
cgitb.enable()
"""
The following issues need to be addressed:
-location of bed files 
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
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    getcmid = """
    select cmid from ComputationalMethod
    where name ="bedtools intersect";
    """
    
    getwmid = """
    select wmid from WetlabMethod
    where name ="bedtools intersect";
    """

    def runQuery(query, user, passwd):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res
    
    def insert_intersect_bed(name, location, command, uname):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query1 = """INSERT INTO BEDfile (name, location,
        upload_date, bedtoolcommand, uploader, cmid, wmid)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");
                    """%(name, location, str(datetime.datetime.now())[:-7],
                         command, uname, runQuery(getcmid, user, passwd)[0][0],
                         runQuery(getwmid, user, passwd)[0][0])
        cursor.execute(query1)
        connection.commit()
        cursor.close()
        connection.close()
    
    def update_exp(bid,eid,uid):
        connection = pymysql.connect(host=host, user=user, db=db, passwd=passwd)
        cursor = connection.cursor()
        query2 = """INSERT INTO ExperimentBEDfile(eid,bid)
              VALUES (%s,%s);"""%(eid,bid)
        query5 = """ INSERT INTO UserBEDfile (uid, bid)
              VALUES (%s, %s)"""%(uid, bid)
        cursor.execute(query2)
        cursor.execute(query5)
        connection.commit()
        cursor.close()
        connection.close()
    
    dire = "/var/www/dapr_test/bedfiles/"
    
    f1 = form.getvalue("f1")
    f2 = form.getvalue("f2")
    eid = form.getvalue("eid")
    
    if f1 and f2 and eid:
        bedname = "Intersection_of_"+f1[:-4]+"_and_"+f2[:-4]
        locpre = "/students_17/Group9/bedfiles/"
        loc = locpre+bedname+".bed"
        
        getbid = """
        select bid from BEDfile
        where name = "%s"
        """ % bedname
        
        getename = """
        select title from Experiment
        where eid = "%s"
        """ % eid
        
        ename = runQuery(getename, user, passwd)[0][0]
        command = "bedtools intersect -a " + f1 + ".bed " + "-b " + f2 + ".bed"
        
        with open(dire+"Intersection_of_"+f1[:-4]+"_and_"+f2[:-4]+".bed", "w") as f:
            call(["bedtools", "intersect", "-a", dire+f1,
              "-b",  dire+f2], stdout=f)
        
        insert_intersect_bed(bedname, loc, command, uname)
        bid = runQuery(getbid, user, passwd)[0][0]
        update_exp(bid, eid, uid)
        
        print("Content-type: text/html\n")
        print("""
        <p><b>Generated BED file %s in experiment %s</b></p>
        """ % (bedname, ename))
    
    else:
        print("Content-type: text/html\n")
        print("""
        <p><b>Invalid inputs! No file was generated!</b></p>
        """)

else:
    print("Location: login.py")
    print("Content-type: text/html\n")


