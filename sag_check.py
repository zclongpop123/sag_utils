#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:16:49
#========================================
from maya.cmds import *
import unicodedata as ud
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# HIGHLIGHT CURRENT BUTTON
def sag_check_highlight( buttId ):
        button( buttId, edit = True, backgroundColor = [0.5, 1.0, 0.5] )


## DEFS
# REMOVE miLabel
def sag_check_removeMiLabel( buttId ):
        sag_check_highlight( buttId )

        feedback = []
        for each in ls( type = 'transform' ) + ls( type = 'mesh' ):
                if attributeQuery( 'miLabel', node = each, exists = True ):
                        lockNode( each, lock = 0 )
                        setAttr( each + '.miLabel', lock = 0 )
                        deleteAttr( each + '.miLabel' )
                        feedback.append( each )
        if feedback != []:
                msg = 'Removed miLabel from the following nodes:\n'
                for each in feedback:
                        msg += '\n' + each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
        else:
                confirmDialog( title = 'Result', message = 'No miLabel attributes found in the scene!', button = [ 'OK' ] )

# LIST miFinalGatherHide
def sag_check_listMiFGHide( buttId ):
        sag_check_highlight( buttId )

        feedback = []
        for each in ls( type = "transform" ) + ls( type = "mesh" ):
                if attributeQuery( "miFinalGatherHide", node = each, exists = True ):
                        feedback.append( each )
        if feedback != []:
                msg = 'miFinalGatherHide exists for the following nodes:\n'
                for each in feedback:
                        msg += '\n' + each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
                select( feedback, replace = True )
        else:
                confirmDialog( title = 'Result', message = 'No miFinalGatherHide attributes found in the scene!', button = [ 'OK' ] )
                select( clear = True )

# LIST RENDER STATS
def sag_check_renderStats( buttId ):
        sag_check_highlight( buttId )

        attrs = [	'castsShadows', 
                         'receiveShadows', 
                         'motionBlur', 
                         'primaryVisibility',
                         'smoothShading',
                         'visibleInReflections', 
                         'visibleInRefractions', 
                         'doubleSided', 
                         'opposite',
                         'miTransparencyCast',
                         'miTransparencyReceive',
                         'miReflectionReceive',
                         'miRefractionReceive',
                         'miFinalGatherCast',
                         'miFinalGatherReceive'
                         ]

        feedback = []
        outList = []
        for each in ls( type = 'mesh' ):
                for attr in attrs:
                        if not getAttr( each + '.' + attr ) and attr != 'opposite':
                                feedback.append( each + ' -> ' + attr )
                                outList.append( each )
                        elif getAttr( each + '.' + attr ) and attr == 'opposite':
                                feedback.append( each + ' -> ' + attr )
                                outList.append( each )

        if feedback != []:
                confirmDialog( title = 'Result', message = 'Some deviations found - selecting objects - check scriptEditor for details!', button = [ 'OK' ] )
                for each in feedback:
                        print each
                select( outList, replace = True )
        else:
                confirmDialog( title = 'Result', message = 'No deviations found!', button = [ 'OK' ] )

# SELECT p_MegaTK SHADERS THAT HAS OPACITY CHANNEL MAPPED OR SET
def sag_check_megaOpacity( buttId ):
        sag_check_highlight( buttId )

        outList = []
        for each in ls( type = 'p_MegaTK' ):
                conns = listConnections( each + '.cOpacity', s = True, d = False )
                if conns != None:
                        outList.append( each )
                else:
                        if getAttr( each + '.cOpacity' ) != [( 1.0, 1.0, 1.0 )]:
                                outList.append( each )

        if outList != []:
                msg = 'Selecting p_MegaTK with transparency:\n'
                print msg
                print ''
                for each in outList:
                        msg += '\n' + each
                        print each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
                select( outList, replace = True )
        else:
                confirmDialog( title = 'Result', message = 'No p_MegaTK with transparency found!', button = [ 'OK' ] )

# CHECK FOR SAME NAMES
def sag_check_sameNames( buttId ):
        sag_check_highlight( buttId )

        feedback = []
        for each in ls( type = 'mesh' ):
                if each.find( '|' ) > -1:
                        feedback.append( each )

        if feedback != []:
                msg = 'Selecting objects that have the same names:\n'
                print msg
                print ''
                for each in feedback:
                        msg += '\n' + each
                        print each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
                select( feedback, replace = True )
        else:
                confirmDialog( title = 'Result', message = 'No objects with the same names found!', button = [ 'OK' ] )

# CHECK FOR INCORRECT p_MegaTK OCCLUSION OPACITY MODE
def sag_check_megaOcclOpacityMode( buttId ):
        sag_check_highlight( buttId )

        feedback = []
        for each in ls( type = 'p_MegaTK' ):
                if getAttr( each + '.o_opacity_mode' ) != 0:
                        feedback.append( each )

        if feedback != []:
                msg = 'Selecting p_MegaTK shaders with incorrect occlusion opacity mode:\n'
                print msg
                print ''
                for each in feedback:
                        msg += '\n' + each
                        print each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
        else:
                confirmDialog( title = 'Result', message = 'No p_MegaTK with incorrect occlusion opacity mode found!', button = [ 'OK' ] )


