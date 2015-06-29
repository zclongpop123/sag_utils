#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:25:44
#========================================
from maya.cmds import *
from sag_utils import *
from sag_exrCube import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def sag_eyeMasks( mode ):
        if mode in [ 'rgb', 'hsv' ]:
                sag_utils_hiGeo()
                sag_utils_selSG()

                sgList = ls( sl = True )

                for sg in sgList:
                        hist = listHistory( sg )

                        eyeShd = ''
                        glassShd = ''
                        for each in hist:
                                if nodeType( each ) == 'eyeShader':
                                        eyeShd = each
                                elif nodeType( each ) == 'p_MegaTK':
                                        glassShd = each

                        if glassShd != '':
                                refr_shd = glassShd.replace( ':', '_' ) + '_eyeMask_rgb_refract'
                                if not objExists( refr_shd ):
                                        shadingNode( 'mib_refract', asUtility = True, name = refr_shd )
                                setAttr( refr_shd + '.refract', 1, 1, 1, type = 'double3' )
                                if not isConnected( glassShd + '.ior_in_refr', refr_shd + '.ior' ):
                                        connectAttr( glassShd + '.ior_in_refr', refr_shd + '.ior', force = True )
                                if not isConnected( refr_shd + '.outValue', sg + '.miMaterialShader' ):
                                        editRenderLayerAdjustment( sg + '.miMaterialShader' )
                                        connectAttr( refr_shd + '.outValue', sg + '.miMaterialShader', force = True )

                        if eyeShd != '':
                                if mode == 'rgb':
                                        # RGB MASK
                                        red = [ '.pupilColor' ]
                                        green = [ '.centerColor1', '.centerColor2', '.peripheryColor1', '.peripheryColor2', '.middleRingColor1', '.middleRingColor2', '.bigRingColor1', '.bigRingColor2', '.smallRingColor1', '.smallRingColor2' ]
                                        blue = [ '.scleraColor1', '.scleraColor2', '.bloodVesselColor' ]

                                        eyeDup = eyeShd.replace( ':', '_' ) + '_eyeMask_rgb'
                                        if not objExists( eyeDup ):
                                                eyeDupTmp = duplicate( eyeShd, ic = True )[0]
                                                rename( eyeDupTmp, eyeDup )

                                        for attr in red + green + blue:
                                                conns = listConnections( eyeDup + attr, s = True, d = False, p = True )
                                                if conns != None:
                                                        disconnectAttr( conns[0], eyeDup + attr )
                                                setAttr( eyeDup + attr, attr in red, attr in green, attr in blue, type = 'double3' )

                                        conns = listConnections( sg + '.miMaterialShader', s = True, d = False, p = True, c = True )
                                        if conns != None:
                                                if not isConnected( eyeDup + '.message', sg + '.miMaterialShader' ):
                                                        editRenderLayerAdjustment( sg + '.miMaterialShader' )
                                                        connectAttr( eyeDup + '.message', sg + '.miMaterialShader', force = True )

                                        conns = listConnections( sg + '.miLightMapShader', s = True, d = False, p = True, c = True )
                                        if conns != None:
                                                editRenderLayerAdjustment( sg + '.miLightMapShader' )
                                                disconnectAttr( conns[1], conns[0] )

                                        conns = listConnections( sg + '.miShadowShader', s = True, d = False, p = True, c = True )
                                        if conns != None:
                                                editRenderLayerAdjustment( sg + '.miShadowShader' )
                                                disconnectAttr( conns[1], conns[0] )

                                elif mode == 'hsv':
                                        # HSV MASK
                                        hsv_mask = 'hsv_mask'
                                        hsv_gamma = 'hsv_mask_gamma'
                                        hsvToRgb = 'hsv_mask_hsvToRgb'
                                        h_ramp = 'hsv_mask_hRamp'
                                        sv_ramp = 'hsv_mask_svRamp'
                                        hsv_place2d = 'hsv_mask_place2d'

                                        if not objExists( hsv_mask ):
                                                shadingNode( 'gluk_constant', asShader = True, name = hsv_mask )
                                        if not isConnected( hsv_mask + '.message', sg + '.miMaterialShader' ):
                                                editRenderLayerAdjustment( sg + '.miMaterialShader' )
                                                connectAttr( hsv_mask + '.message', sg + '.miMaterialShader', force = True )

                                        if not objExists( hsv_gamma ):
                                                shadingNode( 'gammaCorrect', asUtility = True, name = hsv_gamma )
                                                setAttr( hsv_gamma + '.gamma', 0.4545, 0.4545, 0.4545, type = 'double3' )
                                                connectAttr( hsv_gamma + '.outValue', hsv_mask + '.color', force = True )

                                        if not objExists( hsvToRgb ):
                                                shadingNode( 'hsvToRgb', asUtility = True, name = hsvToRgb )
                                                connectAttr( hsvToRgb + '.outRgb', hsv_gamma + '.value', force = True )

                                        if not objExists( h_ramp ):
                                                shadingNode( 'ramp', asTexture = True, name = h_ramp )
                                                removeMultiInstance( h_ramp + '.colorEntryList[1]', b = True )
                                                setAttr( h_ramp + '.colorEntryList[0].color', 0, 0, 0, type = 'double3' )
                                                setAttr( h_ramp + '.colorEntryList[2].color', 360, 0, 0, type = 'double3' )
                                                setAttr( h_ramp + '.colorEntryList[2].position', 1 )
                                                setAttr( h_ramp + '.type', 3 )
                                                connectAttr( h_ramp + '.outColor', hsvToRgb + '.inHsv', force = True )

                                        if not objExists( sv_ramp ):
                                                shadingNode( 'ramp', asTexture = True, name = sv_ramp )
                                                removeMultiInstance( h_ramp + '.colorEntryList[1]', b = True )
                                                setAttr( sv_ramp + '.colorEntryList[0].color', 0, 0, 1, type = 'double3' )
                                                setAttr( sv_ramp + '.colorEntryList[2].color', 0, 1, 1, type = 'double3' )
                                                setAttr( sv_ramp + '.colorEntryList[2].position', 0.7 )
                                                setAttr( sv_ramp + '.type', 4 )
                                                connectAttr( sv_ramp + '.outColor', h_ramp + '.colorOffset', force = True )

                                        if not objExists( hsv_place2d ):
                                                shadingNode( 'place2dTexture', asUtility = True, name = hsv_place2d )
                                                setAttr( hsv_place2d + '.rotateUV', -90 )
                                                connectAttr( hsv_place2d + '.outUV', h_ramp + '.uvCoord', force = True )
                                                connectAttr( hsv_place2d + '.outUV', sv_ramp + '.uvCoord', force = True )
                                                connectAttr( hsv_place2d + '.outUvFilterSize', h_ramp + '.uvFilterSize', force = True )
                                                connectAttr( hsv_place2d + '.outUvFilterSize', sv_ramp + '.uvFilterSize', force = True )


        elif mode == 'layer':
                editRenderLayerAdjustment( 'miDefaultOptions.forceMotionVectors' )
                setAttr( 'miDefaultOptions.forceMotionVectors', 0 )

                editRenderLayerAdjustment( 'miDefaultOptions.finalGather' )
                setAttr( 'miDefaultOptions.finalGather', 0 )

                editRenderLayerAdjustment( 'miDefaultFramebuffer.gamma' )
                setAttr( 'miDefaultFramebuffer.gamma', 1.0 )

                sag_exrCube( "disable" )
