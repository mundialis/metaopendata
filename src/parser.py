#!/usr/bin/python

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT id, data FROM metadata WHERE ("data" LIKE '%WFS%' OR "changedate" LIKE '%WFS%' OR "createdate" LIKE '%WFS%' OR "doctype" LIKE '%WFS%' OR "extra" LIKE '%WFS%' OR "root" LIKE '%WFS%' OR "schemaid" LIKE '%WFS%' OR "title" LIKE '%WFS%' OR "istemplate" LIKE '%WFS%' OR "isharvested" LIKE '%WFS%' OR "harvesturi" LIKE '%WFS%' OR "harvestuuid" LIKE '%WFS%' OR "source" LIKE '%WFS%' OR "uuid" LIKE '%WFS%')
 )

    for id, data in cur.fetchall() :
        print (id, data[:100])


import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
