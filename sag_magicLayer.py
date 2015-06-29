#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:21:24
#========================================
from maya.cmds import *
from sag_exrCube import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_magicLayer( envName ):
        select( clear = True )

        # ENVIRONMENT TO TURN INTO MAGIC
        env = [ 'shot:Ridge:location', 's:/SAVVA/Locations_Compilation/Woodland/Ridge/data/Ridge_magic_shading.mb' ]
        if envName == 'Forest_Night_02':
                env = [ 'shot:Forest_Night_02:location', 's:/SAVVA/Locations_Compilation/Woodland/Forest_Night_02/data/Forest_Night_02_magic_shading.mb' ]
        elif envName == 'Angatsetus_field':
                env = [ 'shot:Angatsetus_field:location', 's:/SAVVA/Locations_Compilation/Woodland/Angatsetus_field/data/Angatsetus_field_magic_shading.mb' ]

        # CREATE RENDER LAYER MAGIC
        createRenderLayer( name = 'magic', empty = True, g = True, makeCurrent = True )

        editRenderLayerAdjustment( 'miDefaultOptions.forceMotionVectors' )
        setAttr( 'miDefaultOptions.forceMotionVectors', 0 )

        editRenderLayerAdjustment( 'miDefaultOptions.finalGather' )
        setAttr( 'miDefaultOptions.finalGather', 1 )

        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherRays' )
        setAttr( 'miDefaultOptions.finalGatherRays', 300 )

        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPresampleDensity' )
        setAttr( 'miDefaultOptions.finalGatherPresampleDensity', 0.3 )

        editRenderLayerAdjustment( 'miDefaultOptions.finalGatherPoints' )
        setAttr( 'miDefaultOptions.finalGatherPoints', 20 )

        editRenderLayerAdjustment( 'miDefaultFramebuffer.gamma' )
        setAttr( 'miDefaultFramebuffer.gamma', 1.0 )

        editRenderLayerAdjustment( 'miDefaultOptions.scanline' )
        setAttr( 'miDefaultOptions.scanline', 0 )

        editRenderLayerAdjustment( 'miDefaultOptions.rayTracing' )
        setAttr( 'miDefaultOptions.rayTracing', 1 )

        sag_exrCube( 'masks' )

        # HIDE ALL ROOT OBJECTS EXCEPT FOR SOME SPECIFIC ONES
        for each in ls( '|*', type = 'transform' ) + ls( '|*:*', type = 'transform', long = True ) + ls( '|*:*:*', type = 'transform' ):
                if not each in [ env[0], 'exrLayerCube', 'persp', 'top', 'side', 'front' ] and each.find( 'shot:cam:' ) < 0:
                        setAttr( each + '.v', 0 )

        # REFERENCE MAGIC NETWORK
        file( env[1], reference = True, namespace = 'magic_shading' )
        nm = file( env[1], query = True, namespace = True )

        # ASSIGN DEFAULT RAYSWITCH TO EVERYTHING
        envSGs = ls( env[0][:env[0].rfind(':')] + ':*', type = 'shadingEngine' ) + ls( env[0][:env[0].rfind(':')] + ':*:*', type = 'shadingEngine' ) + ls( env[0][:env[0].rfind(':')] + ':*:*:*', type = 'shadingEngine' ) + ls( env[0][:env[0].rfind(':')] + ':*:*:*:*', type = 'shadingEngine' )

        shd = nm + ':magic_0_default_rayswitch'

        if objExists( shd ):
                for each in envSGs:
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

        # ASSIGN SPECIFIC RAYSWITCHES
        raySwchs = ls( nm + ':magic*', type = 'mip_rayswitch' )
        raySwchs.remove( shd )

        for each in raySwchs:
                sgs = getAttr( each + '.magic_sg' ).split()
                for sg in sgs:
                        connectAttr( each + '.message', sg + '.miMaterialShader', force = True )


def sag_magicLayer_promptReplace():
        prompt = promptDialog(
                title = 'Indices',
                message = 'Input elements to create fg layers for (e.g. 3 4 9):',
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        ind = ''
        if prompt == 'OK':
                ind = promptDialog( query = True, text = True )

        return ind


def sag_magicFGLayer( mode, chanList ):
        if mode:
                ind = sag_magicLayer_promptReplace()
                if ind != '':
                        chanList = ind.split()
                else:
                        confirmDialog( title = 'Error', message = 'Incorrect numbers specified!', button = ['Cancel'] )
                        return

        for chan in chanList:
                rLay = duplicate( 'magic', inputConnections = True )
                rLay = rename( rLay, 'magic_' + str( chan ) + '_fg' )
                editRenderLayerGlobals( currentRenderLayer = rLay )

                sag_exrCube( 'disable' )

                ibl = listConnections( 'mentalrayGlobals.imageBasedLighting', s = True, d = False )
                if ibl != None:
                        editRenderLayerAdjustment( ibl[0] + '.colorGain' )
                        setAttr( ibl[0] + '.colorGain', 0, 0, 0, type = 'double3' )

                for shd in ls( 'magic_shading:*', type = 'mip_rayswitch' ):
                        if not ('magic_shading:magic_' + str( chan ) + '_') in shd:
                                conn = listConnections( shd + '.finalgather', s = True, d = False, c = True, p = True )
                                if conn != None:
                                        editRenderLayerAdjustment( shd + '.finalgather' )
                                        disconnectAttr( conn[1], conn[0] )
