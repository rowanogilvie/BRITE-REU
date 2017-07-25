#!/usr/local/bin/python3.3
import cgi
import cgitb
import pymysql
import datetime
from functions import get_cookies, phead, ptail
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
    
    bid = form.getvalue('bid')
    
    q1 = """
    select name, location from BEDfile where bid = "%s";
    """ % bid
    
    #reduce redundancy
    user="d4prdb17"
    passwd="d4prp455"
    host="localhost"
    db="group9"
    
    def runQuery(query, user, passwd):
        connection = pymysql.connect(host=host,db=db,user=user,passwd=passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res

    def read_file(location):
        res = []
        with open(location) as f:
            for i in f:
                i = i.split("\t")
                res.append(int(i[2]) - int(i[1]))
        return res
    
    def clean_lengths(results):
        if results:
            res = ""
            for i in results:
                res += "["+str(i)+"],"
            res = res[:-1] + "]);"
        else:
            res = None    
        return res

    print("Content-type: text/html\n")
    phead(name, admin)
    print("""<div class="container">""")
    
    if admin == "1":
        print('<li style="float: right; color:red ! important;">admin</li><br/>')
    
    

    if bid != None:
        res = runQuery(q1, user, passwd)
        filename = res[0][0]   
        feature_lengths = read_file("/var/www/"+res[0][1])
        cl_lengths = clean_lengths(feature_lengths)

        print("""
        
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load("current", {packages:["corechart"]});
              google.charts.setOnLoadCallback(drawChart);
              function drawChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Length'],
                  """)

        if cl_lengths:
            print(cl_lengths)
        else:
            print("]);")
        
        print(
        """
                var options = {
                  title: 'Histogram of the feature lengths in %s.bed',
                  legend: { position: 'none' },
                  hAxis: {title: 'Feature lengths',
                  titleTextStyle:{fontSize: 20}
                  },
                  vAxis: {title: 'Frequency',
                   titleTextStyle:{fontSize: 20}
                   }
                };
        
                var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
                chart.draw(data, options);
              }
            </script>
        
        
            <div id="chart_div" style="width: 900px; height: 500px;"></div>
        """ % filename)

    ptail()

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
