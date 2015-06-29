#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:24:46
#========================================
import os, os.path, cPickle
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# STORE DATA TO FILE
def sag_dataStore( data, filePath ):
        dirPath = filePath[:filePath.rfind( '/' )]

        if not os.path.exists( dirPath ):
                os.makedirs( dirPath )

        f = open( filePath, 'w' )
        cPickle.dump( data, f, 1 )
        f.close()


# RESTORE DATA FROM FILE
def sag_dataRestore( filePath ):
        if not os.path.exists( filePath ):
                return

        f = open( filePath, 'r' )
        data = cPickle.load( f )
        f.close()

        return data
