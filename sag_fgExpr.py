#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:25:24
#========================================
from maya.cmds import *
import re, os, os.path
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


# GLOBAL VARIABLES
dataDir = 'x:/SAVVA/data/' # DEFAULT DATA STORAGE


# RETURN THE SHOT PATH SECTION
def sag_fgExpr_projPath():
        projectPathName = workspace( query = True, fullName = True )

        projectPathNameSplit = projectPathName.split( '/' )
        projPath = ''
        if projectPathNameSplit[0] == 'S:' and projectPathNameSplit[1] == 'SAVVA':
                for each in projectPathNameSplit[3:]:
                        if re.match( 'P[0-9][0-9]$', each ) or re.match( 'Ep[0-9][0-9]$', each ):
                                projPath += each + '_'
                        else:
                                if each == 'LAYOUTS':
                                        each = 'Feature'
                                projPath += each + '/'
        else:
                projPath += '_tmp/'

        return projPath 


# CREATE OR JUST DELETE FGEXPR
def sag_fgExpr( mode, fgPath ):
        exprName = '_fg_expr'
        if objExists( exprName ):
                delete( exprName )

        if mode == 1:
                if fgPath == '':
                        fgPath = dataDir + sag_fgExpr_projPath() + 'fgMaps/'

                if not os.path.exists( fgPath ):
                        os.makedirs( fgPath )

                exprString = 'string $fgPath = "' + fgPath + '";\r\n'
                exprString += '\r\n'
                exprString += 'int $padding = 4;\r\n'
                exprString += 'string $frame = floor( frame );\r\n'
                exprString += 'string $pad = "";\r\n'
                exprString += 'for ($i = size($frame); $i < $padding; $i++)\r\n\t'
                exprString += '$pad += "0";\r\n'
                exprString += '$frame = $pad + $frame;\r\n'
                exprString += '\r\n'
                exprString += 'string $rLayer = ( `editRenderLayerGlobals -q -crl` + "_" );\r\n'
                exprString += 'string $fileName = "";\r\n'
                exprString += 'if( $rLayer != "defaultRenderLayer_" )\r\n\t'
                exprString += '$fileName = $rLayer;\r\n'
                exprString += '\r\n'
                exprString += 'if( $rLayer == "env_" )\r\n\t'
                exprString += 'setAttr -type "string" miDefaultOptions.finalGatherFilename ( $fgPath + $fileName + "fg.fgmap");\r\n'
                exprString += 'else\r\n\t'
                exprString += 'setAttr -type "string" miDefaultOptions.finalGatherFilename ( $fgPath + $fileName + "fg." + $frame + ".fgmap");'

                expr = expression( name = '_fg_expr', string = exprString )

                setAttr( 'miDefaultOptions.finalGatherRebuild', 2 )
