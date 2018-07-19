#!/usr/bin/python

# import re
import xml.etree.ElementTree as ET

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%SERVICE=WFS%'" )
    # cur.execute( "SELECT id, data FROM metadata WHERE id = 370" )

    i = 0
    for id, data in cur.fetchall() :
        i += 1
        root = ET.fromstring( data )
        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        print( i, id )

        # print ( root )
        # for elem in root.iter() :
        #     print ( elem.tag, elem.text )
        #
        # root.getElementsByTagName(URL)

        # for child_of_root in root :
        #     print ( child_of_root.tag, child_of_root.attrib )
        #     for child_of_child_of_root in child_of_root :
        #         print ( child_of_child_of_root.tag, child_of_child_of_root.attrib )
        # for url in urls :
        #     print( url )
        # for child in e:
        #     print(child.tag, child.attrib)
        # for child2 in child.findall( 'distributionInfo' ) :
        #     for child3 in child2:
        #         print(child3.tag, child3.attrib)
        elements = root.findall(".//{http://www.isotc211.org/2005/gmd}URL")
        # print ( elements )
        for elem in elements :
            if "SERVICE=WFS" in elem.text:
                print ( elem.text )

                #1 take GetCapabilities url -> get xml
                #2 find <FeatureTypeList> <FeatureType> <Name> -> build getFeature URL -> dl GML file
                #3 write all in db


import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
