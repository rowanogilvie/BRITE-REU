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
    print("""
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js">
    </script>
    <script>
    function showstudies(str) {
                      if (str == "") {
                        document.getElementById("study").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("study").innerHTML = xmlhttp.responseText;
                                 document.getElementById("exp").innerHTML = "";
                        }
                      }
                       
                          xmlhttp.open("GET","getstudyinproject.py?prid="+str,true);
                      xmlhttp.send();
                    }
                };

    function showexps(str) {
                      if (str == "") {
                        document.getElementById("exp").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("exp").innerHTML = xmlhttp.responseText;
                        }
                      }
                       
                          xmlhttp.open("GET","getexperimentinstudy.py?sid="+str,true);
                      xmlhttp.send();
                    }
                };

    function showbeds(str) {
                      if (str == "") {
                        document.getElementById("bed").innerHTML = "";
                        return;
                        }
                  else {
                        if (window.XMLHttpRequest) {
                          xmlhttp = new XMLHttpRequest();
                      } else {
                      alert("Your browser is bad and you should feel bad!");
                    }
                       
                      xmlhttp.onreadystatechange = function() {
                      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                          document.getElementById("bed").innerHTML = xmlhttp.responseText;
                        }
                      }
                       
                          xmlhttp.open("GET","getbedinexperiment.py?eid="+str,true);
                      xmlhttp.send();
                    }
                };
  
   
    </script>
    """)
#the following code does not work- in progress     
#       function updateTable(eid) {
#                         if (eid == None) {
#                             <p class="message" style="color:red ! important;"><b>Something went wrong! Missing experiment ID, please be sure you have selected an experiment.</b></p>
#                         }
#                         else {
#                         <p>it worked</p>
#     };
    phead(name, admin)
    print("""<div class="container">""")
    
    print("""
    <p class="lead"><b>ROWANS TEST</b></p>
     """)
    
    qProjects = """
    select prid, prname from Project
    where creator="%s"
    order by date desc, prname asc;
    """ % uname
    projects = runQuery(qProjects, user, passwd)
    print(""" 
    <div id="content" > 
    <form class="update-table-form" action='http://128.197.87.29/cgi-bin/dapr_test/BEDfunctions.py' method ='post'>
    <b>Project: </b><select name='project' id="project" onchange="showstudies(this.value)";>
                     <option>-- please select a project-- </option>
                     
                     """)
    for row in projects:
          print("""     <option value="%s">%s</option>""" % (row[0], row[1]))
    print("""</select>
    </br>
    </br>
    <b>Studies: </b>
            <select name='study' id="study" onchange="showexps(this.value)";>
            <option>-- please select a study-- </option>
            </select>
            
            </br>
                  </br>
                  <b>Experiments: </b>
                  <select name='exp' id="exp" onchange="showbeds(this.value)";>
                  <option>-- please select a experiment--</option>
                  </select>
                  </br>
                  </br>
                  
        <div class="go-button">
        <p><input type="submit" value="Get BED files" class="btn btn-lg btn-default" id="submit">
        <!--<select name="submit" id="eid" onchange="updateTable(this.value);></select>-->
        </p>
        </div>
        </div>
        </form>
            
          """)
    """
    need to add some javascript for a button "go" that on click it will update the table of files
    """
          
#     print("""
#     <p><b style="color:red ! important">Note: You must be in a experiment to use this function!</b></p>
#     <form method="post" action="./bedtools.py?eid=%s">
#     File 1: <textarea name="f1" rows=10 cols=30 placeholder="e.g. Bcl6_fBcl6F-idr2-optimal_top3rd_.bed"></textarea>
#     File 2: <textarea name="f2" rows=10 cols=30 placeholder="e.g. FOXA1_fFOXA1F-idr2-optimal_top3rd_.bed"></textarea>
#     <p><input type="submit" value="Intersect BED files" class="btn btn-lg btn-default"></p>
#     </form>
#     <br/>
#     """ % eid)

        

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
                   </tr></thead>"""
                   )
        n1 = len(res1)
        for i in range(n1):
            row = res1[i]

            if i % 2 == 1:
                print('<tbody><tr class="alt">')
            else:
                print('<tbody><tr>')
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
            print("""<td><a href="%s">Download</a></td>""" % row[1])
            print("</tr></tbody>")
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
