#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:29:01
#========================================
import mmap
import os
import re
from geometry import *
import time
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#fileName = 'd:/MayaProject/hair/lab/moveWorld/test.mi'
#destFileName = 'd:/MayaProject/hair/lab/moveWorld/tmp.mi'
def moveScentToZero(fileName, destFileName, zeroPos):
        startTime =  time.clock()
        f2 = open(destFileName, 'wb')

        f = open(fileName, "r+b")
        size = os.path.getsize(fileName)
        data = mmap.mmap(f.fileno(), size)

        reTransform = re.compile(
                r'(transform\n)((?:-?\d+\.\d*(?:e-?\d+)?\s+){16})')

        reInstance = re.compile(
                r'(instance.+?)(?:(?:transform\n)((?:-?\d+\.\d*(?:e-?\d+)?\s+){16}))?(end instance)',
                re.DOTALL)

        strT =''
        pos1 = 0
        count = 0
        TransformationMatrix = matrixT(-zeroPos)
        while True:
                mObj = reInstance.search(data, pos1)
                if not(mObj):
                        break
                count += 1
                pos2 = mObj.start()
                f2.write(data[pos1:pos2])
                f2.write(mObj.groups()[0])

                strT = mObj.groups()[1]
                m = matrix(map(float, strT.split())) if strT is not None else matrixI()
                m = inverseTransform(m)
                m *= TransformationMatrix
                m = inverseTransform(m)

                f2.write('transform\n' + str(m[0]) + ' ' + str(m[1]) + ' ' + str(m[2]) + ' ' + str(m[3]) + '\n' +
                         str(m[4]) + ' ' + str(m[5]) + ' ' + str(m[6]) + ' ' + str(m[7]) + '\n' +
                         str(m[8]) + ' ' + str(m[9]) + ' ' + str(m[10]) + ' ' + str(m[11]) + '\n' +
                         str(m[12]) + ' ' + str(m[13]) + ' ' + str(m[14]) + ' ' + str(m[15]) + '\n' 
                         )
                f2.write(mObj.groups()[2])

                pos1 = mObj.end()

        f2.write(data[pos1:])
        f2.close()
        f.close()

        print( 'count : ' + str(count))
        print( str( time.clock() - startTime) + ' sec.')
