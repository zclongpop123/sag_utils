#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:27:07
#========================================
from maya.cmds import *
from sag_utils import *
from colorsys import hsv_to_rgb
from random import uniform
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def sag_colorize():
        # STORE SELECTION
        selList = ls( sl = True )

        # GET GEO AND SG LISTS
        sag_utils_hiGeo()
        geoList = ls( sl = True )

        sag_utils_selSG()
        sgList = ls( sl = True )

        # CREATE SHADER & CONNECT IT TO SG
        shd = [ '_geoColor_diff_SHD', 'color' ]

        if not objExists( shd[0] ):
                shd[0] = shadingNode( 'lambert', asShader = True, name = shd[0] )

        for sg in sgList:
                if not isConnected( shd[0] + '.outColor', sg + '.surfaceShader' ):
                        connectAttr( shd[0] + '.outColor', sg + '.surfaceShader', force = True )

        # CREATE SWITCH & CONNECT TO SHADER
        swt = '_geoColor_tripleSwitch'

        if not objExists( swt ):
                swt = shadingNode( 'tripleShadingSwitch', asUtility = True, name = swt )
                setAttr( swt + '.default', 0, 0, 0, type = 'double3' )

        if not isConnected( swt + '.output', shd[0] + '.' + shd[1] ):
                connectAttr( swt + '.output', shd[0] + '.' + shd[1], force = True )

        # CONNECT GEO TO SWITCH
        updList = []
        for geo in geoList:
                conns = listConnections( geo, s = False, d = True, p = True, type = 'tripleShadingSwitch' )

                i = -1
                if conns != None:
                        for conn in conns:
                                if conn.split( '.' )[0] == swt:
                                        i = int(conn.replace( '[', ']' ).split( ']' )[-2])
                if i < 0:
                        inds = getAttr( swt + '.input', mi = True )
                        i = 0
                        if inds != None:
                                while i in inds:
                                        i += 1
                        connectAttr( geo + '.instObjGroups[0]', swt + '.input[' + str(i) + '].inShape' )
                updList.append( i )

        # GENERATE COLORS
        for upd in updList:
                h = uniform( 0.0, 1.0 )
                s = 1
                v = 1
                clr = hsv_to_rgb( h, s, v )
                setAttr( swt + '.input[' + str(upd) + '].inTriple', clr[0], clr[1], clr[2], type = 'double3' )

        # RESTORE SELECTION
        if selList != []:
                select( selList, r = True )
