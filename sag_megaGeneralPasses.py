#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:21:03
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_megaGeneralPasses():
        # CREATE NETWORKS FOR MASKS
        mt_shd = 'motion_SHD'
        samp_info = 'samp_info'
        U_ramp = 'U_ramp'
        V_ramp = 'V_ramp'
        inc_ramp = 'inc_reverse'
        hair_ramp = 'hair_ramp'
        hair_map = 'hair_map'
        place2d = 'UV_ramp_place2d'

        if not objExists( mt_shd ):
                shadingNode( 'p_motion_to_rgb', asShader = True, name = mt_shd )
                setAttr( mt_shd + '.mode', 4 )

        if not objExists( samp_info ):
                shadingNode( 'samplerInfo', asUtility = True, name = samp_info )

        if not objExists( U_ramp ):
                shadingNode( 'ramp', asTexture = True, name = U_ramp )
                removeMultiInstance( U_ramp + '.colorEntryList[1]', b = True )
                setAttr( U_ramp + '.colorEntryList[0].color', 0, 0, 0, type = 'double3' )
                setAttr( U_ramp + '.colorEntryList[2].color', 1, 0, 0, type = 'double3' )
                setAttr( U_ramp + '.colorEntryList[2].position', 1 )
                setAttr( U_ramp + '.type', 1 )

        if not objExists( V_ramp ):
                shadingNode( 'ramp', asTexture = True, name = V_ramp )
                removeMultiInstance( V_ramp + '.colorEntryList[1]', b = True )
                setAttr( V_ramp + '.colorEntryList[0].color', 0, 0, 0, type = 'double3' )
                setAttr( V_ramp + '.colorEntryList[2].color', 0, 1, 0, type = 'double3' )
                setAttr( V_ramp + '.colorEntryList[2].position', 1 )
                setAttr( V_ramp + '.type', 0 )
                connectAttr( V_ramp + '.outColor', U_ramp + '.colorOffset' )

        if objExists( 'inc_ramp' ):
                delete( 'inc_ramp' )
        if not objExists( inc_ramp ):
                shadingNode( 'reverse', asUtility = True, name = inc_ramp )
                connectAttr( inc_ramp + '.outputZ', V_ramp + '.colorOffsetB' )
                connectAttr( samp_info + '.facingRatio', inc_ramp + '.inputZ' )

        if not objExists( hair_ramp ):
                shadingNode( 'ramp', asTexture = True, name = hair_ramp )
                removeMultiInstance( hair_ramp + '.colorEntryList[1]', b = True )
                setAttr( hair_ramp + '.colorEntryList[0].color', 1, 0, 0, type = 'double3' )
                setAttr( hair_ramp + '.colorEntryList[2].color', 0, 1, 0, type = 'double3' )
                setAttr( hair_ramp + '.colorEntryList[2].position', 1 )
                setAttr( hair_ramp + '.type', 0 )

        if not objExists( hair_map ):
                createNode( 'p_hair_mapping', name = hair_map )
                connectAttr( hair_map + '.outValue', hair_ramp + '.vCoord' )

        if not objExists( place2d ):
                shadingNode( 'place2dTexture', asUtility = True, name = place2d )
                for each in [ U_ramp, V_ramp ]:
                        connectAttr( place2d + '.outUV', each + '.uvCoord' )
                        connectAttr( place2d + '.outUvFilterSize', each + '.uvFilterSize' )

        # CONNECT TO PUPPET SHADERS
        selList = ls( type = 'p_MegaTK' )
        selList += ls( type = 'p_HairTK' )
        selList += ls( type = 'gluk_hair' )

        for each in selList:
                if not isConnected( mt_shd + '.outValue', each + '.specialC1' ):
                        connectAttr( mt_shd + '.outValue', each + '.specialC1' )
                        setAttr( each + '.use_SpecialC1', 1 )

                if not isConnected( samp_info + '.pointWorld', each + '.specialC2' ):
                        connectAttr( samp_info + '.pointWorld', each + '.specialC2', force = True )
                        setAttr( each + '.use_SpecialC2', 1 )

                if objectType( each ) == 'p_MegaTK':
                        if not isConnected( U_ramp + '.outColor', each + '.specialC10' ):
                                connectAttr( U_ramp + '.outColor', each + '.specialC10', force = True )
                                setAttr( each + '.use_SpecialC10', 1 )
                else:
                        if not isConnected( hair_ramp + '.outColor', each + '.specialC10' ):
                                connectAttr( hair_ramp + '.outColor', each + '.specialC10', force = True )
                                setAttr( each + '.use_SpecialC10', 1 )
