#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:26:27
#========================================
from maya.cmds import *
import maya.mel
import os, os.path, re, time
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_exportMeta( filePath, fileName, cam ):
	# ADDITIONAL DATA
	sceneName = file( query = True, sn = True )
	submitDate = time.strftime('%Y.%m.%d') + ' ' + time.strftime('%H:%M:%S')
	submitUser = os.getenv( 'USERNAME' )

	# METADATA NAME, TYPE, (S)TATIC/(G)ETATTR/(C)OMMAND + STEREOCAMERA (C)/(L)/(R), DATA/ATTRIBUTE/COMMAND
	attrList = (	('camName', 's', 'sc', cam[0]),
					('focalLength', 'f', 'gc', 'focalLength'),
					('hAperture', 'f', 'gc', 'horizontalFilmAperture'),
					('vAperture', 'f', 'gc', 'verticalFilmAperture'),
					('filmTranslateHL', 'f', 'gl', 'filmTranslateH'),
					('interaxial', 'f', 'gc', 'interaxialSeparation'),
					('zeroParallax', 'f', 'gc', 'zeroParallax'),
					('rotOrder', 's', 'cc', 'xform( eachCam, query = True, rotateOrder = True )'),
					('camRotate', 'f3', 'cc', 'xform( eachCam, query = True, worldSpace = True, rotation = True )'),
					('camTranslateL', 'f3', 'cl', 'xform( eachCam, query = True, worldSpace = True, translation = True )'),
					('camTranslateR', 'f3', 'cr', 'xform( eachCam, query = True, worldSpace = True, translation = True )'),
					('sceneName', 's', 'sc', sceneName),
					('submitDate', 's', 'sc', submitDate),
					('submitUser', 's', 'sc', submitUser),
					('nearClip', 'f', 'gc', 'nearClipPlane'),
					('farClip', 'f', 'gc', 'farClipPlane')
				)
	
	# INPUT ATTRIBUTE CAM SHOULD HAVE C/L/R CAMERA TRANSFORM NAMES
	camDict = { 'c':0, 'l':1, 'r':2 }

	# CORRECT SLASHES IN DAT FILE PATH
	filePath = filePath.replace( '\\', '/' )
	if filePath[-1] != '/':
		filePath += '/'

	# WRITE METADATA INTO DAT FILE
	datFile = open( filePath + fileName + '.dat', 'w' )

	for eachAttr in attrList:
		eachType = eachAttr[2]
		eachCam = cam[ camDict[ eachType[1] ] ]

		if eachType[0] == 'g':
			attr = getAttr( eachCam + '.' + eachAttr[3] )
		elif eachType[0] == 'c':
			exec( 'attr = ' + eachAttr[3] )
		else:
			attr = eachAttr[3]

		attr = re.sub( '[\[\](),]', '', str( attr ) )
		datFile.write( eachAttr[0] + ':' + eachAttr[1] + ':' + attr + '\n' )

	datFile.close()
