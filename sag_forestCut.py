#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:23:57
#========================================
from maya.cmds import *
from geometry import *
from operator import add
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# CONVERTS LIST TO STRING
def sag_forestCut_listToString( l ):
        return ''.join(map(lambda x:str(x)+' ', l)) 


# FINDS INDICES IN GIVEN VOLUME
def sag_forestCut_getIndices( geo, box ):
        placesFileName = getAttr( geo[1] + '.places_filename' )
        boxSize = [ getAttr( box + '.size' + i ) for i in ('X', 'Y', 'Z') ]
        geoCubeTransform = inverseTransform( matrix( xform( geo[0], q = True, matrix = True, worldSpace = True ) ) )

        # THIS NEEDS TO BE FILLED IN ANIMATION
        matrices = list( matrix( xform( box, q = True, matrix = True, worldSpace = True) ) * geoCubeTransform )

        m = sag_forestCut_listToString( matrices )
        res = getIndexesInBox( b = boxSize, m = m, f = placesFileName )

        return res


# CREATE VOLUME
def sag_forestCut_volume():
        objShp = createNode( 'implicitBox' )
        obj = listRelatives( objShp, parent = True )[0]
        addAttr( objShp, ln = 'forestCut', at = 'bool', dv = True )

        return obj


# MANAGEMENT
def sag_forestCut( mode, anim ):
        selList = ls( sl = True, long = True )

        geoList = {}
        volList = []

        #CHECK SELECTION AND FIND FORESTGEOSHADERS
        wrongSelection = 0
        if selList != []:
                for eachSel in selList:
                        if nodeType( eachSel ) == 'transform':
                                shps = listRelatives( eachSel, shapes = True, fullPath = True )
                                if shps != None:
                                        for shp in shps:
                                                if nodeType( shp ) == 'mesh':
                                                        forestShd = listConnections( eachSel, s = True, d = False, type = 'forestGeoShader' )
                                                        if forestShd != None:
                                                                geoList[ eachSel ] = forestShd[0]
                                                        else:
                                                                wrongSelection = 1
                                                elif nodeType( shp ) == 'implicitBox':
                                                        volList.append( eachSel )
                                                elif nodeType( shp ) == 'viewportForest':
                                                        connGeo = listConnections( shp + '.placesFileName', s = True, d = False )
                                                        connObj = listConnections( shp + '.inputMesh', s = True, d = False )
                                                        if connGeo != None and connObj != None:
                                                                geoList[ connObj[0] ] = connGeo[0]
                                                else:
                                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'mesh':
                                forestShd = listConnections( eachSel, s = True, d = False, type = 'forestGeoShader' )
                                if forestShd != None:
                                        geoList[ listRelatives( eachSel, parent = True )[0] ] = forestShd[0]
                                else:
                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'implicitBox':
                                volList.append( listRelatives( eachSel, parent = True )[0] )
                        elif nodeType( eachSel ) == 'viewportForest':
                                connGeo = listConnections( eachSel + '.placesFileName', s = True, d = False )
                                connObj = listConnections( eachSel + '.inputMesh', s = True, d = False )
                                if connGeo != None and connObj != None:
                                        geoList[ connObj[0] ] = connGeo[0]
                        else:
                                wrongSelection = 1

        if selList == [] or geoList == {}:
                if not wrongSelection:
                        for eachForest in ls( type = 'forestGeoShader' ):
                                conns = listConnections( eachForest, s = False, d = True, type = 'transform' )
                                if conns != None:
                                        for eachConn in conns:
                                                geoList[ eachConn ] = eachForest

        #STOP SCRIPT IF NO FOREST SETUP FOUND
        if geoList == {}:
                confirmDialog( title = 'Error!', message = 'No forestGeoShader in selection or the scene!', button = [ 'CANCEL' ] )
                return

        #IF NO VOLUMES SELECTED, USE ALL IN THE SCENE THAT HAVE FORESTCUT ATTR TURNED ON
        if volList == []:
                for each in ls( type = 'implicitBox' ):
                        if attributeQuery( 'forestCut', node = each, exists = True ):
                                if getAttr( each + '.forestCut' ):
                                        volList.append( listRelatives( each, parent = True )[0] )

        #STOP THE SCRIPT IF NO VOLUMES FOUND STILL
        if volList == []:
                confirmDialog( title = 'Error!', message = 'No volumes in selection or the scene!', button = [ 'CANCEL' ] )
                return

        # GET FRAME RANGE FROM TIME SLIDER
        curFrame = currentTime( query = True )
        startFrame = curFrame
        endFrame = curFrame
        if anim == 'slider':
                startFrame = playbackOptions( q = True, min = True )
                endFrame = playbackOptions( q = True, max = True )

        #CHECK INDICES IN VOLUME AND APPLY TO FORESTGEOSHADERS
        exclList = {}
        for fr in xrange( int( startFrame ), int( endFrame ) + 1 ):
                if anim != 'static':
                        currentTime( fr, update = True )
                for each in geoList:
                        indList = []
                        if each in exclList:
                                indList = exclList[each]

                        for eachVol in volList:
                                indices = sag_forestCut_getIndices( [ each, geoList[each] ], eachVol )
                                if indices != None:
                                        indList += indices

                        indList = list( set( indList ) )
                        exclList[each] = indList
        if anim != 'static':
                currentTime( curFrame, update = True )

        for each in exclList:
                indList = exclList[each]
                indStr = ''
                if mode == 'add':
                        for ind in getAttr( geoList[each] + '.excludeList' ).split():
                                indList.append( int( ind ) )
                if indList != [] and indList != None:
                        indList.sort()
                        indStr = sag_forestCut_listToString( indList )
                setAttr( geoList[each] + '.excludeList', indStr, type = 'string' )
