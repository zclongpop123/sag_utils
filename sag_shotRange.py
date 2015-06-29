#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:18:14
#========================================
from maya.cmds import *
import mmap
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_shotRange():
        # FIND ALL REFERENCES AND CHOOSE THE ONE THAT HAS 'SHOT' NAMESPACE
        refFiles = file( query = True, reference = True )

        refScene = ''
        for eachRef in refFiles:
                if file( eachRef, query = True, namespace = True ) == 'shot':
                        refScene = eachRef

        # RETURN IF NO REFERENCES WITH 'SHOT' NAMESPACE FOUND, OTHERWISE FIND TIMELINE RANGE AND APPLY TO CURRENT SCENE
        if refScene == '':
                confirmDialog( title = 'Error', message = 'No reference with namespace "shot" found!', button = [ 'OK' ] )
                return
        else:
                f = open( refScene, 'rb' )
                fmap = mmap.mmap( f.fileno(), 0, access = mmap.ACCESS_READ )

                playByte = fmap.find( 'playbackOptions' )

                if playByte == -1:
                        confirmDialog( title = 'Error', message = 'No frame range data in referenced scene!', button = [ 'OK' ] )
                        return

                fmap.seek( playByte )
                line = fmap.read( 50 )

                fmap.close()
                f.close()

                playbackOptions( min = line.split()[2], max = line.split()[4] )
