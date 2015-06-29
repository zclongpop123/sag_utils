#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:26:46
#========================================
from maya.cmds import *
from sag_fileTools import *
from string import zfill
import os, os.path, time
import maya.mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# TRANSFER SETTINGS FROM CHARACTER TO CROWD MEMBER
def sag_crowdLayers_transfer():
        selList = ls( sl = True )
        crd = selList[0][:selList[0].rfind( ':' )]
        obj = selList[1][:selList[1].rfind( ':' )]

        setAttr( crd + ':character.t', 0, 0, 0, type = 'double3' )
        setAttr( crd + ':character.r', 0, 0, 0, type = 'double3' )
        setAttr( crd + ':character.s', 1, 1, 1, type = 'double3' )

        grp = group( em = True )
        parent( crd + ':character', grp )
        parent( grp, obj + ':mesh' )
        setAttr( grp + '.t', 0, 0, 0, type = 'double3' )
        setAttr( grp + '.r', 0, 0, 0, type = 'double3' )
        setAttr( grp + '.s', 1, 1, 1, type = 'double3' )
        parent( crd + ':character', 'Crowds_grp' )
        delete( grp )

        setAttr( crd + ':cacheNode.cachePath', getAttr( obj + ':cacheNode.cachePath' ), type = 'string' )
        setAttr( crd + ':cacheNode.cacheName', getAttr( obj + ':cacheNode.cacheName' ), type = 'string' )
        setAttr( crd + ':character.v', getAttr( obj + ':character.v' ) )
        setAttr( crd + ':character.startFrame', getAttr( obj + ':cacheNode.startFrame' ) )
        setAttr( crd + ':character.scaled', getAttr( obj + ':cacheNode.scale' ) )
        setAttr( crd + ':character.reverse', getAttr( obj + ':cacheNode.reverse' ) )
        setAttr( crd + ':character.oscillate', getAttr( obj + ':cacheNode.oscillate' ) )
        setAttr( crd + ':cacheNode.hold', getAttr( obj + ':cacheNode.hold' ) )
        setAttr( crd + ':cacheNode.preCycle', getAttr( obj + ':cacheNode.preCycle' ) )
        setAttr( crd + ':cacheNode.postCycle', getAttr( obj + ':cacheNode.postCycle' ) )
        setAttr( crd + ':cacheNode.sourceStart', getAttr( obj + ':cacheNode.sourceStart' ) )
        setAttr( crd + ':cacheNode.sourceEnd', getAttr( obj + ':cacheNode.sourceEnd' ) )
        setAttr( crd + ':cacheNode.originalStart', getAttr( obj + ':cacheNode.originalStart' ) )
        setAttr( crd + ':cacheNode.originalEnd', getAttr( obj + ':cacheNode.originalEnd' ) )

        for attr in listAttr( obj + ':head_control', k = True ):
                setAttr( crd + ':head_control.' + attr, getAttr( obj + ':head_control.' + attr ) )
                if attr == 'drotik' and getAttr( obj + ':drotik.v' ) == 0:
                        setAttr( crd + ':head_control.drotik', 0 )


# SAVES SETTINGS FOR THE SELECTED CROWD MEMBER THEN APPLIES THEM TO ANOTHER ONE
def sag_crowdLayers_transferSingle( mode ):
        global trVals, chVals, msVals

        trAttrs = [ '.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v', '.startFrame', '.scaled', '.reverse', '.oscillate' ]
        chAttrs = [ '.cachePath', '.cacheName', '.hold', '.preCycle', '.postCycle', '.sourceStart', '.sourceEnd' ]

        ns = ls( sl = True )[0].split( ':' )[0]

        if mode == 'store':
                trVals = []
                chVals = []
                msVals = {}

                for attr in trAttrs:
                        trVals.append( getAttr( ns + ':character' + attr ) )
                for attr in chAttrs:
                        chVals.append( getAttr( ns + ':cacheNode' + attr ) )
                for attr in listAttr( ns + ':head_control', k = True ):
                        msVals[ '.' + attr ] = getAttr( ns + ':head_control.' + attr )

        elif mode == 'restore':
                try:
                        tmp = trVals
                except:
                        confirmDialog( title = 'Error!', message = 'Nothing stored!', button = [ 'Cancel' ] )
                        return

                editRenderLayerMembers( editRenderLayerGlobals( crl = True, query = True ), ns + ':character', noRecurse = True )

                for attr in trAttrs:
                        setAttr( ns + ':character' + attr, trVals[trAttrs.index(attr)] )
                for attr in chAttrs:
                        if chAttrs.index(attr) > 1:
                                setAttr( ns + ':cacheNode' + attr, chVals[chAttrs.index(attr)] )
                        else:
                                setAttr( ns + ':cacheNode' + attr, chVals[chAttrs.index(attr)], type = 'string' )
                for attr in msVals:
                        setAttr( ns + ':head_control' + attr, msVals[attr] )


