#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:27:42
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


def sag_bakeCam():
        selList = ls( selection = True )

        # MAKE A LIST OF CAMERAS FROM SELECTION
        camList = []
        for each in selList:
                if objectType( each ) == 'camera' or objectType( each ) == 'stereoRigCamera':
                        camList.append( each )
                elif objectType( each ) == 'transform':
                        shps = listRelatives( each, shapes = True )
                        for eachShp in shps:
                                if objectType( eachShp ) == 'camera':
                                        camList.append( eachShp )
                elif objectType( each ) == 'stereoRigTransform':
                        camList.append( listRelatives( each, shapes = True )[0] )
                        chds = listRelatives( each, children = True, type = 'transform' )
                        for eachChd in chds:
                                shps = listRelatives( eachChd, shapes = True )
                                if shps != None:
                                        for eachShp in shps:
                                                if objectType( eachShp ) == 'camera':
                                                        camList.append( eachShp )
        camList = list( set( camList ) )
        camList.sort()

        # DUPLICATE CAMERAS, LINK THEM TO ORIGINALS
        bakeList = []
        junkList = []
        for each in camList:
                eachTrs = listRelatives( each, parent = True )[0]

                # UNREFERENCE
                if referenceQuery( eachTrs, isNodeReferenced = True ):
                        file( referenceQuery( eachTrs, filename = True ), importReference = True )

                # SET LINEAR INFINITY TO ALL ANIMATION CURVES OF THE ORIGINAL CAMERA
                animCurves = listConnections( ( each, eachTrs ), s = True, d = False, c = False, p = False, type = 'animCurve' )
                if animCurves != None:
                        selectKey( animCurves, replace = True )
                        setInfinity( poi = 'linear' )
                        selectKey( clear = True )

                # RENAME ORIGINAL CAMERA AND MAKE A DUPLICATE OR JUST DUPLICATE FOR CAMERAS WITH NAMESPACES
                if eachTrs.find( ':' ) > -1:
                        dup = duplicate( eachTrs, renameChildren = True )[0]
                        eachTmpTrs = eachTrs
                        eachTrs = dup
                        camList[ camList.index( each ) ] = listRelatives( dup, shapes = True )[0] 
                        each = listRelatives( dup, shapes = True )[0]
                else:
                        eachTmpTrs = rename( eachTrs, eachTrs + '_bakeCamTmp' )
                        dup = duplicate( eachTmpTrs, name = eachTrs, renameChildren = True )[0]

                # REMOVE ALL CHILDREN UNDER THE DUPLICATE
                chds = listRelatives( dup, children = True )
                forDel = []
                for eachChd in chds:
                        if eachChd not in camList:
                                forDel.append( eachChd )
                if forDel != []:
                        delete( forDel )

                # DEFINE ATTRIBUTES TO BAKE, UNLOCK THEM, UNPARENT DUPLICATE, PARENTCONSTRAINT TRANSFORMS AND CONNECT SHAPE TO ORIGINAL
                trsAttrs = [ 'tx', 'ty', 'tz', 'rx', 'ry', 'rz' ]
                shpAttrs = [ 'focalLength', 'horizontalFilmAperture', 'verticalFilmAperture' ]

                setAttr( eachTrs + '.translate', lock = False )
                setAttr( eachTrs + '.rotate', lock = False )

                for eachAttr in trsAttrs:
                        setAttr( eachTrs + '.' + eachAttr, lock = False, keyable = True )
                if listRelatives( dup, parent = True ) != None:
                        parent( dup, world = True )
                junkList.append( parentConstraint( eachTmpTrs, eachTrs, maintainOffset = True )[0] )
                bakeList.append( eachTrs )

                for eachAttr in shpAttrs:
                        setAttr( each + '.' + eachAttr, lock = False, keyable = True )
                        print 'connecting ' + listRelatives( eachTmpTrs, shapes = True )[0] + '.' + eachAttr + ' -> ' + each + '.' + eachAttr
                        connectAttr( listRelatives( eachTmpTrs, shapes = True )[0] + '.' + eachAttr, each + '.' + eachAttr, force = True )
                bakeList.append( each )

        # ISOLATE DUPLICATES IN VIEWPORT FOR FASTER BAKING
        select( bakeList, replace = True )
        viewPanel = paneLayout( 'viewPanes', query = True, pane1 = True )
        isolateSelect( viewPanel, state = 1 )
        isolateSelect( viewPanel, addSelected = True )

        # GET FRAME RANGE FROM TIME SLIDER AND BAKE ANIMATION
        startFrame = playbackOptions( q = True, min = True )
        endFrame = playbackOptions( q = True, max = True )

        bakeResults( bakeList, simulation = True, t = ( startFrame, endFrame ) )

        # CLEANUP CONSTRAINTS, STATIC CHANNELS, APPLY EULER FILTER AND DISABLE ISOLATE
        delete( junkList )
        delete( bakeList, staticChannels = True )
        animCurves = listConnections( bakeList, source = True, destination = False, connections = False, plugs = False )
        filterCurve( animCurves )

        isolateSelect( viewPanel, state = 0 )
