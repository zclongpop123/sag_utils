#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:20:46
#========================================
from maya.cmds import *
from maya.app.stereo import stereoCameraRig
import maya.mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def sag_mirrorCam():
        if not pluginInfo( 'decomposeMatrix', query = True, loaded = True):
                loadPlugin( 'decomposeMatrix', quiet = True )

        selList = ls( sl = True )

        transList = []
        for each in selList:
                if objectType( each ) == 'transform' or objectType( each ) == 'stereoRigTransform':
                        transList.append( each )

        loc = spaceLocator( name = 'mirrorCam_loc' )[0]

        for each in transList:
                baseLoc = spaceLocator( name = 'mirrorCam_baseLoc' )[0]
                aimLoc = spaceLocator( name = 'mirrorCam_aimLoc' )[0]
                upLoc = spaceLocator( name = 'mirrorCam_upLoc' )[0]

                setAttr( aimLoc + '.tz', -1 )
                setAttr( upLoc + '.ty', 1 )
                setAttr( baseLoc + '.v', 0 )

                parent( aimLoc, upLoc, baseLoc )

                multMtx = createNode( 'multMatrix', name = 'mirrorCam_multMatrix' )
                decompMtx = createNode( 'decomposeMatrix', name = 'mirrorCam_decomposeMatrix' )

                connectAttr( each + '.worldMatrix', multMtx + '.matrixIn[0]' )
                connectAttr( loc + '.worldInverseMatrix', multMtx + '.matrixIn[1]' )
                maya.mel.eval( 'setAttr ' + multMtx + '.matrixIn[2] -type "matrix" 1 0 0 0 0 1 0 0 0 0 -1 0 0 0 0 1;' )
                connectAttr( loc + '.worldMatrix', multMtx + '.matrixIn[3]' )

                connectAttr( multMtx + '.matrixSum', decompMtx + '.inputMatrix' )

                setAttr( baseLoc + '.rotateOrder', getAttr( each + '.rotateOrder' ) )
                connectAttr( decompMtx + '.outputTranslate', baseLoc + '.t' )
                connectAttr( decompMtx + '.outputRotate', baseLoc + '.r' )
                connectAttr( decompMtx + '.outputScale', baseLoc + '.s' )

                cam = ''
                # DUPLICATE CAMERA
                if nodeType( each ) == 'stereoRigTransform':
                        # DUPLICATE STEREO CAMERA
                        eachShape = listRelatives( each, type = 'stereoRigCamera' )[0]

                        cam = stereoCameraRig.createStereoCameraRig( rigName = 'StereoCamera' )

                        cam[0] = rename( cam[0], 'mirrorCam_' + each.split( ':' )[-1] )
                        cam[1] = rename( cam[1], 'mirrorCam_' + each.split( ':' )[-1][:-1] + 'L' )
                        cam[2] = rename( cam[2], 'mirrorCam_' + each.split( ':' )[-1][:-1] + 'R' )

                        camShape = listRelatives( cam[0], type = 'stereoRigCamera' )[0]

                        attrListShape = set(['horizontalFilmAperture', 'verticalFilmAperture', 'shakeOverscan', 'shakeOverscanEnabled', 'horizontalFilmOffset',
                                             'verticalFilmOffset', 'shakeEnabled', 'horizontalShake', 'verticalShake', 'stereoHorizontalImageTranslateEnabled',
                                             'stereoHorizontalImageTranslate', 'preScale', 'filmTranslateH', 'filmTranslateV', 'horizontalRollPivot', 'verticalRollPivot',
                                             'filmRollValue', 'filmRollOrder', 'postScale', 'filmFit', 'filmFitOffset', 'focalLength', 'lensSqueezeRatio', 'cameraScale',
                                             'triggerUpdate', 'fStop', 'focusDistance', 'shutterAngle', 'centerOfInterest', 'tumblePivotX',
                                             'tumblePivotY', 'tumblePivotZ', 'usePivotAsLocalSpace', 'depthOfField',
                                             'useExploreDepthFormat', 'backgroundColorR', 'backgroundColorG', 'backgroundColorB', 'focusRegionScale',
                                             'toeInAdjust', 'filmOffsetRightCam', 'filmOffsetLeftCam', 'stereo', 'interaxialSeparation', 'zeroParallax'])

                        attrListTransform = set(['translate', 'rotate', 'scale'])

                        for eachAttr in attrListShape:
                                connectAttr( eachShape + '.' + eachAttr, camShape + '.' + eachAttr )

                        for eachAttr in attrListTransform:
                                connectAttr( each + '.' + eachAttr, cam[0] + '.' + eachAttr )

                        stereoShapes = listRelatives( each, allDescendents = True, type = 'camera' )
                        connectAttr( stereoShapes[1] + '.filmTranslateH', cam[1] + '.filmTranslateH' )
                        connectAttr( stereoShapes[2] + '.filmTranslateH', cam[2] + '.filmTranslateH' )

                        for eachCam in cam:
                                setAttr( eachCam + '.bestFitClippingPlanes', 0 )

                        cam = cam[0]
                else:
                        # DUPLICATE NON-STEREO CAMERA
                        cam = duplicate( each, ic = True )[0]

                        camName = 'mirrorCam_' + each
                        if each.rfind( ':' ) > -1:
                                camName = 'mirrorCam_' + each[each.rfind( ':' )+1:]
                        cam = rename( cam, camName )

                attrs = [ 't', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz', 'v' ]
                for attr in attrs:
                        setAttr( cam + '.' + attr, lock = False, keyable = True )

                attrs += [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ', 'visibility', 'translate', 'rotate', 'scale' ]
                for attr in attrs:
                        conns = listConnections( cam + '.' + attr, s = True, d = False, c = True, p = True )
                        if conns != None:
                                for i in xrange( 0, len( conns ), 2 ):
                                        disconnectAttr( conns[i+1], conns[i] )

                if listRelatives( cam, parent = True ) != None:
                        parent( cam, world = True )

                select( baseLoc, cam, replace = True )
                pointConstraint( mo = False )
                select( aimLoc, cam, replace = True )
                aimConstraint( mo = False, aimVector = (0, 0, -1), upVector = (0, 1, 0), worldUpType = 'object', worldUpObject = upLoc )

                group( [ loc, baseLoc, cam ], name = 'mirror_cam_grp' )

                select( loc, replace = True )
