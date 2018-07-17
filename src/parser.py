#!/usr/bin/python

import re

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%WFS%'" )

    i = 0
    for id, data in cur.fetchall() :
        i += 1
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', data)
        print (i, id)
        print (urls)


import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
