#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:26:06
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def sag_exrCube( mode ):
        attrList = [ 'mr_z_pass', 
                     'mr_normal_pass', 
                     'mr_motion_pass', 
                     'mr_label_pass', 
                     'mr_coverage_pass', 
                     'shading_pass', 
                     'color_occlusion_pass', 
                     'diffuse_pass', 
                     'diffuse_shadow_pass',
                     'specular_pass',
                     'specular_shadow_pass',
                     'occlusion_pass',
                     'indirect_illum_pass',
                     'amb_occlusion_pass',
                     'ambient_pass',
                     'reflect_pass',
                     'refract_pass',
                     'incandescence_pass',
                     'z_pass',
                     'bent_normal_pass',
                     'specialC1_pass',
                     'specialC2_pass',
                     'specialC3_pass',
                     'specialC4_pass',
                     'specialC5_pass',
                     'specialC6_pass',
                     'specialC7_pass',
                     'specialC8_pass',
                     'specialC9_pass',
                     'specialC10_pass',
                     'specialC11_pass',
                     'specialC12_pass',
                     'specialC13_pass',
                     'specialC14_pass',
                     'specialC15_pass' ]

        selList = ls( type = 'p_MegaTK_pass' )

        for each in selList:
                for eachAttr in attrList:
                        if mode == 'disable':
                                editRenderLayerAdjustment( each + '.' + eachAttr )
                                setAttr( each + '.' + eachAttr, 0 )
                        elif mode == 'clear':
                                editRenderLayerAdjustment( each + '.' + eachAttr, remove = True )
                        elif mode == 'masks':
                                editRenderLayerAdjustment( each + '.' + eachAttr )
                                if attrList.index( eachAttr ) > 19:
                                        setAttr( each + '.' + eachAttr, 1 )
                                        editRenderLayerAdjustment( each + '.' + eachAttr.split('_')[0] + '_float' )
                                        setAttr( each + '.' + eachAttr.split('_')[0] + '_float', 0 )
                                else:
                                        setAttr( each + '.' + eachAttr, 0 )
                        elif mode == 'all':
                                editRenderLayerAdjustment( each + '.' + eachAttr )
                                val = 1
                                if attrList.index( eachAttr ) in [2, 3, 4, 13, 14, 18, 19]:
                                        val = 0
                                setAttr( each + '.' + eachAttr, val )
