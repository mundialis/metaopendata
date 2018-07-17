#!/usr/bin/python

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT id, data FROM metadata" )

    for id, data in cur.fetchall() :
        print (id, data[:100])


print ("Using psycopg2")
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
