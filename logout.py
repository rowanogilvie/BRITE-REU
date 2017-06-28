#!/usr/local/bin/python3.3
import cgi
import cgitb
import os
import http.cookies as Cookie

cgitb.enable()
cookie = Cookie.SimpleCookie()

if 'HTTP_COOKIE' in os.environ:
    # get cookie
    cookie.load(os.environ["HTTP_COOKIE"])
    try:
        uid = cookie["uid"].value
    except:
        cookie["uid"] = ""
        cookie["uid"] = ""
        cookie["uname"] = ""
        cookie["pword"] = ""
        cookie["fname"] = ""
        cookie["lname"] = ""
        cookie["admin"] = ""
        cookie["appro"] = ""
    else:
        cookie["uid"] = ""
        cookie["uid"] = ""
        cookie["uname"] = ""
        cookie["pword"] = ""
        cookie["fname"] = ""
        cookie["lname"] = ""
        cookie["admin"] = ""
        cookie["appro"] = ""
        
else:
    cookie["uid"] = ""
    cookie["uid"] = ""
    cookie["uname"] = ""
    cookie["pword"] = ""
    cookie["fname"] = ""
    cookie["lname"] = ""
    cookie["admin"] = ""
    cookie["appro"] = ""

print(cookie)

print("Location: login.py")

print("Content-type: text/html\n")

