#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:22:20
#========================================
from maya.cmds import *
import maya.mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


# MAIN PROCEDURE
def sag_hairUnDyn():
        selList = ls( selection = True, long = True )

        hairList = []
        # FIND ALL HAIRNODES IN THE SCENE IF NOTHING IS SELECTED
        if selList == []:
                hairList = ls( type = 'hairNode' )

                if hairList == []:
                        confirmDialog( title = 'Hair Cache Warning', message = 'No hairNodes found in the scene!', button = [ 'OK' ] )
                        return

        # FIND ALL HAIRNODES BASED ON SELECTION
        else:
                for each in selList:
                        # FOR HAIRCUBE OR MESH SELECTION
                        if objectType( each ) == 'transform':
                                geoShd = listConnections( each + '.miGeoShader', s = True, d = False )

                                if geoShd != None:
                                        if objectType( geoShd[0] ) == 'hairGeoShader':
                                                usrData = listConnections( geoShd[0] + '.userData', s = True, d = False )
                                                if usrData != None:
                                                        if objectType( usrData[0] ) == 'mentalrayUserData':
                                                                hairNode = listConnections( usrData[0] + '.asciiData', s = True, d = False )
                                                                if hairNode != None:
                                                                        if objectType( hairNode[0] ) == 'hairNode':
                                                                                hairList.append( hairNode[0] )
                                else:
                                        shp = listRelatives( each, shapes = True, noIntermediate = True, path = True )
                                        if shp != None:
                                                for eachShp in shp:
                                                        furMesh = listConnections( eachShp + '.message', s = False, d = True )
                                                        if furMesh != None:
                                                                for eachFurMesh in furMesh:
                                                                        if objectType( eachFurMesh ) == 'hairGeoShader':
                                                                                usrData = listConnections( eachFurMesh + '.userData', s = True, d = False )
                                                                                if usrData != None:
                                                                                        if objectType( usrData[0] ) == 'mentalrayUserData':
                                                                                                hairNode = listConnections( usrData[0] + '.asciiData', s = True, d = False )
                                                                                                if hairNode != None:
                                                                                                        if objectType( hairNode[0] ) == 'hairNode':
                                                                                                                hairList.append( hairNode[0] )
                        # FOR HAIRGUIDE SELECTION
                        elif objectType( each ) == 'hairTransform':
                                hairNode = listConnections( each + '.outputData', s = False, d = True )
                                if hairNode != None:
                                        for eachHairNode in hairNode:
                                                if objectType( eachHairNode ) == 'hairNode':
                                                        hairList.append( eachHairNode )
                        # FOR HAIRNODE SELECTION
                        elif objectType( each ) == 'hairNode':
                                hairList.append( each )

                if hairList == []:
                        confirmDialog( title = 'Hair Remove Dynamics Warning', message = 'No hairNodes found based on selection!', button = [ 'OK' ] )
                        return

        # CHECK HISTORY FOR EACH HAIRNODE, RECONNECT ORIGINAL GUIDE SHAPES AND DELETE DYNAMICS NODES
        feedback = []
        for hairNode in hairList:
                feedback.append( '\r\n Evaluating ' + hairNode + ':\r\n' )

                shInd = getAttr( hairNode + '.inputSpline', mi = True )
                trInd = getAttr( hairNode + '.inputData', mi = True )

                # IF SOME SPLINES HAVE NO TRANSFORMS OR VICE VERSA, MAKE INFO AND REMOVE FROM LIST
                for each in shInd:
                        if each not in trInd:
                                feedback.append( ' No transform for spline #' + str( each ) + ']\r\n' )
                                shInd.remove( each )
                        else:
                                conns = listConnections( hairNode + '.inputSpline[' + str( each ) + ']', s = 1, d = 0 )
                                if conns == None:
                                        feedback.append( ' No connection for spline #' + str( each ) + ']\r\n' )
                                        shInd.remove( each )
                                        trInd.remove( each )
                for each in trInd:
                        if each not in shInd:
                                feedback.append( ' No spline for transform [' + str( each ) + ']\r\n' )
                                trInd.remove( each )
                        else:
                                conns = listConnections( hairNode + '.inputData[' + str( each ) + ']', s = 1, d = 0 )
                                if conns == None:
                                        feedback.append( ' No connection for transform [' + str( each ) + ']\r\n' )
                                        shInd.remove( each )
                                        trInd.remove( each )

                feedback.append( '\r\n' )

                for ind in shInd:
                        sh = listConnections( hairNode + '.inputSpline[' + str( ind ) + ']', s = 1, d = 0, c = 0, p = 0, sh = 1 )[0]
                        tr = listConnections( hairNode + '.inputData[' + str( ind ) + ']', s = 1, d = 0, c = 0, p = 0 )[0]

                        # FIND ORIGINAL SHAPE
                        origs = listRelatives( tr, shapes = True, path = True )

                        orig = ''
                        if origs != None:
                                for eachOrig in origs:
                                        hist = listHistory( eachOrig )

                                        if len( hist ) > 1:
                                                notOrig = 0
                                                for eachHist in hist[1:]:
                                                        if nodeType( eachHist ) == 'nurbsCurve':
                                                                if eachHist in origs:
                                                                        notOrig = 1
                                                if notOrig == 0:
                                                        if orig != '':
                                                                print 'More than one possible origs for ' + tr + '!'
                                                                return
                                                        orig = eachOrig
                                        else:
                                                if listConnections( eachOrig, s = 0, d = 1 ) == None:
                                                        delete( eachOrig )
                                                        feedback.append( ' Deleted floating orig: ' + eachOrig + '\r\n' )
                                                else:
                                                        if orig != '':
                                                                print 'More than one possible origs for ' + tr + '!'
                                                                return
                                                        orig = eachOrig

                        if orig == '':
                                print 'No origs found for ' + tr + '!'
                                return

                        # DELETE FOLLICLES IF PRESENT
                        prn1 = listRelatives( tr, parent = True, path = True )

                        if prn1 != None:
                                if listRelatives( prn1[0], shapes = True, type = 'follicle', path = True ) != None:
                                        prn2 = listRelatives( prn1[0], parent = True, path = True )
                                        if prn2 != None:
                                                parent( tr, prn2[0] )
                                                delete( prn1 )

                        # REMOVE DYNAMICS FROM SHAPE
                        if orig == sh:
                                #feedback.append( ' No dynamics for spline [' + str( ind ) + ']: ' + tr + ' <-> ' + sh + '\r\n' )
                                clrShp = listRelatives( tr, shapes = True, path = True )
                                clrShp.remove( orig )
                                if clrShp != []:
                                        delete( clrShp )
                        else:
                                setAttr( orig + '.v', 1 )
                                setAttr( orig + '.intermediateObject', 0 )

                                connectAttr( orig + '.local', hairNode + '.inputSpline[' + str( ind ) + ']', force = True )

                                delete( sh )

                                # DELETE ALL SHAPES BUT ORIG
                                clrShp = listRelatives( tr, shapes = True, path = True )
                                clrShp.remove( orig )
                                if clrShp != []:
                                        delete( clrShp )

                                if orig.find( 'Orig' ) > -1:
                                        orig = rename( orig, orig[:orig.find( 'Orig' )] )

                                feedback.append( '[' + str( ind ) + ']: ' + orig + ' -> ' + tr + '\r\n' )

        select( cl = True )

        # FEEDBACK
        feedbackOut = ' Removing dynamics from ' + str( len( hairList ) ) + ' hairNodes:'
        for each in hairList:
                feedbackOut += ' ' + each + ','
        feedbackOut = feedbackOut[:-1]

        feedLen = len( feedbackOut )
        feedbackOut += '\r\n'
        for each in feedback:
                if len( each ) > feedLen:
                        feedLen = len( each )
                feedbackOut += each

        liner = '#'
        for i in xrange( 0, feedLen ):
                liner += '#'
        print ''
        print liner
        print feedbackOut
        print liner
