#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:19:49
#========================================
from maya.cmds import *
import maya.mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_refCleanup( filterEdits ):	
        # GET ALL REFERENCE NODES FROM SELECTION
        refList = []
        for each in ls( sl = True ):
                if referenceQuery( each, isNodeReferenced = True ):
                        refList.append( referenceQuery( each, referenceNode = True ) )

        if refList == []:
                confirmDialog( title = 'Error!', message = 'No references selected!', button = [ 'CANCEL' ] )
                return

        # CLEANUP REFERENCES
        for refNode in refList:
                refFile = referenceQuery( refNode, filename = True )
                file( refFile, unloadReference = True )
                allEdits = referenceQuery( orn = refNode, editStrings = True )
                file( cleanReference = refNode )
                file( refFile, loadReference = True )

                for eachEdit in allEdits:
                        for eachFilter in filterEdits:
                                if eachEdit.find( eachFilter ) == -1:
                                        try:
                                                maya.mel.eval( eachEdit )
                                        except:
                                                print 'SHIT'

                refresh( force = True )

        curTime = int( currentTime( query = True ) )
        currentTime( curTime + 1, update = True )
        currentTime( curTime, update = True )
