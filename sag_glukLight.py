#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:23:19
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_glukLight():
        selList = ls( sl = True )

        lights = [ 'directionalLight', 'pointLight', 'spotLight', 'areaLight' ]

        for each in selList:
                attrs = [ '.color', '.emitDiffuse', '.emitSpecular', '.intensity', '.rayDepthLimit', '.shadowColor', '.shadowRays', '.useRayTraceShadows' ]

                if nodeType( each ) == 'transform':
                        shp = listRelatives( each, shapes = True )
                        if shp != None:
                                each = shp[0]

                if nodeType( each ) in lights:
                        if listConnections( each + '.miLightShader', s = True, d = False ) == None:

                                if nodeType( each ) == 'directionalLight':
                                        lShd = shadingNode( 'gluk_light_direct', asUtility = True, name = each + '_gluk_direct' )

                                        attrs += [ '.lightAngle', '.useLightPosition' ]
                                        for attr in attrs:
                                                connectAttr( each + attr, lShd + attr, force = True )

                                elif nodeType( each ) == 'pointLight':
                                        lShd = shadingNode( 'gluk_light_point', asUtility = True, name = each + '_gluk_point' )
                                        setAttr( lShd + '.decayRate', getAttr( each + '.decayRate' ) )

                                        attrs += [ '.lightRadius' ]
                                        for attr in attrs:
                                                connectAttr( each + attr, lShd + attr, force = True )

                                elif nodeType( each ) == 'spotLight':
                                        lShd = shadingNode( 'gluk_light_spot', asUtility = True, name = each + '_gluk_spot' )
                                        setAttr( lShd + '.decayRate', getAttr( each + '.decayRate' ) )

                                        attrs += [ '.lightRadius', '.coneAngle', '.dropoff', '.penumbraAngle' ]
                                        for attr in attrs:
                                                connectAttr( each + attr, lShd + attr, force = True )

                                elif nodeType( each ) == 'areaLight':
                                        lShd = shadingNode( 'gluk_light_area', asUtility = True, name = each + '_gluk_area' )
                                        connectAttr( each + '.areaShapeIntensity', lShd + '.shapeIntensity', force = True )
                                        setAttr( lShd + '.decayRate', getAttr( each + '.decayRate' ) )

                                        for attr in attrs:
                                                connectAttr( each + attr, lShd + attr, force = True )

                                connectAttr( lShd + '.message', each + '.miLightShader', force = True )

        select( selList, replace = True )
