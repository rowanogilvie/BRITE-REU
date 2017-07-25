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
                                 document.getElementById("eid").innerHTML = "";
                        }
                      }
                       
                          xmlhttp.open("GET","getstudyinproject.py?prid="+str,true);
                      xmlhttp.send();
                    }
                };

    function showexps(str) {
                      if (str == "") {
                        document.getElementById("eid").innerHTML = "";
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
                          document.getElementById("eid").innerHTML = xmlhttp.responseText;
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
                          document.getElementById("bedfiles").innerHTML = xmlhttp.responseText;
                          document.getElementById("eid").value = str;
                        }
                      }
                        
                          xmlhttp.open("GET","getbedinexperiment.py?eid="+str,true);
                      xmlhttp.send();
                    }
                };
    </script>
    <script>
    $(document).ready(function() {
        "use strict";
        $(document.getElementById("filter")).on('click', function() {
            var list = [];
            $(".input:checked").each(function() {
                var bed = $(this).parent().siblings().children().html();
               // window.alert(bed);
                list.push(bed);
            });
            var serialized_data=JSON.stringify(list);
            window.alert(serialized_data);
            var eid = document.getElementById("eid").value;
            $.get( "bedtools.py", {checkboxes:serialized_data, eid:eid})
            .done(function( data ) {
            window.alert( data );
            location.href='BEDfunctions.py?eid=%s';
           // window.location.href=data;
            });
        })});
        
    function getEID() {
    
        var exp = document.getElementbyId("eid");
        window.location.href='BEDfunctions.py?eid='+exp;
    }
    </script>
    
    """%eid)
    
#                 //var checkedValue = null; 
#             //var inputElements = document.getElementsByClassName('input');
#             //for(var i=0; inputElements[i]; ++i){
#               //  if(inputElements[i].checked){
#                 //    checkedValue = inputElements[i].value;
#                   //  var data = $(inputElements[i]).parent().siblings().children().html();
#                     //window.alert(data);
#                     //break;
#                // }
#            // }
#            // window.alert("this worked!");
#      
#      //   })});


    phead(name, admin)
    print("""<div class="container">""")
    
    print("""<div class="lead">
    <p class="well" align="center"><b>ROWANS TEST</b></p>
    </div>
     """)
    
    qProjects = """
    select prid, prname from Project
    where creator="%s"
    order by date desc, prname asc;
    """ % uname
    projects = runQuery(qProjects, user, passwd)
    print(""" 
    <div id="content" > 
    <form class="update-table-form" action='./BEDfunctions.py' method ='post'>
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
	  """)
    
    if eid:
        qExperiments = """
        select title
        from Experiment where eid="%s"
        """ % (eid)
        experiments = runQuery(qExperiments, user, passwd)
        print("""
      <b>Experiments: </b>
      <select name='eid' id="eid">
      """)
        for row in experiments:
            print("""<option value="%s" selected>%s</option>"""% (eid, row[0]))
        print("""</select>""")
    else:
        print("""
    	  <b>Experiments: </b>
    	  <select name='eid' id="eid";>
    	  <option>-- please select an experiment--</option>
    	  </select>
    	  </br>
    	  </br>
    	  """)
    #need to work on later
#     print("""
#         <script type="text/javascript">
#         if eid == None:
#             window.alert("ALERT!")
#                 
#         </script>
#                 """)
    print(""" 
    <div class="go-button">
    <p><input type="submit" value="Get BED files" class="btn btn-lg btn-default" id="submit" onclick='getEID()'></p>
    </div>
    </div>
    </form>
    """)



        
#     if eid:
#         print("""
#                     <script type="text/javascript">
#                     window.alert("File was successfully uploaded. Click OK to be directed to list of BED files.")
#                     location.href='BEDfunctions.py?eid=%s';
#                     </script>
#                     """%eid)

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
        <div id="bedfiles"><div class="datagrid"><table id="example" class="display" cellspacing="0" width="100%">
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

            print("""<td><input name ="input" class="input" type="checkbox"/></td>""")

            
            for j in range(len(row)):
                if j == 0 or j == 2:
                    print("""<td><a href="./bedinfo.py?bid=%s">%s</a></td>""" % (str(row[0]),str(row[j])))
                elif j == 1:
                    pass
                else:
                    print("<td>%s</td>" % str(row[j]))
            
            print("""<td><a href="%s">Download</a></td></tr>""" % row[1])
        print("</tbody>")
        print("</table></div></div></br></br>")
    nuname = form.getvalue("uname")
    nbid = form.getvalue("bid")
    
    print("""
    <p class="lead"><b>Bedtools Intersect:</b></p>
    <p><b style="color:red ! important">Note: You must be in a experiment to use this function!</b></p>
    <p>Please select two files using checkboxes</p>
    <p><input type="button" value="Intersect BED files" class="btn btn-lg btn-default" id="filter"></p>
   
    <br/>
    """)
    
    
#     <!--
# 
#         var inputs = document.getElementsByTagName('input');
#         for(var i=0; i < inputs.length; i++){
#             if(inputs[i].type == 'checkbox' && inputs[i].checked) {
#                 //print
#                 document.write(inputs[i].value);
#             }
#         }


#     -->
    
    print("""
        <br/>
        <p class="lead"><b>Copy the BEDfile:</b></p>
        <p><b style="color:red ! important">Note: You must be in a experiment to use this function!</b></p>
        <form method="post" action="./BEDcopy.py" enctype="multipart/form-data">
        <p>Please select one file using checkboxes</p>
        <input type="submit" value="copy" class="btn btn-lg btn-default>
        </form>
        
        """)
    
#     <label for="input-project" class="col-sm-2 control-label" style="padding-top: 5px;">Experiment title:</label>
#               <div class="col-sm-10">
#                                 <input class="form-control" type="text" placeholder="Please enter experiment" name="eid">
#</div>
    
    if nbid != None:
        q2 = """select wmid,cmid,name,location,description1,description2,description3,bedtoolcommand, stringency, source from BEDfile where bid = "%s";"""%bid
        q3 = """select bid from BEDfile order by bid DESC limit 1;"""
        q4 = """select eid from Experiment where title = "%s";"""%eid
        add_new = runQuery(q2,user,passwd)
        nbid = runQuery(q3,user,passwd)
        neid = runQuery(q4,user,passwd)
        name = add_new[0][2] + "_" + str(nbid)
        Copy(nbid,name, add_new[0][3], add_new[0][4], add_new[0][5], add_new[0][6], add_new[0][7], nuname, add_new[0][1], add_new[0][0],add_new[0][8], add_new[0][9],neid)
     
    ptail()
    

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