# CREATES CROWD CONTROLS ATTRIBUTES ON SELECTED AND TRIES TO CONNECT THEM TO CACHE NODE
def sag_crowdLayers_ctrlSetup():
        for each in ls( sl = True ):
                cacheNode = each[:each.rfind( ':' )+1] + 'cacheNode'

                if objExists( cacheNode ):
                        if not attributeQuery( 'startFrame', node = each, exists = True ):
                                addAttr( each, ln = 'startFrame', at = 'time', k = True )
                        if not attributeQuery( 'scaled', node = each, exists = True ):
                                addAttr( each, ln = 'scaled', at = 'double', k = True )
                        if not attributeQuery( 'reverse', node = each, exists = True ):
                                addAttr( each, ln = 'reverse', at = 'bool', k = True )
                        if not attributeQuery( 'oscillate', node = each, exists = True ):
                                addAttr( each, ln = 'oscillate', at = 'bool', k = True )

                        setAttr( each + '.startFrame', 1 )
                        setAttr( each + '.scaled', 1 )
                        setAttr( cacheNode + '.hold', 0 )
                        setAttr( cacheNode + '.preCycle', 10000 )
                        setAttr( cacheNode + '.postCycle', 10000 )

                        if not isConnected( each + '.startFrame', cacheNode + '.startFrame' ):
                                connectAttr( each + '.startFrame', cacheNode + '.startFrame', force = True )
                        if not isConnected( each + '.scaled', cacheNode + '.scale' ):
                                connectAttr( each + '.scaled', cacheNode + '.scale', force = True )
                        if not isConnected( each + '.reverse', cacheNode + '.reverse' ):
                                connectAttr( each + '.reverse', cacheNode + '.reverse', force = True )
                        if not isConnected( each + '.oscillate', cacheNode + '.oscillate' ):
                                connectAttr( each + '.oscillate', cacheNode + '.oscillate', force = True )
                else:
                        confirmDialog( title = 'Warning', message = 'No cacheNode found for ' + each + '! No connections made!', button = [ 'OK' ] )


