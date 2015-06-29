#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:18:35
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_shadInShad( mode ):
        selList = ls( sl = True )

        if mode == 'create':
                if not objExists( 'shadow_SHD' ):
                        shadingNode( 'mip_matteshadow', asShader = True, name = 'shadow_SHD' )
                        setAttr( 'shadow_SHD.background', 1, 1, 1, type = 'double3' )
                        setAttr( 'shadow_SHD.ao_on', 0 )

                feedback = []
                for each in selList:
                        if nodeType( each ) == 'shadingEngine':
                                mega = ''
                                conns = listConnections( each + '.miMaterialShader', s = True, d = False )

                                if conns != None:
                                        if nodeType( conns[0] ) == 'p_maya_shadingengine':
                                                sheConns = listConnections( conns[0] + '.inColor', s = True, d = False )
                                                if sheConns != None:
                                                        if nodeType( sheConns[0] ) == 'p_MegaTK':
                                                                mega = sheConns[0]
                                                        else:
                                                                feedback.append( 'No p_MegaTK shader connected to ' + each )
                                        elif nodeType( conns[0] ) == 'p_MegaTK':
                                                mega = conns[0]
                                        else:
                                                feedback.append( 'No shaders_p network connected to ' + each )
                                else:
                                        feedback.append( 'No shading network connected to ' + each )

                                if each != 'initialShadingGroup' and each != 'initialParticleSE':
                                        if editRenderLayerGlobals( query = True, crl = True ) != 'defaultRenderLayer':
                                                editRenderLayerAdjustment( each + '.miMaterialShader' )
                                        connectAttr( 'shadow_SHD.message', each + '.miMaterialShader', force = True )

                                if mega != '':
                                        bumpConn = listConnections( mega + '.input_normal', s = True, d = False, p = True )

                                        if bumpConn != None:
                                                she = createNode( 'p_maya_shadingengine', name = mega.split( ':' )[-1] + '_shadow_SHE' )
                                                connectAttr( 'shadow_SHD.result', she + '.inColor' )
                                                connectAttr( bumpConn[0], she + '.inputNormal' )
                                                connectAttr( mega + '.use_normal', she + '.useNormal' )
                                                connectAttr( she + '.message', each + '.miMaterialShader', force = True )

                                lmapConn = listConnections( each + '.miLightMapShader', s = True, d = False, c = True, p = True )
                                if lmapConn != None:
                                        editRenderLayerAdjustment( each + '.miLightMapShader' )
                                        disconnectAttr( lmapConn[1], lmapConn[0] )

                                shadConn = listConnections( each + '.miShadowShader', s = True, d = False, c = True, p = True )
                                if lmapConn != None:
                                        editRenderLayerAdjustment( each + '.miShadowShader' )
                                        disconnectAttr( shadConn[1], shadConn[0] )

                for each in feedback:
                        print each
