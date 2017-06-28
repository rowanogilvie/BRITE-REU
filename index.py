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
    phead(name, admin)
    ptmpbody()
    ptail()

else:
    print("Location: login.py")
    print("Content-type: text/html\n")
