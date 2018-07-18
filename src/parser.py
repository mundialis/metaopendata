#!/usr/bin/python

# import re
import xml.etree.ElementTree as ET

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

def doQuery( conn ) :
    cur = conn.cursor()

    # cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%WFS%'" )
    cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%WFS%'" )

    i = 0
    for id, data in cur.fetchall() :
        i += 1
        e = ET.fromstring( data )
        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        # print(i, id)
        # for url in urls :
        #     print( url )
        for url in e.findall( 'gmd:URL' ) :
            print( url )



import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
