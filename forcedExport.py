#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:16:01
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def forcedExport( mode ):
        forcedTypes = { 'forestGeoShader':'object_filename' } # , 'hairGeoShader':'cacheFileName'

        exprName = '_forcedExport_expr'
        if objExists( exprName ):
                delete( exprName )

        connList = []
        for forcedType in forcedTypes:
                if forcedType in listNodeTypes( 'rendernode/mentalray/geometry' ):

                        if mode == 1:
                                geoList = ls( type = forcedType )

                                for geo in geoList:
                                        if getAttr( geo + '.' + forcedTypes[ forcedType ] ).find( '#' ) > -1 or forcedType == 'hairGeoShader':
                                                obj = ls( listConnections( geo, s = False, d = True ), type = 'transform' )
                                                if obj != []:
                                                        shp = listRelatives( obj[0], shapes = True, fullPath = True )
                                                        if shp != None:
                                                                shp = shp[0]

                                                                if not attributeQuery( 'fake', node = shp, exists = True ):
                                                                        addAttr( shp, ln = 'fake', at = 'float' )
                                                                connList.append( shp )

                                                                if not attributeQuery( 'fake', node = geo, exists = True ):
                                                                        addAttr( geo, ln = 'fake', at = 'float' )
                                                                connList.append( geo )
                else:
                        print 'Node type ' + forcedType + ' is unknown! No forcedExport applied...'			

        if mode == 1 and connList != []:
                exprString = ''
                for each in connList:
                        exprString += each + '.fake = floor( frame );\r\n'

                expr = expression( name = '_forcedExport_expr', string = exprString )
