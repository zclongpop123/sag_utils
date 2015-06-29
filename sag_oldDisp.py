#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:20:12
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_oldDisp( mode ):
        miText = '_maya_displace_miText'

        if objExists( miText ):
                delete( miText )

        if mode == 'create':
                miText = createNode( 'mentalrayText', name = miText )

                setAttr( miText + '.mode', 1 )
                setAttr( miText + '.text', 'link "maya_displace.dll"\n$include "maya_displace.mi"', type = 'string' )

                connectAttr( miText + '.message', 'mentalrayGlobals.miText', force = True )
