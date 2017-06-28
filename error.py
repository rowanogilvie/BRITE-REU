#!/usr/local/bin/python3.3
import cgi
import cgitb
import datetime
from functions import get_cookies, phead, ptail, ptmpbody
cgitb.enable()

cookie = get_cookies()
if cookie:
    print(cookie)
    fname = cookie["fname"].value
    lname = cookie["lname"].value
    name = " ".join((fname, lname))
    admin = cookie["admin"].value
    print("Content-type: text/html\n")
    print("""<h1>You are logged in- page does not exist. Please log out to reset password</h1>""")
    

else:
    print("""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="icon" href="../../favicon.ico">
        
        
        <title>DASR: Database for the Analysis of Sequencing Reads</title>
        
        <!-- Bootstrap core CSS -->
        <link href="../../dapr_test/css/bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">
        
        <!-- footer -->
        <link href="../../dapr_test/css/sticky-footer.css" rel="stylesheet">
        
        <!-- Datatable -->
        <link rel="stylesheet" type="text/css" href="../../dapr_test/css/DataTables/datatables.min.css"/>
        
      </head>
      
      <body>
          <div class="container">
              <div class="page-header">
              <h1 class="well">Reset Password *PAGE UNDER CONSTRUCTION*</h1>
              </div>
              <h3>Please see your admin to reset your password</h3>
            </div>
      </body>
      """)
    ptail()


