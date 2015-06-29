#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:22:04
#========================================
from maya.cmds import *
from hairMain import *
from hairUpdate import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# HAIR VIEWPORT VISUALIZATION
def sag_hairViewportVis():
        selList = ls( selection = True, long = True )

        hairList = []
        # FIND ALL HAIRGEOSHADER NODES IN THE SCENE IF NOTHING IS SELECTED
        if selList == []:
                hairList = ls( type = 'hairGeoShader' )

                if hairList == []:
                        confirmDialog( title = 'Hair Viewport Warning', message = 'No hairGeoShaders found in the scene!', button = [ 'OK' ] )
                        return

        # FIND ALL HAIRGEOSHADER NODES BASED ON SELECTION
        else:
                for each in selList:
                        # FOR HAIRCUBE OR MESH SELECTION
                        if objectType( each ) == 'transform':
                                geoShd = listConnections( each + '.miGeoShader', s = True, d = False )

                                if geoShd != None:
                                        if objectType( geoShd[0] ) == 'hairGeoShader':
                                                hairList.append( hairNode[0] )
                                else:
                                        shp = listRelatives( each, shapes = True, noIntermediate = True )
                                        if shp != None:
                                                for eachShp in shp:
                                                        furMesh = listConnections( eachShp + '.message', s = False, d = True )
                                                        if furMesh != None:
                                                                for eachFurMesh in furMesh:
                                                                        if objectType( eachFurMesh ) == 'hairGeoShader':
                                                                                hairList.append( eachFurMesh )
                        # FOR HAIRGUIDE SELECTION
                        elif objectType( each ) == 'hairTransform':
                                hairNode = listConnections( each + '.outputData', s = False, d = True )
                                if hairNode != None:
                                        for eachHairNode in hairNode:
                                                if objectType( eachHairNode ) == 'hairNode':
                                                        usrData = listConnections( eachHairNode + '.output', s = False, d = True )
                                                        if usrData != None:
                                                                for eachUsrData in usrData:
                                                                        if nodeType( eachUsrData ) == 'mentalrayUserData':
                                                                                geoShd = listConnections( eachUsrData + '.message', s = False, d = True )
                                                                                if geoShd != None:
                                                                                        for eachGeoShd in geoShd:
                                                                                                if nodeType( eachGeoShd ) == 'hairGeoShader':
                                                                                                        hairList.append( eachGeoShd )
                        # FOR HAIRGEOSHADER SELECTION
                        elif objectType( each ) == 'hairGeoShader':
                                hairList.append( each )
                        # FOR HAIRNODE SELECTION
                        elif objectType( each ) == 'hairNode':
                                usrData = listConnections( each + '.output', s = False, d = True )
                                if usrData != None:
                                        for eachUsrData in usrData:
                                                if nodeType( eachUsrData ) == 'mentalrayUserData':
                                                        geoShd = listConnections( eachUsrData + '.message', s = False, d = True )
                                                        if geoShd != None:
                                                                for eachGeoShd in geoShd:
                                                                        if nodeType( eachGeoShd ) == 'hairGeoShader':
                                                                                hairList.append( eachGeoShd )

                if hairList == []:
                        confirmDialog( title = 'Hair Viewport Warning', message = 'No hairGeoShaders found based on selection!', button = [ 'OK' ] )
                        return

        for each in hairList:
                hairSystemNodes( each ).updateTextures()
                hairSystemNodes( each ).updateViewport()


# SET ALL HEAD_CONTROL.HAIR TO MESH
def sag_hairViewportVis_setAllToMesh():
        for each in ls( '*head_control' ) + ls( '*:head_control' ) + ls( '*:*:head_control' ) + ls( '*:*:*:head_control' ) + ls( '*:*:*:*:head_control' ) + ls( '*:*:*:*:*:head_control' ):
                if attributeQuery( 'hair', node = each, exists = True ):
                        setAttr( each + '.hair', 0 )
