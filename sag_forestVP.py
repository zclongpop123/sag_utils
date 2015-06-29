#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:23:37
#========================================
from maya.cmds import *
from random import uniform
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_forestVP():
        selList = ls( sl = True, long = True )

        #DATA STORAGES
        geoList = {}
        camList = []
        lightList = []

        #CHECK SELECTION AND PUT IT INTO CORRESPONDING STORAGES
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
                                                elif nodeType( shp ) == 'camera' or nodeType( shp ) == 'stereoRigCamera':
                                                        camList.append( shp )
                                                elif nodeType( shp ) == 'directionalLight' or nodeType( shp ) == 'pointLight':
                                                        lightList.append( shp )
                                                else:
                                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'mesh':
                                forestShd = listConnections( eachSel, s = True, d = False, type = 'forestGeoShader' )
                                if forestShd != None:
                                        geoList[ listRelatives( eachSel, parent = True )[0] ] = forestShd[0]
                                else:
                                        wrongSelection = 1
                        elif nodeType( eachSel ) == 'camera' or nodeType( eachSel ) == 'stereoRigCamera':
                                camList.append( eachSel )
                        elif nodeType( eachSel ) == 'stereoRigTransform':
                                camList.append( listRelatives( eachSel, shapes = True, fullPath = True, type = 'stereoRigCamera' )[0] )
                        elif nodeType( eachSel ) == 'directionalLight' or nodeType( eachSel ) == 'pointLight':
                                lightList.append( eachSel )
                        else:
                                wrongSelection = 1

        if selList == [] or geoList == {}:
                if not wrongSelection:
                        for eachForest in ls( type = 'forestGeoShader' ):
                                conns = listConnections( eachForest, s = False, d = True, type = 'transform' )
                                if conns != None:
                                        for eachConn in conns:
                                                geoList[ eachConn ] = eachForest

        #REMOVE DUPLICATES
        camList = list( set( camList ) )
        lightList = list( set( lightList ) )

        #STOP SCRIPT IF NO FOREST SETUP FOUND
        if geoList == {}:
                confirmDialog( title = 'Error!', message = 'No forestGeoShader in selection or the scene!', button = [ 'CANCEL' ] )
                return

        #CREATE VP NODE AND MAKE CONNECTIONS
        vpList = []
        vpInd = 0
        for eachGeo in geoList:
                eachShp = listRelatives( eachGeo, shapes = True )[0]
                geoName = eachGeo.split( '|' )[-1].split( ':' )[-1]
                vp = createNode( 'viewportForest' )
                vpTr = rename( listRelatives( vp, parent = True )[0], geoName + '_vp' )
                vp = rename( vp, vpTr + 'Shape' )
                vpList.append( vp )

                connectAttr( 'defaultResolution.deviceAspectRatio', vp + '.aspect' )
                connectAttr( 'defaultResolution.width', vp + '.imageWidthRes' )
                connectAttr( 'defaultResolution.height', vp + '.imageHeightRes' )

                if camList == []:
                        cam = 'perspShape'
                else:
                        cam = camList[0]

                connectAttr( cam + '.focalLength', vp + '.focalLength' )
                connectAttr( cam + '.horizontalFilmAperture', vp + '.aperture' )

                parent( vpTr, eachGeo )
                xform( vpTr, matrix = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0] )

                connectAttr( eachGeo + '.outMesh', vp + '.inputMesh' )
                connectAttr( eachShp + '.boundingBoxMin', vp + '.bboxMin' )
                connectAttr( eachShp + '.boundingBoxMax', vp + '.bboxMax')
                connectAttr( eachGeo + '.v', vp + '.v' )

                connectAttr( 'time1.outTime', vp + '.inTime' )
                connectAttr( geoList[ eachGeo ] + '.places_filename', vp + '.placesFileName' )
                connectAttr( geoList[ eachGeo ] + '.shadow_plane_level', vp + '.shadowPlane')
                connectAttr( geoList[ eachGeo ] + '.user_shadow_plane', vp + '.userShadowPlane')
                connectAttr( geoList[ eachGeo ] + '.use_mirror', vp + '.mirror')
                connectAttr( geoList[ eachGeo ] + '.mirror_count', vp + '.mirrorCount')
                connectAttr( geoList[ eachGeo ] + '.fade_distance', vp + '.pathDistance')
                connectAttr( geoList[ eachGeo ] + '.use_path_fade', vp + '.pathBorder')

                for eachAttr in [ 'use_filter_distance', 
                                  'minDistance', 
                                  'maxDistance', 
                                  'minDensity', 
                                  'vertical_disappear', 
                                  'scale', 
                                  'verticality', 
                                  'vertical_rnd', 
                                  'trample_down', 
                                  'trim', 
                                  'trim_point1', 
                                  'trim_point2', 
                                  'screen_sizeX1', 
                                  'screen_sizeX2', 
                                  'screen_sizeY1', 
                                  'screen_sizeY2', 
                                  'use_filter_camera', 
                                  'start_count', 
                                  'end_count', 
                                  'sub_places', 
                                  'sub_radius', 
                                  'sub_count', 
                                  'bunch', 
                                  'bunch_radius', 
                                  'bunch_count', 
                                  'bunch_angle', 
                                  'check_shadows', 
                                  'excludeList', 
                                  'rippling', 
                                  'rippling_direction', 
                                  'rippling_angle', 
                                  'rippling_maxAngle', 
                                  'rippling_ampSin', 
                                  'rippling_freqSin', 
                                  'rippling_freqCoeff',
                                  'rippling_freqBlend',
                                  'rippling_ampNoise', 
                                  'rippling_freqNoise', 
                                  'rippling_ampWind', 
                                  'rippling_freqWind', 
                                  'rippling_fractalAmp', 
                                  'rippling_fractalScale', 
                                  'rippling_fractalSeed', 
                                  'rippling_phase' ]:
                        connectAttr( geoList[ eachGeo ] + '.' + eachAttr, vp + '.' + eachAttr )

                multMtx = createNode( 'multMatrix', name = geoName + '_multMtx' ) 
                connectAttr( eachGeo + '.worldMatrix', multMtx + '.matrixIn[0]' )
                connectAttr( listRelatives( cam, parent = True )[0] + '.worldInverseMatrix', multMtx + '.matrixIn[1]' )
                connectAttr( multMtx + '.matrixSum', vp + '.camInvMatrix' )

                parent( vpTr, world = True, absolute = True )

                setAttr( vp + '.filterCameraAtViewport', 1 )
                vpInd += 1
                if vpInd > 1:
                        #setAttr( vp + '.color', uniform( 0.0, 1.0 ), uniform( 0.0, 1.0 ), uniform( 0.0, 1.0 ), type = 'double3' )
                        if vpInd > 29:
                                vpInd -= 28
                        clr = colorIndex( vpInd+2, query = True )
                        setAttr( vp + '.color', clr[0], clr[1], clr[2], type = 'double3' )

        if vpList != []:
                select( vpList, replace = True )
