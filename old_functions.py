#!/usr/local/bin/python3.3

import http.cookies as Cookie
import os
import datetime


def get_cookies():
    # Create a cookie object
    cookie = Cookie.SimpleCookie()
    # Check for existing cookies
    if 'HTTP_COOKIE' in os.environ:
        # get cookie
        cookie.load(os.environ["HTTP_COOKIE"])
        try:
            uid = cookie["uid"].value
            if uid == "":
                cookie = None
                return cookie
        except:
            cookie = None
        else:
            cookie["uid"]["max-age"] = 60*60
            cookie["uname"]["max-age"] = 60*60
            cookie["pword"]["max-age"] = 60*60
            cookie["fname"]["max-age"] = 60*60
            cookie["lname"]["max-age"] = 60*60
            cookie["admin"]["max-age"] = 60*60
            cookie["appro"]["max-age"] = 60*60
            
    else:
        cookie = None
    return cookie

def phead(name, admin):
    ad = ""
    if admin == "1":
        ad = '<span style="color:red;">(admin)</span>'
      
  
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
        <link href="/dapr_test/css/bootstrap.min.css" rel="stylesheet">
        
        <!-- footer -->
        <link href="/dapr_test/css/sticky-footer.css" rel="stylesheet">
        
        <!-- Datatable -->
        <link rel="stylesheet" type="text/css" href="/students_17/Group9/css/DataTables/datatables.min.css"/>
        
      </head>
      
      <body>
        <nav class="navbar navbar-default navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="./index.py">DASR</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="./index.py">Home</a></li>
                
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Manage <span class="caret"></span></a>
                  <ul class="dropdown-menu">
                    <li><a href="./showproject.py">Project</a></li>
                    <li><a href="./showstudy.py">Study</a></li>
                    <li><a href="./showexperiment.py">Experiment</a></li>
                    <li role="separator" class="divider"></li>
                    <li><a href="./showplatform.py">Platform</a></li>
                    <li><a href="./showComMethod.py">Computational method</a></li>
                    <li><a href="./showWetMethod.py">Wet-lab method</a></li>
    """)
    if admin == "1":
        print("""
                    <li role="separator" class="divider"></li>
                    <li><a href="./showusers.py">User</a></li>
        """)
    print("""
                    
                  </ul>
                </li>
                
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">BEDtools <span class="caret"></span></a>
                  <ul class="dropdown-menu">
                    <li><a href="./BEDfile.py">Compare BED files</a></li>
                  </ul>
                </li>
                
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Upload <span class="caret"></span></a>
                  <ul class="dropdown-menu">
                    <li><a href="./upload_v0.1.py">Upload BED file</a></li>
                  </ul>
                </li>
                
                <li><a href="./help.py">Help</a></li>
                <li><a href="./about.py">About</a></li>
                
              </ul>
            
              <ul class="nav navbar-nav pull-right">
                
                <li><a href="#">%s%s</a></li>
                <li><a href="./logout.py">Log out</a></li>
              
              </ul>
            
            </div><!--/.nav-collapse -->
          </div>
        </nav>
    """ % (name, ad))

def ptmpbody():
    print("""
    <div class="container">
      <div class="page-header">
        <h1><div class="well">DASR (Database for the Analysis of Sequencing Reads)</div></h1>
        
      <h3>
      What is DASR?
      </h3>
      <div>
      Database for the Analysis of Sequencing Reads (DASR) is an online database for 
      the storage, output, query and analysis of
      <a href="https://genome.ucsc.edu/FAQ/FAQformat.html#format1">
      Browser Extensible Data (BED)</a>.
      </div>
      
      <h3>
      Purpose of the database?
      </h3>
      <div>
      <p>DASR was developed to facilitate data storage and analysis. Biologists can upload
      BED files to the database and identify overlapping regions of genomic features by
      the integrated utility
      <a href="http://bedtools.readthedocs.io/en/latest/">
      BEDtools</a>. These genomic features include transcription 
      factor (TF) binding sites, histone modifications, DNase hypersensitivity sites, 
      transcriptional (RNA) profiles, and other markings on a genome-wide basis.
      </div>
      
      <h3>
      Developers:
      </h3>
      <div>
      The database was developed by Akanksha Raju Khorgade, Junming Hu, Thomas Marsden,
      and Zhe Wang at Boston University as part of BF768 
      Biological Database Analysis, Spring 2017, G. Benson instructor. Faculty advisor:
      Prof. David Waxman.
      </div>
      <br/>
      <div>
      <p><b>Junming Hu</b></br>
      Bioinformatics Program at Boston University,</br>
      hjunming@bu.edu
      </br>
      </div>
      
      <div>
      <p><b>Akanksha Raju Khorgade</b></br>
      Bioinformatics Program at Boston University,</br>
      akankshk@bu.edu
      </br>
      </div>
      
      <div>
      <p><b>Thomas Marsden</b></br>
      Bioinformatics Program at Boston University,</br>
      tmarsden@bu.edu
      </br>
      </div>
      
      <div>
      <p><b>Zhe Wang</b></br>
      Bioinformatics Program at Boston University,</br>
      zhe@bu.edu
      </br>
      </div>
        
      </div>
    </div>
    """)
    
def ptail():
    print("""
    <footer class="footer">
      <div class="container">
        <p class="text-muted">
        DASR version 2.1.0.
        <br/>
        <a title="Boston University" href="http://www.bu.edu/">Boston University.</a>
          %s</p>
      </div>
    </footer>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        
    <script type="text/javascript" charset="utf-8">
          $(document).ready(function() {
          	$('#example').DataTable();
          } );
    </script>
    
    <script src="https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js"></script>
    
    <!-- script src="/students_17/Group9/css/DataTables/datatables.min.js"></script -->
    
    <script type="text/javascript" src="/students_17/Group9/css/bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>
    
    
    </body>
    </html>
    """ % str(datetime.datetime.now())[:-7])
