#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:24:30
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_forestCheckShadows():
        selList = ls( sl = True, long = True )

        geoList = []
        litList = []

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
                                                                geoList.append( forestShd[0] )
                                                        else:
                                                                wrongSelection = 1
                                                elif nodeType( shp ) == 'viewportForest':
                                                        connGeo = listConnections( shp + '.placesFileName', s = True, d = False )
                                                        connObj = listConnections( shp + '.inputMesh', s = True, d = False )
                                                        if connGeo != None and connObj != None:
                                                                geoList.append( connGeo[0] )
                                                elif nodeType( shp ) == 'directionalLight' or nodeType( shp ) == 'pointLight' or nodeType( shp ) == 'spotLight':
                                                        litList.append( shp )
                                                else:
                                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'mesh':
                                forestShd = listConnections( eachSel, s = True, d = False, type = 'forestGeoShader' )
                                if forestShd != None:
                                        geoList.append( forestShd[0] )
                                else:
                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'viewportForest':
                                connGeo = listConnections( eachSel + '.placesFileName', s = True, d = False )
                                connObj = listConnections( eachSel + '.inputMesh', s = True, d = False )
                                if connGeo != None and connObj != None:
                                        geoList.append( connGeo[0] )
                        elif nodeType( eachSel ) == 'forestGeoShader':
                                geoList.append( eachSel )
                        elif nodeType( eachSel ) == 'directionalLight' or nodeType( eachSel ) == 'pointLight' or nodeType( eachSel ) == 'spotLight':
                                litList.append( eachSel )
                        else:
                                wrongSelection = 1
        else:
                confirmDialog( title = 'Error!', message = 'Select a light you want to calculate shadows from!', button = [ 'CANCEL' ] )
                return

        if geoList == []:
                if not wrongSelection:
                        for eachForest in ls( type = 'forestGeoShader' ):
                                conns = listConnections( eachForest, s = False, d = True, type = 'transform' )
                                if conns != None:
                                        for eachConn in conns:
                                                geoList.append( eachForest )

        #STOP SCRIPT IF NO FOREST SETUP FOUND
        if geoList == []:
                confirmDialog( title = 'Error!', message = 'No forestGeoShader in selection or the scene!', button = [ 'CANCEL' ] )
                return

        #STOP SCRIPT IF NO LIGHTS FOUND IN SELECTION
        if litList == []:
                confirmDialog( title = 'Error!', message = 'No lights found in selection! Select a light you want to calculate shadows from!', button = [ 'CANCEL' ] )
                return
        elif len( litList ) > 1:
                confirmDialog( title = 'Error!', message = 'You can use only one light!', button = [ 'CANCEL' ] )
                return


        #MAKE CONNECTIONS
        for each in geoList:
                pLight = 0
                if nodeType( litList[0] ) == 'pointLight':
                        pLight = 1

                if not isConnected( litList[0] + '.worldMatrix[0]', each + '.light_transform' ):
                        connectAttr( litList[0] + '.worldMatrix[0]', each + '.light_transform', force = True )

                setAttr( each + '.point_light', pLight )

                setAttr( each + '.check_shadows', 1 )
