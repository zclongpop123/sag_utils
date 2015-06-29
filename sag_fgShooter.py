#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:25:05
#========================================
from maya.cmds import *
import maya.mel
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# MAIN PROCEDURE FOR CREATING FGSHOOTER
def sag_fgShooter_do( mode ):
        cam = optionMenuGrp( 'sag_fgShooter_cam_ctrl', query = True, value = True )
        cam = listRelatives( cam, shapes = True )[0]

        # DELETE OLD FG SHOOTER IF PRESENT
        conns = listConnections( cam, s = True, d = False )
        if conns != None:
                for eachConn in conns:
                        if objectType( eachConn ) == 'mip_fgshooter':
                                delete( eachConn )

        # CREATE FG SHOOTER
        if mode == 'create':
                fgShoot = createNode( 'mip_fgshooter' )
                lensListSize = getAttr( cam + '.miLensShaderList', size = True )
                connectAttr( fgShoot + '.message', cam + '.miLensShaderList[' + str( lensListSize ) +']' )

                fgShootMode = optionMenuGrp( 'sag_fgShooter_mode_ctrl', query = True, select = True )
                setAttr( fgShoot + '.mode', fgShootMode - 1 )

                # GET RANGE FROM THE TIMESLIDER AND MAKE A FRAMELIST BASED ON STEP SIZE
                startFrame = int( playbackOptions( q = True, min = True ) )
                endFrame = int( playbackOptions( q = True, max = True ) )
                stepFrame = intSliderGrp( 'sag_fgShooter_step_ctrl', query = True, value = True )
                origFrame = currentTime( query = True )

                frameList = []
                for i in xrange( startFrame, endFrame, stepFrame ):
                        frameList.append( i )

                # MAKE SURE LAST FRAME IS IN THE LIST
                if frameList[-1] != endFrame:
                        frameList.append( endFrame )

                # GO THROUGH FRAMES IN THE LIST AND STORE MATRICES INTO FGSHOOTER
                for eachFrame in frameList:
                        currentTime( eachFrame, update = True )

                        mtx = getAttr( cam + '.worldMatrix' )

                        evalString = 'setAttr ' + fgShoot + '.trans[' + str(frameList.index( eachFrame )) + '] -type "matrix"'
                        for eachValue in mtx:
                                evalString += ' ' + str( eachValue )
                        maya.mel.eval( evalString )

                # RETURN TO THE ORIGINAL FRAME
                currentTime( origFrame, update = True )


# GUI
def sag_fgShooter():
        if window( 'sag_fgShooter', exists = True ):
                deleteUI( 'sag_fgShooter' )

        win = window( 'sag_fgShooter', title = 'FG Shooter', sizeable = False )

        columnLayout( adj = True )

        frameLayout( label = ' FG Shooter Settings', 
                     borderStyle = 'etchedIn', 
                     labelVisible = True, 
                     borderVisible = True, 
                     collapsable = False )

        columnLayout( adj = True, rowSpacing = 4, columnAttach = [ 'both', 4 ] )

        separator( height = 5, style = 'none' )

        optionMenuGrp( 'sag_fgShooter_cam_ctrl',
                       label = 'Camera',
                       columnWidth2 = [ 55, 425 ],
                       columnAlign = [ 1, 'right' ] )
        cams = ls( type = 'camera' )
        renderCams = []
        for eachCam in cams:
                eachCam = listRelatives( eachCam, parent = True )[0]
                menuItem( label = eachCam )

                # COLLECT RENDERABLE CAMERAS
                if getAttr( eachCam + '.renderable' ):
                        renderCams.append( eachCam )
        # IF RENDERABLE CAMERA EXISTS - SET IT AS DEFAULT VALUE
        if renderCams != []:
                optionMenuGrp( 'sag_fgShooter_cam_ctrl', edit = True, value = renderCams[0] )

        optionMenuGrp( 'sag_fgShooter_mode_ctrl',
                       label = 'Mode',
                       columnWidth2 = [ 55, 425 ],
                       columnAlign = [ 1, 'right' ] )
        menuItem( label = '0: MultiFrame' )
        menuItem( label = '1: Overlay (All Visible)' )
        menuItem( label = '2: Overlay (First Visible)' )

        # LIMIT INTERVAL TO THE MAXIMUM NUMBER OF FRAMES IN THE SEQUENCE
        maxFrames = int( playbackOptions( q = True, max = True ) ) - int( playbackOptions( q = True, min = True ) ) + 1
        intSliderGrp( 'sag_fgShooter_step_ctrl',
                      label = 'Interval',
                      enable = True,
                      minValue = 1,
                      maxValue = maxFrames,
                      field = True,
                      fieldMinValue = 1,
                      fieldMaxValue = maxFrames,
                      value = min( 5, maxFrames ),
                      columnWidth3 = [ 55, 50, 450 ] )

        setParent( '..' )
        setParent( '..' )	

        # BUTTONS
        rowLayout( numberOfColumns = 2, columnWidth2 = [ 250, 250 ], columnAlign2 = [ 'center', 'center' ] )

        button( label = 'Create',
                width = 250, 
                height = 25,
                command = 'sag_fgShooter_do( "create" )' )

        button( label = 'Delete',
                width = 245,
                height = 25,
                command = 'sag_fgShooter_do( "delete" )' )

        setParent( '..' )

        showWindow( win )

        window( win, edit = True, width = 500, height = 166 ) 
