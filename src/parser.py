#!/usr/bin/python

import psycopg2
import lxml.etree as ET
import urllib.request
import urllib
import time
import sys, getopt
import os, shutil

def main(argv):

    hostname = 'db'
    username = 'postgres'
    password = '6Hwg8a7z3m7TZMg6'
    database = 'bmvimetadaten'

    # default values
    cleanup = False # if True Table will be dropped and recreated
    debug = False
    dryrun = True

    try:
        opts, args = getopt.getopt(argv,"hdcv",["no-dryrun","cleanup","debug"])
    except getopt.GetoptError:
        print ('parser.py [--no-dryrun] [--cleanup] [--debug]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('parser.py [--no-dryrun] [--cleanup] [--debug]')
            sys.exit()
        elif opt in ("-d", "--no-dryrun"):
            dryrun = False
        elif opt in ("-c", "--cleanup"):
            cleanup = True
        elif opt in ("-v", "--debug"):
            debug = True

    if cleanup :
        print ( bcolors.UNDERLINE + bcolors.BOLD + "# info # cleanup enabled; will remove old files and redownload #" + bcolors.ENDC )
    if dryrun :
        print ( bcolors.UNDERLINE + bcolors.BOLD + "# info # dryrun enabled; will not download #" + bcolors.ENDC )
    if debug :
        print ( bcolors.UNDERLINE + bcolors.BOLD + "# info # debug enabled #" + bcolors.ENDC )

    if cleanup and not dryrun :
        doCleanup()

    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    retrieveGML( myConnection, debug, cleanup, dryrun )
    myConnection.close()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def doCleanup() :
    print( bcolors.WARNING + "doing cleanup - deleting files" + bcolors.ENDC )
    folder = '/download'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

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

@timing
def retrieveGML( conn, debug, cleanup, dryrun ) :
    cur = conn.cursor()
    cur.execute( "SELECT id, data FROM metadata WHERE data LIKE '%SERVICE=WFS%'" )
    # cur.execute( "SELECT id, data FROM metadata WHERE id IN ( 838, 542, 370 )" ) # for tests only on selected ids
    # cur.execute( "SELECT id, data FROM metadata WHERE (id BETWEEN 1231 AND 1246) AND (data LIKE '%SERVICE=WFS%')" ) # for tests only on selected ids
    i = wfsUrlCount = wfsUrlCountAll = gmlCount = gmlCountAll = 0
    for id, data in cur.fetchall() :
        i += 1
        root = ET.fromstring( data )
        wfsUrls = root.findall( ".//{*}URL" )
        if debug :
            print (  )
        if  wfsUrls :
            if debug :
                print ( bcolors.UNDERLINE + bcolors.HEADER + "#### " + str(i) + " ####" + bcolors.ENDC )
        else :
            print ( bcolors.UNDERLINE + bcolors.HEADER + "#### " + str(i) + " ####" + bcolors.ENDC )
            print ( bcolors.FAIL + "# No wfsUrl found! metadata_id: " + str(id) + " #" + bcolors.ENDC )
        for wfsUrl in wfsUrls :
            if "REQUEST=GetCapabilities" in wfsUrl.text and "SERVICE=WFS" in wfsUrl.text:
                wfsName = wfsUrl.text.split('?')[0].split('/')[-1]
                print ( bcolors.BOLD + "### processing metadata_id: " + str(id) + " name: " + wfsName + " ###" + bcolors.ENDC )
                identifiers = root.findall( ".//{*}fileIdentifier/{*}CharacterString" )
                for identifier in identifiers :
                    if debug :
                        print ( bcolors.OKGREEN + "# identifier: " + identifier.text + bcolors.ENDC )
                if debug :
                    print ( bcolors.OKBLUE + "## WFS URL: " + wfsUrl.text + " ##" + bcolors.ENDC )
#1 take GetCapabilities url -> get xml
######################################
                try:
                    wfsUrlCount += 1
                    response = urllib.request.urlopen( wfsUrl.text )
                    xml = ET.fromstring( response.read() )

#2 find <FeatureTypeList> <FeatureType> <Name>
##############################################
                    featureTypes = xml.findall( ".//{*}FeatureType/{*}Name" )
                    if not featureTypes :
                        print ( bcolors.FAIL + "# No FeatureTypeName found (check parser)!" + bcolors.ENDC )
                    for featureType in featureTypes :
                        if debug :
                            print ( bcolors.OKGREEN + "# FeatureTypeName: " + featureType.text + bcolors.ENDC )
#4 build FeatureType url
########################


                        versions = xml.findall( ".//{*}ServiceTypeVersion" )
                        for version in versions :
                            featureTypeURLName = urllib.parse.quote( featureType.text, safe='/', encoding=None, errors=None )
                            gmlUrl = wfsUrl.text.replace( "REQUEST=GetCapabilities" , "version=" + version.text + "&REQUEST=GetFeature&count=5&typeNames=" + featureTypeURLName )
#5 download GML
###############
                            try:
                                response = urllib.request.urlopen( gmlUrl )
                                fileName = wfsName + "-" + identifier.text + "-" + featureType.text.split(':')[-1] + "-" + version.text + ".gml"
                                if not dryrun :
                                    text_file = open( "/download/" + fileName, "wb" )
                                    text_file.write( response.read() )
                                    text_file.close()
                                    if debug :
                                        print ( "  saved " + bcolors.UNDERLINE + gmlUrl + bcolors.ENDC + " to file: " + fileName )
                                gmlCount += 1
                            except UnicodeEncodeError as e:
                                print( bcolors.FAIL + "#2# ERROR: " + e.reason + " URL: " + gmlUrl + bcolors.ENDC )
                                pass

                except urllib.error.URLError as e:
                    print( bcolors.FAIL + "#1# ERROR: " + e.reason  + " metadata_id: " + str(id) + " name: " + wfsName + " URL: " + wfsUrl.text + bcolors.ENDC )
                    pass
                print ( "Collected " + str(gmlCount) + " GML files from " + str(wfsUrlCount) + " WFS URLs." )
                gmlCountAll += gmlCount
                wfsUrlCountAll += wfsUrlCount
                gmlCount = wfsUrlCount = 0
            # else :
            #     print ( bcolors.WARNING + "## wrong URL: " + wfsUrl.text + " ##" + bcolors.ENDC )
    print ( bcolors.OKGREEN + "Collection of GML files finished." + bcolors.ENDC)
    print ( bcolors.OKGREEN + "Collected " + str(gmlCountAll) + " GML files from " + str(wfsUrlCountAll) + " WFS URLs of " + str(i) + " metadata entries." + bcolors.ENDC)

if __name__ == "__main__":
   main(sys.argv[1:])
