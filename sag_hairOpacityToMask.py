#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:22:50
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_hairOpacityToMask():
        if ls( sl = True ) != []:
                nmList = []
                for each in ls( sl = True ):
                        if each.find( ':' ) > -1:
                                nmList.append( each[:each.rfind( ':' )] )

                allHair = ls( type = 'hairGeoShader' )
                hairList = []
                for each in allHair:
                        if each[:each.rfind( ':' )] in nmList:
                                hairList.append( each )
        else:
                hairList = ls( type = 'hairGeoShader' )


        # MAIN FUNCTION
        for each in hairList:
                conns = listConnections( each + '.message', s = False, d = True, type = 'transform' )

                for conn in conns:
                        connShps = listRelatives( conn, shapes = True, type = 'mesh' )
                        for connShp in connShps:
                                sgs = listConnections( connShp, s = False, d = True, type = 'shadingEngine' )
                                for sg in sgs:
                                        shds = listConnections( sg + '.miMaterialShader', s = True, d = False )
                                        for shd in shds:
                                                if nodeType( shd ) == 'gluk_constant':
                                                        sgOvers = listConnections( sg, s = False, d = True, c = True, p = True, type = 'renderLayer' )
                                                        for sgOver in sgOvers:
                                                                if sgOver.find( 'defaultRenderLayer.' ) > -1:
                                                                        if sgOvers[sgOvers.index(sgOver)-1].find( '.miMaterialShader' ) > -1:
                                                                                origShds = listConnections( sgOver[:sgOver.rfind( '.' )] + '.value', s = True, d = False )
                                                                                for origShd in origShds:
                                                                                        if getAttr( origShd + '.transp_en' ):
                                                                                                rmp = origShd.replace( ':', '_' ) + '_transparencyHair_ramp'
                                                                                                if not objExists( rmp ):
                                                                                                        rmp = createNode( 'ramp', name = rmp )
                                                                                                        removeMultiInstance( rmp + '.colorEntryList[1]' )
                                                                                                        removeMultiInstance( rmp + '.colorEntryList[2]' )
                                                                                                if not isConnected( 'hair_map.outValue', rmp + '.vCoord' ):
                                                                                                        connectAttr( 'hair_map.outValue', rmp + '.vCoord' )
                                                                                                inds = getAttr( origShd + '.transparencyHair', mi = True )
                                                                                                for ind in inds:
                                                                                                        if not isConnected( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_Position', rmp + '.colorEntryList[' + str(ind) + '].position' ):
                                                                                                                connectAttr( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_Position', rmp + '.colorEntryList[' + str(ind) + '].position' )
                                                                                                        if not isConnected( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorR' ):
                                                                                                                connectAttr( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorR' )
                                                                                                        if not isConnected( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorG' ):
                                                                                                                connectAttr( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorG' )
                                                                                                        if not isConnected( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorB' ):
                                                                                                                connectAttr( origShd + '.transparencyHair[' + str(ind) + '].transparencyHair_FloatValue', rmp + '.colorEntryList[' + str(ind) + '].colorB' )

                                                                                                transp = origShd.replace( ':', '_' ) + '_transparencyHair'
                                                                                                if not objExists( transp ):
                                                                                                        transp = createNode( 'mib_transparency', name = transp )
                                                                                                if not isConnected( shd + '.outValue', transp + '.input' ):
                                                                                                        connectAttr( shd + '.outValue', transp + '.input' )
                                                                                                if not isConnected( rmp + '.outColor', transp + '.transp' ):
                                                                                                        connectAttr( rmp + '.outColor', transp + '.transp' )
                                                                                                if not isConnected( shd + '.outValue', transp + '.input' ):
                                                                                                        connectAttr( shd + '.outValue', transp + '.input' )

                                                                                                if not isConnected( transp + '.message', sg + '.miMaterialShader' ):
                                                                                                        connectAttr( transp + '.message', sg + '.miMaterialShader', force = True )
