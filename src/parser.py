#!/usr/bin/python

# import xml.etree.ElementTree as ET
import lxml.etree as ET
import urllib.request

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

cleanup = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def createTable( conn ):
    cur = conn.cursor()
    dropTable = "DROP TABLE IF EXISTS gml_files;"
    try:
        cur.execute( dropTable )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    createTable = "CREATE TABLE IF NOT EXISTS gml_files (id SERIAL PRIMARY KEY, metadata_id integer NOT NULL, filename varchar(255) NOT NULL, created timestamp NOT NULL);"
    try:
        cur.execute( createTable )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def retrieveGML( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%SERVICE=WFS%'" )
    # cur.execute( "SELECT id, data FROM metadata WHERE id IN ( 370, 218, 319, 3814, 4208, 1552, 2377, 1202, 2530)" )
    for id, data in cur.fetchall() :1
        root = ET.fromstring( data )
        wfsUrls = root.findall( ".//{*}URL" )
        print (  )
        print ( bcolors.UNDERLINE + bcolors.HEADER + "#### " + str(i) + " ####" + bcolors.ENDC )
        for wfsUrl in wfsUrls :
            if "REQUEST=GetCapabilities" in wfsUrl.text and "SERVICE=WFS" in wfsUrl.text:
                wfsName = wfsUrl.text.split('?')[0].split('/')[-1]
                print ( bcolors.BOLD + "### " + str(id) + " " + wfsName + " ###" + bcolors.ENDC )
                print ( bcolors.OKBLUE + "## " + wfsUrl.text + " ##" + bcolors.ENDC )
#1 take GetCapabilities url -> get xml
######################################
                response = urllib.request.urlopen( wfsUrl.text )
                xml = ET.fromstring( response.read() )
#2 find <FeatureTypeList> <FeatureType> <Name>
##############################################
                featureTypes = xml.findall( ".//{*}FeatureType/{*}Name" )
                if not featureTypes :
                    print ( bcolors.FAIL + "# No FeatureTypeName found (check parser)!" + bcolors.ENDC )
                for featureType in featureTypes :
                    print ( bcolors.OKGREEN + "# FeatureTypeName : " + featureType.text + bcolors.ENDC )
#4 build FeatureType url
########################
                    versions = xml.findall( ".//{*}ServiceTypeVersion" )
                    for version in versions :
                        gmlUrl = wfsUrl.text.replace( "REQUEST=GetCapabilities" , "version=" + version.text + "&REQUEST=GetFeature&count=5&typeNames=" + featureType.text )
#5 download GML
###############
                        response = urllib.request.urlopen( gmlUrl )
                        fileName = wfsName + "-" + featureType.text.replace( ":", "-" ) + "-" + version.text + ".gml"
                        text_file = open( "/download/" + fileName, "wb" )
                        text_file.write( response.read() )
                        text_file.close()
                        print ( "  saved file: " + fileName )
#3 write all in db
##################
                        insert = "INSERT INTO gml_files (metadata_id, filename, created) VALUES (" + str(id) + ", \'" + fileName + "\', " + "current_timestamp"  + ");"
                        cur.execute( insert )
                        conn.commit()

import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
if cleanup :
    createTable( myConnection )

retrieveGML( myConnection )
myConnection.close()