def sag_check_megaPassesExport( buttId ):
        sag_check_highlight( buttId )

        attrs = [ 'shading_pass', 'color_occlusion_pass', 'diffuse_pass', 'diffuse_shadow_pass', 'specular_pass', 'specular_shadow_pass', 'occlusion_pass', 'indirect_illum_pass', 'ambient_pass', 'reflect_pass', 'refract_pass', 'incandescence_pass', 'z_pass', 'bent_normal_pass', 'specialC1_pass', 'specialC2_pass', 'specialC3_pass', 'specialC4_pass', 'specialC5_pass', 'specialC6_pass', 'specialC7_pass', 'specialC8_pass', 'specialC9_pass', 'specialC10_pass', 'specialC11_pass', 'specialC12_pass', 'specialC13_pass', 'specialC14_pass', 'specialC15_pass' ] 

        feedback = []
        for each in ls( type = 'p_MegaTK' ):
                for attr in attrs:
                        if not getAttr( each + '.' + attr ):
                                feedback.append( each )

        if feedback != []:
                msg = 'Selecting p_MegaTK shaders with disabled passes:\n'
                print msg
                print ''
                for each in feedback:
                        msg += '\n' + each
                        print each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
                select( feedback, replace = True )
        else:
                confirmDialog( title = 'Result', message = 'No p_MegaTK with disabled passes found!', button = [ 'OK' ] )

#####################################################################################################
# CHECK NON-UNICODE NAMES AND FILE NODE PATHS (CODE SOMEWHERE FROM WEB)

latin_letters = {}

def sag_check_is_latin(uchr):
        try: return latin_letters[uchr]
        except KeyError:
                return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def sag_check_only_roman_chars(unistr):
        return all(sag_check_is_latin(uchr)
                   for uchr in unistr
                   if uchr.isalpha())

def sag_check_nonUnicode( buttId ):
        sag_check_highlight( buttId )

        feedback1 = []
        for each in ls( type = 'file' ):
                filePath = getAttr( each + '.fileTextureName' )
                if not sag_check_only_roman_chars( filePath ):
                        feedback1.append( each )

        feedback2 = []
        for each in ls():
                if not sag_check_only_roman_chars( each ):
                        feedback2.append( each )

        if feedback1 != [] or feedback2 != []:
                msg1 = 'Paths with non-unicode characters:\n'
                print msg1
                print ''
                if feedback1 != []:
                        for each in feedback1:
                                msg1 += '\n' + each
                                print each
                else:
                        msg1 += '\n----'
                        print '----'

                msg2 = '\n\nNode names with non-unicode characters:\n'
                print msg2
                print ''
                if feedback2 != []:
                        for each in feedback2:
                                msg2 += '\n' + each
                                print each
                else:
                        msg2 += '\n----'
                        print '----'

                confirmDialog( title = 'Result', message = (msg1 + msg2), button = [ 'OK' ] )
        else:
                confirmDialog( title = 'Result', message = 'No non-unicode characters found!', button = [ 'OK' ] )

#################################################################################################################
# CHECK FOR UNKNOWN NODES

def sag_check_unkNodes( buttId ):
        sag_check_highlight( buttId )

        feedback = []
        for each in ls( type = 'unknown' ):
                feedback.append( each )

        if feedback != []:
                msg = 'Selecting unknown nodes:\n'
                print msg
                print ''
                for each in feedback:
                        msg += '\n' + each
                        print each
                confirmDialog( title = 'Result', message = msg, button = [ 'OK' ] )
        else:
                confirmDialog( title = 'Result', message = 'No unknown nodes found!', button = [ 'OK' ] )


# DEFS COLLECTOR			
def sag_check_defs():
        outDict = [
                ('sag_check_removeMiLabel()',			'Delete all miLabel attributes' ),
                ('sag_check_listMiFGHide()',			'List all objects with miFinalGather attribute' ),
                ('sag_check_renderStats()',				'List Render Stats deviations' ),
                ('sag_check_megaOpacity()',				'Select all p_MegaTK with transparency' ),
                ('sag_check_sameNames()',				'Select objects with the same names' ),
                ('sag_check_megaOcclOpacityMode()',		'Select all p_MegaTK with incorrect occlusion opacity mode' ),
                ('sag_check_megaPassesExport()',		'Select all p_MegaTK with disabled passes' ),
                ('sag_check_nonUnicode()',				'Find non-unicode characters in paths and node names' ),
                ('sag_check_unkNodes()',				'Select unknown nodes' )
        ]

        return outDict


# GUI
def sag_check():
        # GUI WINDOW
        winName = 'sag_check_win'

        if window( winName, exists = True ):
                deleteUI( winName )

        win = window( winName, title = 'Check', sizeable = False )

        # VARIABLES
        buttonHeight = 30

        # LAYOUTS
        columnLayout( adj = True )

        frameLayout( label = 'Checking procedures', 
                     borderStyle = 'etchedIn', 
                     labelVisible = True, 
                     borderVisible = True, 
                     collapsable = False )

        columnLayout( adj = True, rowSpacing = 4, columnAttach = [ 'both', 4 ] )

        defs = sag_check_defs()

        buttList = []
        for each in defs:
                buttList.append( button( label = each[1], height = buttonHeight, command = each[0] ) )

        for each in buttList:
                cmd = button( each, query = True, command = True )[:-1] + ' "' + each + '" )'
                button( each, edit = True, command = cmd )

        setParent( '..' )
        setParent( '..' )
        setParent( '..' )

        showWindow( win )

        window( win, edit = True, width = 627, height = (17 + 8 * (len(defs)+1) + buttonHeight * len(defs)) )
