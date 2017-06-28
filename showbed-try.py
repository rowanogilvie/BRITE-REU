#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies

cgitb.enable()
#unsure of purpose
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
    
    print("Content-type: text/html\n")
    print("""
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
    	<title>DASR</title>
    	<meta charset="utf-8"/>
    	<link rel="stylesheet" href="../../dapr_test/css/index.css" type="text/css" />
     <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/bs-3.3.7/jq-2.2.4/dt-1.10.15/af-2.2.0/b-1.3.1/b-colvis-1.3.1/b-flash-1.3.1/b-html5-1.3.1/b-print-1.3.1/r-2.1.1/sc-1.4.2/se-1.2.2/datatables.min.css"/>
 
<script type="text/javascript" src="https://cdn.datatables.net/v/bs-3.3.7/jq-2.2.4/dt-1.10.15/af-2.2.0/b-1.3.1/b-colvis-1.3.1/b-flash-1.3.1/b-html5-1.3.1/b-print-1.3.1/r-2.1.1/sc-1.4.2/se-1.2.2/datatables.min.js"></script>

		<script type="text/javascript" charset="utf-8">
			$(document).ready(function() {
				$('#example').DataTable();
			} );
		</script>
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
         
         <li style="float: right;"><a href="http://128.197.87.29/cgi-bin/dapr_test/logout.py">Log out</a></li>
         </ul>
         </div>
    		<nav><ul>
    			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/index.py">Home</a></li>
    			<li><a href="http://128.197.87.29/cgi-bin/dapr_test/help.py">Help</a></li>
                <li><a href="http://128.197.87.29/cgi-bin/dapr_test/about.py">About</a></li>
    		</ul></nav>
    	</header>
    
      <div class="colmask blogstyle">                            
              <div class="col1">					
              <h3>Manage</h3>
    			<ul>
    				<li><a class="" title="Manage Experiments" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showexperiment.py">Manage Experiments</a></li>
    				<li><a class="" title="Manage Studies" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showstudy.py">Manage Studies</a></li>
    				<li><a class="" title="Manage Projects"
        href="http://128.197.87.29/cgi-bin/dapr_test/showproject.py">Manage Projects</a></li>
    				<li><a class="" title="Manage Platforms" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showplatform.py">Manage Platforms</a></li>
    				<li><a class="" title="Manage Users" href="http://128.197.87.29/cgi-bin/dapr_test/showusers.py">Manage Users</a></li>
                    <li><a class="" title="Manage Computational Method"
        href="http://128.197.87.29/cgi-bin/dapr_test/showComMethod.py">Manage Computational Method</a></li>
                    <li><a class="" title="Manage Wetlab Method"
        href="http://128.197.87.29/cgi-bin/dapr_test/showWetMethod.py">Manage Wetlab Method</a></li>

    			</ul>
            </div>
    
            <div class="col2">
              <h3>BEDTools</h3>
    			<ul>
    				<li><a class="" title="Compare BEDFiles and store them in BED format in database" 
        href="http://128.197.87.29/cgi-bin/dapr_test/BEDfile.py">CompareBEDFiles</a></li>
            <li><a class="" title="Show BED file" 
        href="http://128.197.87.29/cgi-bin/dapr_test/showBED.py">Show BED Files</a></li>
    			</ul>
            </div>
     
            <div class="col3">
            <h3>Upload</h3>
    			<ul>
    				<li><a class="" title="Upload BED file to a experiment" 
        href="http://128.197.87.29/cgi-bin/dapr_test/upload_v0.1.py">Upload BEDfile</a></li>
    			</ul>	
            </div>
    </div>
    </br>
    """)

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
        <div class="container">
<table id="example" class="display" cellspacing="0" width="100%">
          <thead>
                 <tr>
                     <th>ID</th>
                     <th>BED file</th>
                     <th>Wetlab method</th>
                     <th>Computational method</th>
					 <th>Tissue</th>
                     <th>Descriptor1</th>
                     <th>Descriptor2</th>
                     <th>Descriptor3</th>
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
                    <a href="http://128.197.87.29/cgi-bin/dapr_test/bedinfo.py?bid=%s">
                    %s</a></td>""" % (str(row[0]),str(row[j])))
                elif j == 1:
                    pass
                else:
                    print("<td>%s</td>" % str(row[j]))
            print("""<td><a href="%s">Download</a></td>""" % row[1])
            print("</tr></tbody>")
        print("</table></div></br></br>")

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
		<script type="text/javascript">
	// For demo to fit into DataTables site builder...
	$('#example')
		.removeClass( 'display' )
		.addClass('table table-striped table-bordered');
</script>
    </body>
    </html>
    """ % str(datetime.datetime.now())[:-7])

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
