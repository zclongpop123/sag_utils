#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:27:25
#========================================
from maya.cmds import *
import os, os.path, shutil, glob
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# LISTS
scenes = []
chars = []
locations = []
props = []
tex = []
maps = []
caches = []
misc = []
errors = []

# STORAGE
sn = workspace( query = True, sn = True ).replace( '\\', '/' )
storageFile = sn[:sn.rfind( '/' )+1] + 'collector.list'

# RESTORE DATA FROM STORAGE IF IT EXISTS ALREADY
if os.path.exists( storageFile ):
        f = open( storageFile, 'r' )
        section = ''
        for eachLine in f:
                eachLine = eachLine[:-1]
                if eachLine.find( 'rem ' ) == 0:
                        section = eachLine[4:]
                elif eachLine != '':
                        if section == 'SCENES':
                                scenes.append( eachLine )
                        elif section == 'CHARACTERS':
                                chars.append( eachLine )
                        elif section == 'LOCATIONS':
                                locations.append( eachLine )
                        elif section == 'PROPS':
                                props.append( eachLine )
                        elif section == 'TEXTURES':
                                tex.append( eachLine )
                        elif section == 'MAPS':
                                maps.append( eachLine )
                        elif section == 'CACHES':
                                caches.append( eachLine )
                        elif section == 'MISC':
                                misc.append( eachLine )
                        elif section == 'ERRORS':
                                errors.append( eachLine )
        f.close()

# CHECK FOREST GEO SHADERS FOR INPUT FILES
for each in ls( type = 'forestGeoShader' ):
        places = getAttr( each + '.places_filename' ).lower().replace( '\\', '/' ).replace( '#', '*' )
        if places != '' and places not in maps:
                maps.append( places )
        objects = getAttr( each + '.object_filename' ).lower().replace( '\\', '/' ).replace( '#', '*' )
        if objects != '' and objects not in maps:
                maps.append( objects )

# CHECK REFERENCES FOR INPUT FILES
allRefs = file( query = True, list = True, withoutCopyNumber = True )

# ADD TEXTURES INCLUDING LOCAL
localTex = ls( type = 'file' )
localTex += ls( type = 'mentalrayTexture' )

for eachTex in localTex:
        filePath = getAttr( eachTex + '.fileTextureName' )
        if filePath != None:
                filePath = filePath.lower().replace( '\\', '/' )
                if filePath != '':
                        if not 'c:/temp/' in filePath and not filePath in tex:
                                if os.path.exists( filePath ):
                                        allRefs.append( filePath )
                                else:
                                        if not filePath in errors:
                                                errors.append( filePath )
                                                print 'FILE DOESN\'T EXIST: ' + filePath
                else:
                        print 'EMPTY FILE: ' + eachTex
        else:
                print 'EMPTY FILE: ' + eachTex

for eachRef in allRefs:
        eachRefFormat = eachRef.lower().replace( '\\', '/' )
        fileType = eachRefFormat.split( '.' )[-1].lower()

        if fileType == 'ma' or fileType == 'mb':
                used = 0
                for eachDir in eachRefFormat.split( '/' ):
                        if eachDir == 'locations_compilation':
                                if not eachRefFormat in locations:
                                        locations.append( eachRefFormat )
                                used = 1
                        elif eachDir == 'locations':
                                if not eachRefFormat in props:
                                        props.append( eachRefFormat )
                                used = 1
                        elif eachDir == 'characters':
                                if not eachRefFormat in chars:
                                        chars.append( eachRefFormat )
                                used = 1
                if not used:
                        if not eachRefFormat in scenes:
                                scenes.append( eachRefFormat )

        elif fileType == 'tga' or fileType == 'iff' or fileType == 'bmp' or fileType == 'tif' or fileType == 'tiff' or fileType == 'jpg' or fileType == 'jpeg' or fileType == 'map':
                if not 'c:/temp/' in eachRefFormat:
                        if not eachRefFormat in tex:
                                tex.append( eachRefFormat )

        elif fileType == 'mc' or fileType == 'xml':
                if not eachRefFormat in caches:
                        caches.append( eachRefFormat )

        else:
                misc.append( eachRefFormat )

#for eachRef in file( query = True, reference = True ):
#	file( eachRef, unloadReference = True )

# WRITE DATA INTO A FILE
f = open( storageFile, 'w' )

f.write( 'rem SCENES\n' )
for each in scenes:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem CHARACTERS\n' )
for each in chars:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem LOCATIONS\n' )
for each in locations:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem PROPS\n' )
for each in props:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem TEXTURES\n' )
for each in tex:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem MAPS\n' )
for each in maps:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem CACHES\n' )
for each in caches:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem MISC\n' )
for each in misc:
        f.write( each + '\n' )
f.write( '\n' )

f.write( 'rem ERRORS\n' )
for each in errors:
        f.write( each + '\n' )
f.write( '\n' )

f.close()

# MAKE DUPLICATES
fromPath = 's:/savva'
toPath = 'd:/savva'

f = open( storageFile, 'r' )

for eachLine in f:
        eachLine = eachLine[:-1]
        if not 'rem ' in eachLine and not eachLine == '':
                newPath = eachLine[:eachLine.rfind( '/' )].replace( fromPath, toPath )
                if not os.path.exists( newPath ):
                        os.makedirs( newPath )
                if os.path.exists( eachLine ):
                        shutil.copy( eachLine, eachLine.replace( fromPath, toPath ) )
                else:
                        if eachLine.find( '*' ) > -1:
                                for eachFile in glob.glob( eachLine ):
                                        shutil.copy( eachFile, eachFile.replace( fromPath, toPath ) )
                        else:
                                print 'FILE DOESN\'T EXIST: ' + eachLine
