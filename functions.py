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
        <link href="../../dapr_test/css/bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">
        
        <!-- footer -->
        <link href="../../dapr_test/css/sticky-footer.css" rel="stylesheet">
        
        <!-- Datatable -->
        <link rel="stylesheet" type="text/css" href="../../dapr_test/css/DataTables/datatables.min.css"/>
        
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
                    <li><a href="./BEDfile.py">View BED files</a></li>
                    <li><a href="./BEDfunctions.py">Perform BED functions</a></li>
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
    <link rel="stylesheet" href="../../dapr_test/css/sticky-footer.css" type="text/css" />
      <div class="container">
        <p class="text-muted">
        DASR version 2.1.0.
        <br/>
        <a title="Boston University" href="http://www.bu.edu/" target="_blank">Boston University.</a>
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
    
    <!-- script src="http://128.197.87.29/dapr_test/css/DataTables/DataTables-1.10.15/js"></script -->
    
    <!-- script src="../../dapr_test/css/DataTables/datatables.min.js"></script -->
    
    <script type="text/javascript" src="../../dapr_test/css/bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>

    <!--testing things below here rowan 6.21.2017 -->
    <!--responsive-->
    <script src="https://cdn.datatables.net/responsive/2.1.1/css/responsive.dataTables.min.css"></script>
    <script src="https://cdn.datatables.net/responsive/2.1.1/js/dataTables.responsive.min.js"></script>

    <!--select (not sure what this is doing)-->
    <script src="https://cdn.datatables.net/select/1.2.2/css/select.dataTables.min.css"></script>
    <script src="https://cdn.datatables.net/select/1.2.2/js/dataTables.select.min.js"></script>

    <!--buttons-->
    <script src="https://cdn.datatables.net/buttons/1.3.1/css/buttons.dataTables.min.css"></script>
    <script src="https://cdn.datatables.net/buttons/1.3.1/js/dataTables.buttons.min.js"></script>

    <!--autofill-->
    <script src="https://cdn.datatables.net/autofill/2.2.0/css/autoFill.dataTables.min.css"></script>
    <script src="https://cdn.datatables.net/autofill/2.2.0/js/dataTables.autoFill.min.js"></script>
    
    <!--fixed header-->
    <script src="https://cdn.datatables.net/fixedheader/3.1.2/css/fixedHeader.dataTables.min.css"></script>
    <script src="https://cdn.datatables.net/fixedheader/3.1.2/js/dataTables.fixedHeader.min.js"></script>
    
    </body>
    </html>
    """ % str(datetime.datetime.now())[:-7])
    
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