# PROMPT REPLACEMENT STRING
def sag_crowdLayers_promptReplace( title, message, txt ):
        prompt = promptDialog(
                title = title,
                message = message,
                text = txt,
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        replacement = ''
        if prompt == 'OK':
                replacement = promptDialog( query = True, text = True )
        else:
                replacement = None

        return replacement


# GET RENDERABLE RENDER LAYERS
def sag_crowdLayers_renderLays():
        lays = ls( type = 'renderLayer' )

        renderLays = []
        for eachLay in lays:
                if getAttr( eachLay + '.renderable' ) and eachLay.find( ':' ) < 0:
                        renderLays.append( eachLay )

        return renderLays


# MAIN PROCEDURE
def sag_crowdLayers( mode ):

        if mode == 'store' or mode == 'multiStore':
                fileName = fileDialog( mode = 1 )

                if fileName == '':
                        return

                selList = ls( selection = True )

                # ADD HEAD_CONTROL AND CACHENODE
                objList = []
                for each in selList:
                        objList.append( each )

                        if each.find( ':' ) > -1:
                                ctrlName = each.split( ':' )[-2] + ':head_control'
                                if objExists( ctrlName ):
                                        objList.append( ctrlName )

                                cacheName = each.split( ':' )[-2] + ':cacheNode'
                                if objExists( cacheName ):
                                        objList.append( cacheName )

                # GET LIST OF RENDER LAYERS TO EXPORT
                layList = [ editRenderLayerGlobals( query = True, currentRenderLayer = True ) ]
                curLayer = layList[0]

                if mode == 'multiStore':
                        layList = sag_crowdLayers_renderLays()	

                # RUN EXPORT
                for rLayer in layList:
                        if mode == 'multiStore':
                                editRenderLayerGlobals( currentRenderLayer = rLayer )
                                fileName = fileName[:fileName.rfind( '/' )+1] + rLayer + '.dat'

                        rLayerMems = editRenderLayerMembers( rLayer, query = True )

                        massDict = {}
                        for each in objList:
                                attrs = listAttr( each, k = True )
                                if nodeType( each ) == 'cacheFile':
                                        attrs = listAttr( each, cb = True ) + [ 'cachePath', 'cacheName' ]

                                attrDict = {}
                                for eachAttr in attrs:
                                        if each in selList and each.find( ':' ) > -1 and eachAttr == 'visibility' and each not in rLayerMems:
                                                attrDict[ eachAttr ] = 0
                                        else:
                                                attrDict[ eachAttr ] = getAttr( each + '.' + eachAttr )

                                massDict[ each ] = attrDict

                        sag_dataStore( massDict, fileName )

                if mode == 'multiStore':
                        editRenderLayerGlobals( currentRenderLayer = curLayer )

        elif mode == 'restore' or mode == 'multiRestore':
                fileName = fileDialog( mode = 0 )

                if fileName == '':
                        return

                layList = [ editRenderLayerGlobals( query = True, currentRenderLayer = True ) ]

                if mode == 'multiRestore':
                        layList = []
                        path = fileName[:fileName.rfind( '/' )+1]
                        for eachFile in os.listdir( path ):
                                if eachFile.find( '.dat' ) > -1:
                                        layList.append( eachFile[:-4] )
                        # SORT LAYERS IN REVERSE BASED ON NUMBERED SUFFIX
                        layListSorted = {}
                        for eachLay in layList:
                                layElem = eachLay.split( '_' )
                                try:
                                        layInd = int( layElem[-1] )
                                except:
                                        try:
                                                layInd = int( layElem[-2] )
                                        except:
                                                layInd = 0

                                layListSorted[ layInd ] = eachLay

                        layList = []
                        sortKeys = layListSorted.keys()
                        sortKeys.sort( reverse = False )
                        for eachLay in sortKeys:
                                layList.append( layListSorted[ eachLay ] )

                repl = sag_crowdLayers_promptReplace( 'Replacement', 'replaceFrom replaceTo:', 'crowd:' )
                if repl == None:
                        return

                if mode == 'multiRestore':
                        dupLay = sag_crowdLayers_promptReplace( 'Duplication', 'layer to duplicate (blank to create new):', 'crowd_1' )
                        if dupLay == None:
                                return

                for rLayer in layList:
                        if mode == 'multiRestore':
                                fileName = path + rLayer + '.dat'

                                if dupLay != '':
                                        if objExists( dupLay ):
                                                if nodeType( dupLay ) != 'renderLayer':
                                                        dupLay = ''
                                        else:
                                                dupLay = ''

                                existLayer = 0
                                if objExists( rLayer ): 
                                        if nodeType( rLayer ) != 'renderLayer':
                                                rLayer += '_TMP'
                                        else:
                                                existLayer = 1

                                if dupLay == '':
                                        if not existLayer:
                                                createRenderLayer( name = rLayer, g = True )
                                else:
                                        duplicate( dupLay, name = rLayer, ic = True )

                                editRenderLayerGlobals( currentRenderLayer = rLayer )

                        massDict = sag_dataRestore( fileName )

                        for each in massDict:
                                if repl == '':
                                        target = each
                                elif len( repl.split() ) == 1:
                                        target = repl + each
                                elif len( repl.split() ) == 2:
                                        target = each.replace( repl.split()[0], repl.split()[1] )
                                else:
                                        target = each

                                if objExists( target ):
                                        for eachAttr in massDict[ each ]:
                                                if eachAttr == 'cachePath' or eachAttr == 'cacheName':
                                                        editRenderLayerAdjustment( target + '.' + eachAttr )
                                                        setAttr( target + '.' + eachAttr, massDict[ each ][ eachAttr ], type = 'string' )
                                                elif getAttr( target + '.' + eachAttr, settable = True ):
                                                        editRenderLayerAdjustment( target + '.' + eachAttr )
                                                        setAttr( target + '.' + eachAttr, massDict[ each ][ eachAttr ] )

                                                # ALWAYS SET HAIR TO MESH
                                                if eachAttr == 'hair':
                                                        setAttr( target + '.hair', 2 )


# GENERATE HARDWARE LAYERS COMPOSITE BATCH
def sag_crowdLayers_hwComp( outListStr, fileName, curFrame, comp, compBatch, anim, startFrame, endFrame ):
        isFinal = 0
        if str( curFrame ) == str( endFrame ):
                isFinal = 1

        outList = outListStr.split()
        rd = workspace( query = True, rd = True )
        cmd = ''

        # CONVERT TO PNG
        for outFile in outList:
                cmd += '"' + os.getenv( 'MAYA_LOCATION' ) + '/bin/imgcvt.exe" "' + rd + outFile[:-8] + zfill( curFrame, 4 ) + '.iff" "' + rd + outFile[:-8] + zfill( curFrame, 4 ) + '.png"' + '\n'

        # LAYER
        outList.reverse()
        cmd += '"' + os.getenv( 'MAYA_LOCATION' ) + '/bin/imconvert.exe"'
        for outFile in outList:
                cmd += ' "' + rd + outFile[:-8] + zfill( curFrame, 4 ) + '.png"'
        cmd += ' -background black'
        cmd += ' -flatten "' + rd + fileName + '.' + zfill( curFrame, 4 ) + '.png"'

        # CLEANUP
        for outFile in outList:
                if comp != 'both':
                        cmd += '\n' + 'del "' + rd.replace( '/', '\\' ) + outFile[:-8].replace( '/', '\\' ) + zfill( curFrame, 4 ) + '.iff"'
                cmd += '\n' + 'del "' + rd.replace( '/', '\\' ) + outFile[:-8].replace( '/', '\\' ) + zfill( curFrame, 4 ) + '.png"'
        if anim == 'single':
                cmd += '\n' + 'call "' + rd + fileName + '.' + zfill( curFrame, 4 ) + '.png"'
        elif isFinal:
                cmd += '\n' + 'call "' + os.getenv( 'MAYA_LOCATION' ) + '/bin/fcheck.exe" -n ' + str( startFrame ) + ' ' + str( endFrame ) + ' 1 "' + rd + fileName + '.#.png"'
        cmd += '\n' + 'del "' + compBatch.replace( '/', '\\' ) + '"'

        # WRITE TO BATCH FILE
        f = open( compBatch, 'w' )
        f.write( cmd )
        f.close()


# HARDWARE LAYERS RENDERING
def sag_crowdLayers_hwRender( res, anim, comp, matte ):
        # VARS
        fileName = 'hwRender/gl'
        light = 0

        # GET SCENE NAME
        sceneName = file( query = True, sn = True, shn = True ).split( '.' )[0]
        curTime = time.strftime('%y%m%d') + '-' + time.strftime('%H%M%S')
        if sceneName == '':
                sceneName = 'untitled'

        procMel = 'C:/Temp/sag_crowdLayers_hwRender_' + sceneName + '.' + curTime + '.mel'
        compBatch = 'C:/Temp/sag_crowdLayers_hwComp_' + sceneName + '.' + curTime + '.bat'

        matteTypes = { 'none':1, 'black':6 }

        resTypes = { 'wide':'savva_wide 2138 872 2.452', 
                     'tall':'savva_tall 2138 1152 2.452',
                     'wide_half':'savva_wide_half 1069 436 2.452'
                     }

        # GET CAMERA
        camList = []
        for each in ls( sl = True ):
                if nodeType( each ) == 'stereoRigTransform':
                        camList.append( each )
                elif nodeType( each ) == 'stereoRigCamera':
                        camList.append( each )
                elif nodeType( each ) == 'camera':
                        camList.append( each )
                elif nodeType( each ) == 'transform':
                        shps = listRelatives( each, shapes = True )
                        if shps != None:
                                for shp in shps:
                                        if nodeType( shp ) == 'camera':
                                                camList.append( shp )

        if camList == []:
                confirmDialog( title = 'Error!', message = 'No cameras selected!', button = [ 'CANCEL' ] )
                return

        cam = camList[0]

        # GET FRAME RANGE FROM TIME SLIDER
        curFrame = int( currentTime( query = True ) )
        startFrame = curFrame
        endFrame = curFrame
        if anim == 'slider':
                startFrame = int( playbackOptions( q = True, min = True ) )
                endFrame = int( playbackOptions( q = True, max = True ) )
                curFrame = startFrame
                currentTime( curFrame )

        # FIND RENDERABLE RENDER LAYERS
        rLayers = sag_crowdLayers_renderLays()
        if rLayers == []:
                confirmDialog( title = 'Error!', message = 'No renderable renderLayers!', button = [ 'CANCEL' ] )
                return

        # SETUP HARDWARE RENDER BUFFER
        hwg = 'defaultHardwareRenderGlobals'
        setAttr( hwg + '.filename', fileName, type = 'string' )
        setAttr( hwg + '.extension', 4 )
        setAttr( hwg + '.startFrame', curFrame )
        setAttr( hwg + '.endFrame', curFrame )
        setAttr( hwg + '.byFrame', 1 )
        setAttr( hwg + '.imageFormat', 7 )
        setAttr( hwg + '.resolution', resTypes[res], type = 'string' )
        setAttr( hwg + '.alphaSource', matteTypes[matte] )
        setAttr( hwg + '.writeZDepth', 1 )
        setAttr( hwg + '.lightingMode', light )
        setAttr( hwg + '.drawStyle', 3 )
        setAttr( hwg + '.texturing', 1 )
        setAttr( hwg + '.lineSmoothing', 1 )
        setAttr( hwg + '.fullImageResolution', 1 )
        setAttr( hwg + '.geometryMask', 0 )
        setAttr( hwg + '.multiPassRendering', 0 )
        setAttr( hwg + '.grid', 0 )
        setAttr( hwg + '.cameraIcons', 0 )
        setAttr( hwg + '.lightIcons', 0 )
        setAttr( hwg + '.emitterIcons', 0 )
        setAttr( hwg + '.fieldIcons', 0 )
        setAttr( hwg + '.collisionIcons', 0 )
        setAttr( hwg + '.transformIcons', 0 )
        setAttr( hwg + '.backgroundColor', 0, 0, 0, type = 'double3' )

        # CREATE MEL PROC FOR EACH RENDER LAYER
        outList = []

        melCode = ''
        for i in xrange( 0, len( rLayers ) ):
                rLayer = rLayers[i]
                rLayerName = rLayer.split( ':' )[-1]
                if rLayerName == 'defaultRenderLayer':
                        rLayerName = 'masterLayer'
                fileNameLayer = fileName + '_' + rLayerName

                melCode += '\n' + 'global proc sag_crowdLayers_hwLayer' + str(i+1) + '( string $image, int $fs, int $fe, int $fi, int $rate, string $path, string $filename ) {'
                melCode += '\n\t' + 'editRenderLayerGlobals -crl "' + rLayer + '";'
                melCode += '\n\t' + 'setAttr "' + hwg + '.filename" -type "string" "' + fileNameLayer + '";'
                if i < len( rLayers ) - 1:
                        melCode += '\n\t' + 'glRender -e -fc sag_crowdLayers_hwLayer' + str(i+2) + ';'
                else:
                        melCode += '\n\t' + 'glRender -e -fc sag_crowdLayers_hwEnd;'
                melCode += '\n\t' + 'glRender -renderSequence hardwareRenderView;'
                melCode += '\n' + '}' + '\n'

                outList.append( fileNameLayer + '.' + zfill( curFrame, 4 ) + '.iff' )

                i += 1

        outListStr = ' '.join( outList )

        # APPEND TO RENDER END PROC
        melOut = 'global proc sag_crowdLayers_hwEnd( string $image, int $fs, int $fe, int $fi, int $rate, string $path, string $filename ) {'
        if comp == 'layer' or comp == 'both':
                melOut += '\n\t' + 'string $fr = `currentTime -q`;'
                melOut += '\n\t' + 'python( "sag_crowdLayers_hwComp( \\"' + outListStr + '\\", \\"' + fileName + '\\", " + $fr + ", \\"' + comp + '\\", \\"' + compBatch + '\\", \\"' + anim + '\\", \\"' + str( startFrame ) + '\\", \\"' + str( endFrame ) + '\\" )" );'
                melOut += '\n\t' + 'system( "' + compBatch + '" );'
        if anim == 'slider':
                melOut += '\n\t' + 'if( `currentTime -q` < ' + str( endFrame ) + ' ) {'
                melOut += '\n\t\t' + 'print( "Frame " + `currentTime -q` + " is done. Starting next one...\\n" );'
                melOut += '\n\t\t' + 'currentTime( `currentTime -q` + 1 );'
                melOut += '\n\t\t' + 'setAttr "' + hwg + '.startFrame" `currentTime -q`;'
                melOut += '\n\t\t' + 'setAttr "' + hwg + '.endFrame" `currentTime -q`;'
                melOut += '\n\t\t' + 'glRender -e -fc sag_crowdLayers_hwLayer1;'
                melOut += '\n\t\t' + 'glRender -renderSequence hardwareRenderView;'
                melOut += '\n\t' + '} else {'
                melOut += '\n\t\t' + 'print "Hardware Rendering Done!\\n";'
                melOut += '\n\t' + '}'
        else:
                melOut += '\n\t' + 'print "Hardware Rendering Done!\\n";' 
        melOut += '\n' + '}' + '\n'
        melOut += melCode

        # WRITE MEL PROCEDURES TO FILE
        #f = open( procMel, 'w' )
        #f.write( melOut )
        #f.close()

        # RUN GL RENDERING
        select( clear = True )
        maya.mel.eval( melOut )
        maya.mel.eval( 'glRenderWin' )
        glRenderEditor( 'hardwareRenderView', edit = True, lookThru = cam )
        maya.mel.eval( 'sag_crowdLayers_hwLayer1( "", 0, 0, 0, 0, "", "" )' )
