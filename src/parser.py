#!/usr/bin/python

# import xml.etree.ElementTree as ET
import lxml.etree as ET
import urllib.request

hostname = 'db'
username = 'postgres'
password = '6Hwg8a7z3m7TZMg6'
database = 'bmvimetadaten'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def doQuery( conn ) :
    cur = conn.cursor()

    # cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%SERVICE=WFS%'" )
    cur.execute( "SELECT id, data FROM metadata WHERE id IN ( 370, 218, 319, 3814, 4208, 1552, 2377, 1202, 2530)" )

    i = 0
    for id, data in cur.fetchall() :
        i += 1
        root = ET.fromstring( data )
        # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        # print( "# WFS Num + id :", i, id )

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
        wfsUrls = root.findall( ".//{*}URL" )
        print (  )
        print ( bcolors.UNDERLINE + bcolors.HEADER + "#### " + str(i) + " ####" + bcolors.ENDC )
        # print ( elements )
        for wfsUrl in wfsUrls :
            if "REQUEST=GetCapabilities" in wfsUrl.text and "SERVICE=WFS" in wfsUrl.text:
                wfsName = wfsUrl.text.split('?')[0].split('/')[-1]

                print ( bcolors.BOLD + "### " + str(id) + " " + wfsName + " ###" + bcolors.ENDC )
                print ( bcolors.OKBLUE + "## " + wfsUrl.text + " ##" + bcolors.ENDC )

#1 take GetCapabilities url -> get xml
######################################

                response = urllib.request.urlopen( wfsUrl.text )
                # xmlString = response.read().decode()
                # xml = ET.ElementTree( ET.fromstring( xmlString ) )
                xml = ET.fromstring( response.read() )
                # print ( xml )
                # for elem in xml.iter() :
                #      print ( elem.tag, elem.text )

#2 find <FeatureTypeList> <FeatureType> <Name>
##############################################

                # featureTypes = xml.findall( ".//{http://www.opengis.net/wfs/2.0}FeatureType" )
                # featureTypes = xml.findall( ".//{http://www.opengis.net/wfs/2.0}Name" )
                featureTypes = xml.findall( ".//{*}FeatureType/{*}Name" )
                if not featureTypes :
                    print ( bcolors.FAIL + "# No FeatureTypeName found (check parser)!" + bcolors.ENDC )
                for featureType in featureTypes :
                    print ( bcolors.OKGREEN + "# FeatureTypeName : " + featureType.text + bcolors.ENDC )

#4 build FeatureType url
########################
                    # verison ??? --> ServiceTypeVersion
                    versions = xml.findall( ".//{*}ServiceTypeVersion" )
                    for version in versions :
                        # print ( version.text )
                        # replace REQUEST=GetCapabilities with REQUEST=GetFeature&typeNames=FeatureTypeName&count=5
                        gmlUrl = wfsUrl.text.replace( "REQUEST=GetCapabilities" , "version=" + version.text + "&REQUEST=GetFeature&count=5&typeNames=" + featureType.text )
                        # print ( gmlUrl )

#5 download GML
###############
                        response = urllib.request.urlopen( gmlUrl )
                        # gml = ET.fromstring( response.read() )
                        # print ( gml )
                        fileName = wfsName + "-" + featureType.text.replace( ":", "-" ) + "-" + version.text + ".gml"
                        text_file = open( "/download/" + fileName, "wb" )
                        text_file.write( response.read() )
                        text_file.close()
                        print ( "  saved file: " + fileName )
#3 write all in db
##################
# CREATE TABLE gml_files (
#     id          integer,
#     metadata_id integer,
#     filename    varchar(40) NOT NULL,
#     created     date,
#     PRIMARY KEY (id)
# );


import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
