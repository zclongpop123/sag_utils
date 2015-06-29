#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:19:12
#========================================
from maya.cmds import *
import maya.mel

import time
from string import zfill

from sag_exrCube import *
from sag_utils import *
from sag_eyeMasks import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

modes = [ 'env', 'chars', 'furry', 'occl', 'shadow', 'crossMask', 'eyeMask', 'dofReference', 'lightMask' ]


def sag_renderSetup_timer( startTime ):
        endTime = time.clock()	
        secs = int( (endTime - startTime) % 60 )
        hours = int( (endTime - startTime - secs) / 3600 )
        mins = int( (endTime - startTime - secs - hours * 3600) / 60 )
        duration = zfill( str( hours ), 2 ) + ':' + zfill( str( mins ), 2 ) + ':' + zfill( str( secs ), 2 )

        return duration


def sag_renderSetup( mode ):
        if not mode in modes:
                confirmDialog( title = 'Error!', message = 'Unknown layer type!', button = [ 'CANCEL' ] )
                return

        if objExists( mode ) or objExists( mode + '_rgb' ) or objExists( mode + '_hsv' ):
                msg = 'RenderLayer "' + mode + '" already exists. Delete it or rename first.'
                if objectType( mode ) != 'renderLayer':
                        msg = 'Node with the name "' + mode + '" already exists. Delete it or rename first.'
                confirmDialog( title = 'Error!', message = msg, button = [ 'CANCEL' ] )
                return

        # START TIMER
        startTime = time.clock()

        # CREATE LAYER
        if mode == 'env':
                sag_renderSetup_create( 'env', 
                                        glob = 1, 
                                        mvec = 1,
                                        fg = 1,
                                        gamma = 0.4545, 
                                        scan = 0,
                                        rayt = 1,
                                        exr = 'all',
                                        camBg = [0,0,0],
                                        keep = ['envs'] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling, additional parts of environment!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        elif mode == 'chars':
                sag_renderSetup_create( 'chars', 
                                        glob = 1, 
                                        mvec = 1,
                                        fg = 1,
                                        gamma = 0.4545, 
                                        scan = 0,
                                        rayt = 1,
                                        exr = 'all',
                                        camBg = [0,0,0],
                                        hair = 2,
                                        keep = ['envs','chars'],
                                        primVisOff = ['envs'] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, additional character props! Remove furry characters! Set lighting!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'furry':
                sag_renderSetup_create( 'furry', 
                                        glob = 1, 
                                        mvec = 1,
                                        fg = 0,
                                        gamma = 0.4545, 
                                        scan = 3,
                                        rayt = 1,
                                        exr = 'all',
                                        camBg = [0,0,0],
                                        hair = 2,
                                        keep = ['envs','chars'],
                                        primVisOff = ['envs'] )	

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, additional character props! Remove hairy characters! Set lighting!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'occl':
                sag_renderSetup_create( 'occl', 
                                        glob = 1, 
                                        mvec = 0, 
                                        fg = 0, 
                                        gamma = 1.0, 
                                        scan = 0, 
                                        rayt = 1, 
                                        exr = 'disable', 
                                        camBg = [1,1,1],
                                        hair = 0,
                                        keep = ['envs','chars'],
                                        primVisOff = ['chars'],
                                        shade = [['chars','black_SHD'], ['envs','occl_SHD']] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling, additional parts of environment!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'shadow':
                sag_renderSetup_create( 'shadow', 
                                        glob = 1, 
                                        mvec = 0, 
                                        fg = 0, 
                                        gamma = 1.0, 
                                        scan = 0, 
                                        rayt = 1, 
                                        exr = 'disable', 
                                        camBg = [1,1,1],
                                        hair = 0,
                                        keep = ['envs','chars'],
                                        primVisOff = ['chars'],
                                        shade = [['chars','black_SHD'], ['envs','shadow_SHD']] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling, additional parts of environment! Make sure proper lightRig is enabled!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'crossMask':
                sag_renderSetup_create( 'crossMask', 
                                        glob = 1, 
                                        mvec = 0, 
                                        fg = 0, 
                                        gamma = 1.0, 
                                        scan = 0, 
                                        rayt = 1, 
                                        exr = 'disable', 
                                        camBg = [0,0,0],
                                        hair = 2,
                                        keep = ['envs','chars'] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling, additional parts of environment! For furry characters switch to Rasterizer and apply "Hair Opacity to Mask"!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'eyeMask':
                sag_renderSetup_create( 'eyeMask_rgb', 
                                        glob = 1, 
                                        mvec = 0, 
                                        fg = 0, 
                                        gamma = 1.0, 
                                        scan = 0, 
                                        rayt = 1, 
                                        exr = 'disable', 
                                        camBg = [0,0,0],
                                        hair = 0,
                                        keep = ['chars'] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'dofReference':
                sag_renderSetup_create( 'dofReference', 
                                        glob = 1, 
                                        mvec = 0,
                                        fg = 1,
                                        gamma = 0.4545, 
                                        scan = 0,
                                        rayt = 1,
                                        exr = 'disable',
                                        camBg = [0,0,0],
                                        hair = 0,
                                        keep = ['envs','chars'] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check that central camera (mono mode) is set properly! Optimize lighting!\n\nCreated in: ' + dur, button = [ 'OK' ] )

        if mode == 'lightMask':
                sag_renderSetup_create( 'lightMask', 
                                        glob = 1,
                                        mvec = 0,
                                        fg = 0,
                                        gamma = 1.0,
                                        scan = 0,
                                        rayt = 1,
                                        exr = 'disable',
                                        camBg = [0,0,0],
                                        keep = ['envs'],
                                        shade = [['envs','diffuse_SHD']] )

                dur = sag_renderSetup_timer( startTime )
                confirmDialog( title = 'Reminder!', message = 'Done! Check camera, sampling, additional parts of environment!\nSet proper lighting!\n\nCreated in: ' + dur, button = [ 'OK' ] )

def sag_renderSetup_shade( grp, shd ):
        select( grp, replace = True )
        sag_utils_hiGeo()
        sag_utils_selSG()

        for each in ls( sl = True ):
                conns = listConnections( each + '.miMaterialShader', s = True, d = False, p = True, c = True )
                if conns != None:
                        editRenderLayerAdjustment( each + '.miMaterialShader' )
                        if not isConnected( shd + '.message', each + '.miMaterialShader' ):
                                connectAttr( shd + '.message', each + '.miMaterialShader', force = True )

                conns = listConnections( each + '.miLightMapShader', s = True, d = False, p = True, c = True )
                if conns != None:
                        editRenderLayerAdjustment( each + '.miLightMapShader' )
                        disconnectAttr( conns[1], conns[0] )

                conns = listConnections( each + '.miShadowShader', s = True, d = False, p = True, c = True )
                if conns != None:
                        editRenderLayerAdjustment( each + '.miShadowShader' )
                        disconnectAttr( conns[1], conns[0] )


# PROMPT REPLACEMENT STRING
def sag_renderSetup_prompt( title, message ):
        prompt = promptDialog(
                title = title,
                message = message,
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        inp = ''
        if prompt == 'OK':
                inp = promptDialog( query = True, text = True )
        else:
                inp = None

        return inp


def sag_renderSetup_create( lay, **attrs ):
        # DESELECT EVERYTHING
        select( clear = True )

        # CREATE RENDER LAYER & SET IT'S SETTINGS
        createRenderLayer( name = lay, empty = True, g = attrs['glob'], makeCurrent = True )

        if 'mvec' in attrs:
                editRenderLayerAdjustment( 'miDefaultOptions.forceMotionVectors' )
                setAttr( 'miDefaultOptions.forceMotionVectors', attrs['mvec'] )

        if 'fg' in attrs:
                editRenderLayerAdjustment( 'miDefaultOptions.finalGather' )
                setAttr( 'miDefaultOptions.finalGather', attrs['fg'] )

        if 'gamma' in attrs:
                editRenderLayerAdjustment( 'miDefaultFramebuffer.gamma' )
                setAttr( 'miDefaultFramebuffer.gamma', attrs['gamma'] )

        if 'scan' in attrs:
                editRenderLayerAdjustment( 'miDefaultOptions.scanline' )
                setAttr( 'miDefaultOptions.scanline', attrs['scan'] )

        if 'rayt' in attrs:
                editRenderLayerAdjustment( 'miDefaultOptions.rayTracing' )
                setAttr( 'miDefaultOptions.rayTracing', attrs['rayt'] )

        setAttr( 'defaultRenderGlobals.imageFormat', 51 )
        editRenderLayerAdjustment( 'defaultRenderGlobals.imageFormat' )

        setAttr( 'miDefaultFramebuffer.datatype', 16 )
        editRenderLayerAdjustment( 'miDefaultFramebuffer.datatype' )

        setAttr( 'miDefaultOptions.motionBlur', 0 )
        setAttr( 'mentalrayGlobals.exportCustomMotion', 0 )
        setAttr( 'mentalrayGlobals.exportMotionOffset', 0 )
        setAttr( 'mentalrayGlobals.exportMotionOutput', 0 )

        setAttr( 'defaultRenderGlobals.imageFilePrefix', '', type = 'string' )
        setAttr( 'defaultRenderGlobals.animation', 1 )
        setAttr( 'defaultRenderGlobals.animationRange', 1 )
        setAttr( 'defaultRenderGlobals.startFrame', 1 )
        setAttr( 'defaultRenderGlobals.endFrame', 1 )
        setAttr( 'defaultRenderGlobals.extensionPadding', 4 )
        setAttr( 'defaultRenderGlobals.outFormatControl', 0 )
        setAttr( 'defaultRenderGlobals.enableDefaultLight', 0 )

        # SETUP EXR CUBE
        maya.mel.eval( 'SetupEXRexport' )
        if 'exr' in attrs:
                sag_exrCube( attrs['exr'] )

        # SETUP CAMERAS BACKGROUND
        if 'camBg' in attrs:
                cams = ls( type = ['camera', 'stereoRigCamera'] )
                for cam in [ 'perspShape', 'frontShape', 'sideShape', 'topShape' ]:
                        cams.remove( cam )

                for cam in cams:
                        if listConnections( cam + '.backgroundColorR', s= True, d = False ) == None:
                                editRenderLayerAdjustment( cam + '.backgroundColor' )
                                setAttr( cam + '.backgroundColor', attrs['camBg'][0], attrs['camBg'][1], attrs['camBg'][2], type = 'double3' )

        # SORT OBJECTS IN THE ROOT OF THE SCENE
        roots = { 'cams':[], 'envs':[], 'chars':[], 'misc':[] }
        core = ['exrLayerCube', 'persp', 'top', 'side', 'front']

        for each in ls( '|*', type = 'transform' ) + ls( '|*:*', type = 'transform', long = True ) + ls( '|*:*:*', type = 'transform' ):
                if referenceQuery( each, isNodeReferenced = True ):
                        filePath = referenceQuery( each, filename = True )
                        if each.find( 'shot:cam:' ) > -1:
                                roots['cams'].append( each )
                        elif 'locations_compilation' in filePath.lower():
                                roots['envs'].append( each )
                        elif 'characters' in filePath.lower():
                                roots['chars'].append( each )
                        else:
                                roots['misc'].append( each )
                else:
                        if not each in core:
                                roots['misc'].append( each )

        # HIDE ALL ROOT OBJECTS EXCEPT FOR NEEDED ONES
        if 'keep' in attrs:
                toHide = roots['misc'][:]
                if not 'envs' in attrs['keep']:
                        toHide += roots['envs']
                if not 'chars' in attrs['keep']:
                        toHide += roots['chars']
                for each in toHide:
                        setAttr( each + '.v', 0 )

        # TURN OFF PRIMARY VISIBILITY FOR SPECIFIED TYPES
        if 'primVisOff' in attrs:
                for each in attrs['primVisOff']:
                        for eachRoot in roots[each]:
                                select( eachRoot, replace = True )
                                sag_utils_hiGeo()
                                for eachGeo in ls( sl = True ):
                                        setAttr( eachGeo + '.primaryVisibility', 0 )
                select( clear = True )

        # ASSIGN NEW SHADING TO SPECIFIED TYPES
        if 'shade' in attrs:
                sag_auxShaders()
                for eachPair in attrs['shade']:
                        for eachRoot in roots[eachPair[0]]:
                                sag_renderSetup_shade( eachRoot, eachPair[1] )
                select( clear = True )

        # SET HAIR MODE
        headCtrls = ls( '*head_control' ) + ls( '*:head_control' ) + ls( '*:*:head_control' ) + ls( '*:*:*:head_control' ) + ls( '*:*:*:*:head_control' ) + ls( '*:*:*:*:*:head_control' )
        if 'hair' in attrs:
                for each in headCtrls:
                        if attributeQuery( 'hair', node = each, exists = True ):
                                editRenderLayerAdjustment( each + '.hair' )
                                setAttr( each + '.hair', attrs['hair'] )

        # ENV
        if lay == 'env':
                if objExists( 'env_lights_grp' ):
                        setAttr( 'env_lights_grp.v', 1 )

        # CHARS
        if lay in ['chars', 'furry']:
                for eachRoot in roots['envs']:
                        select( eachRoot, replace = True )
                        sag_utils_hiGeo()
                        sag_utils_castReceiveOverride( 'set', ['miTransparencyCast', 'transparency'] )
                select( clear = True )
                if lay == 'furry':
                        setAttr( 'miDefaultOptions.rapidSamplesCollect', 10 )
                        #editRenderLayerAdjustment( 'miDefaultOptions.rapidSamplesCollect' )

                        setAttr( 'miDefaultOptions.rapidSamplesShading', 6 )
                        #editRenderLayerAdjustment( 'miDefaultOptions.rapidSamplesShading' )

                        inds = getAttr( 'miDefaultOptions.stringOptions', multiIndices = True )
                        for ind in inds:
                                if getAttr( 'miDefaultOptions.stringOptions[' + str(ind) + '].name' ) == 'rast transparency depth':
                                        if int(getAttr( 'miDefaultOptions.stringOptions[' + str(ind) + '].value' )) < 64:
                                                setAttr( 'miDefaultOptions.stringOptions[' + str(ind) + '].value', 64, type = 'string' )
                elif lay == 'chars':
                        editRenderLayerAdjustment( 'miDefaultOptions.maxSamples' )
                        setAttr( 'miDefaultOptions.maxSamples', 3 )

                        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherRays' )
                        setAttr( 'miDefaultOptions.finalGatherRays', 750 )

                        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPresampleDensity' )
                        setAttr( 'miDefaultOptions.finalGatherPresampleDensity', 1.0 )

                        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPoints' )
                        setAttr( 'miDefaultOptions.finalGatherPoints', 20 )

                        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherTraceDiffuse' )
                        setAttr( 'miDefaultOptions.finalGatherTraceDiffuse', 0 )

        # OCCL AND SHADOW
        if lay in ['occl', 'shadow'] :
                for eachRoot in roots['envs']:
                        select( eachRoot, replace = True )
                        sag_utils_hiGeo()
                        if lay == 'occl':
                                for eachGeo in ls( sl = True ):
                                        eachPar = listRelatives( eachGeo, parent = True, fullPath = True )[0]
                                        if not attributeQuery( 'miLabel', node = eachPar, exists = True ):
                                                addAttr( eachPar, ln = 'miLabel', at = 'long', keyable = True, dv = 13 )
                                        else:
                                                editRenderLayerAdjustment( eachPar + '.miLabel' )
                                                setAttr( eachPar + '.miLabel', 13 )
                        elif lay == 'shadow':
                                sag_utils_castReceiveOverride( 'set', ['castsShadows', 'shadow'] )
                                if objExists( 'env_lights_grp' ):
                                        setAttr( 'env_lights_grp.v', 1 )
                select( clear = True )

        # CROSSMASK
        rgbShd = ['red_SHD', 'green_SHD', 'blue_SHD']
        if lay in ['crossMask']:
                for eachRoot in roots['envs']:
                        sag_renderSetup_shade( eachRoot, 'black_SHD' )

                i = 0
                for eachRoot in roots['chars']:
                        sag_renderSetup_shade( eachRoot, rgbShd[(i%3)] )
                        i += 1

        #EYEMASK
        if lay in ['eyeMask_rgb']:
                dup = duplicate( 'eyeMask_rgb', ic = True, name = 'eyeMask_hsv' )
                for eachLay in [ 'eyeMask_rgb', 'eyeMask_hsv' ]:
                        editRenderLayerGlobals( crl = eachLay )

                        for eachRoot in roots['chars']:
                                select( eachRoot, replace = True )
                                sag_utils_hiGeo()
                                eyes = []
                                allTrs = []
                                for eachGeo in ls( sl = True, long = True ):
                                        trs = listRelatives( eachGeo, parent = True )[0]
                                        allTrs.append( trs )
                                        for par in eachGeo.split( '|' )[1:]:
                                                hist = listHistory( par )
                                                for eachHist in hist:
                                                        if eachHist in headCtrls:
                                                                if not getAttr( trs + '.v', l = True ):
                                                                        setAttr( trs + '.v', 0 )
                                        if eachGeo.find( 'eye' ) > -1 and eachGeo.find( 'GlassShape' ) > -1:
                                                eyes.append( trs )
                                select( eyes, replace = True )
                                sag_eyeMasks( eachLay.split( '_' )[-1] )

                                allTrs = list( set( allTrs ) )
                                for eachEye in eyes:
                                        allTrs.remove( eachEye )
                                sag_renderSetup_shade( allTrs, 'black_SHD' )

        #DOFREFERENCE
        if lay in ['dofReference']:
                if objExists( 'env_lights_grp' ):
                        setAttr( 'env_lights_grp.v', 1 )

                focDist = sag_renderSetup_prompt( 'Focus Distance', 'Input focus distance:' )
                if focDist == None or focDist == '':
                        focDist = 100

                for cam in cams:
                        if listConnections( cam + '.depthOfField', s = True, d = False ) == None:
                                editRenderLayerAdjustment( cam + '.depthOfField' )
                                setAttr( cam + '.depthOfField', 1 )
                        if listConnections( cam + '.focusDistance', s = True, d = False ) == None:
                                editRenderLayerAdjustment( cam + '.focusDistance' )
                                setAttr( cam + '.focusDistance', float(focDist) )
                        if listConnections( cam + '.fStop', s = True, d = False ) == None:
                                editRenderLayerAdjustment( cam + '.fStop' )
                                setAttr( cam + '.fStop', 2 )
                        if listConnections( cam + '.focusRegionScale', s = True, d = False ) == None:
                                editRenderLayerAdjustment( cam + '.focusRegionScale' )
                                setAttr( cam + '.focusRegionScale', 1 )

                        editRenderLayerAdjustment( cam + '.renderable' )
                        if cam == 'shot:cam:CCenterCamShape':
                                setAttr( cam + '.renderable', 1 )
                        else:
                                setAttr( cam + '.renderable', 0 )

                editRenderLayerAdjustment( 'miDefaultOptions.maxSamples' )
                setAttr( 'miDefaultOptions.maxSamples', 2 )

                editRenderLayerAdjustment( 'miDefaultOptions.finalGatherRays' )
                setAttr( 'miDefaultOptions.finalGatherRays', 100 )

                editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPresampleDensity' )
                setAttr( 'miDefaultOptions.finalGatherPresampleDensity', 1.0 )

                editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPoints' )
                setAttr( 'miDefaultOptions.finalGatherPoints', 10 )

                editRenderLayerAdjustment( 'miDefaultOptions.finalGatherTraceDiffuse' )
                setAttr( 'miDefaultOptions.finalGatherTraceDiffuse', 2 )
