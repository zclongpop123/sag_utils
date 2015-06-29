#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:18:52
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
nodeTypes = [ 'mib_texture_lookup', 'mib_texture_lookup2', 'mib_bump_map2' ]

def sag_reTex():
        selList = ls( selection = True )

        outNodes = []
        for each in selList:
                tex = shadingNode( 'file', asTexture = True )
                setAttr( tex + '.filterType', 1 )
                setAttr( tex + '.filter', 0.5 )
                setAttr( tex + '.defaultColor', 0, 0, 0, type = 'double3' )

                plc = shadingNode( 'place2dTexture', asUtility = True )
                connectAttr( plc + '.outUV', tex + '.uvCoord' )
                connectAttr( plc + '.outUvFilterSize', tex + '.uvFilterSize' )
                for attr in [ 'coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger', 'wrapU', 'wrapV', 'repeatUV', 'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne', 'noiseUV', 'offset', 'rotateUV' ]:
                        connectAttr( plc + '.' + attr, tex + '.' + attr )

                if objectType( each ) in nodeTypes:
                        if objectType( each ) == 'mib_texture_lookup2':
                                repeatU = getAttr( each + '.factor' )
                                repeatV = repeatU
                        elif objectType( each ) == 'mib_texture_lookup':
                                repeatU = getAttr( listConnections( each + '.coord', s = True, d = False )[0] + '.repeatX' )
                                repeatV = getAttr( listConnections( each + '.coord', s = True, d = False )[0] + '.repeatY' )
                        elif objectType( each ) == 'mib_bump_map2':
                                repeatU = getAttr( each + '.scale' )
                                repeatV = repeatU
                        setAttr( plc + '.repeatU', repeatU )
                        setAttr( plc + '.repeatV', repeatV )

                        conn = listConnections( each + '.tex', s = True, d = False )[0]
                        filePath = getAttr( conn + '.fileTextureName' )
                        setAttr( tex + '.fileTextureName', filePath, type = 'string' )

                        fileName = filePath.replace( '\\', '/' ).split( '/' )[-1].split( '.' )[-2]
                        tex = rename( tex, fileName + '_file' )
                        plc = rename( plc, fileName + '_place2d' )
                        texOut = 'outColor'

                        if objectType( each ) == 'mib_bump_map2':
                                bmp = shadingNode( 'bump2d', asUtility = True, name = fileName + '_bump2d' )
                                connectAttr( tex + '.outColorR', bmp + '.bumpValue' )
                                if getAttr( conn + '.miFilter' ):
                                        setAttr( bmp + '.bumpFilter', getAttr( conn + '.miFilterSize' ) )
                                else:
                                        setAttr( bmp + '.bumpFilter', 0.5 )
                                setAttr( bmp + '.bumpDepth', getAttr( each + '.factor' ) * -1 )
                                tex = bmp
                                texOut = 'outNormal'

                        delete( conn )

                        conns = listConnections( each, s = False, d = True, p = True, c = True )

                        for i in xrange( len( conns ) ):
                                if conns[i].find( 'outValue' ) > -1:
                                        print tex + '.' + texOut + conns[i].split( 'outValue' )[-1] + ' -> ' + conns[i + 1]
                                        connectAttr( tex + '.' + texOut + conns[i].split( 'outValue' )[-1], conns[i + 1], force = True )

                        delete( each )

                        outNodes.append( tex )
                        outNodes.append( plc )

        select( outNodes, replace = True )
