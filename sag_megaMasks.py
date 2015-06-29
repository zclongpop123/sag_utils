#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:17:29
#========================================
from maya.cmds import *
from sag_fileTools import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# GATHERS DATA FROM SPECIALC CHANNELS
def sag_megaMasks_gather():
        selList = ls( type = 'p_MegaTK' )
        selList += ls( type = 'p_HairTK' )
        selList += ls( type = 'gluk_hair' )

        shDict = {}
        for each in selList:
                specials = []
                for i in xrange( 3, 16 ):
                        if i != 10:
                                conn = listConnections( each + '.specialC' + str( i ), s = True, d = False, c = False, p = True )
                                if conn != None:
                                        specials.append( conn[0] )
                                        specials.append( conn[0] )
                                        specials.append( conn[0] )
                                else:
                                        vals = getAttr( each + '.specialC' + str( i ) )[0]
                                        specials.append( vals[0] )
                                        specials.append( vals[1] )
                                        specials.append( vals[2] )
                        else:
                                specials.append( 0.0 )
                                specials.append( 0.0 )
                                specials.append( 0.0 )
                shDict[ each ] = specials

        return shDict


# CLEAR ALL SPECIAL CHANNELS
def sag_megaMasks_clear():
        selList = ls( type = 'p_MegaTK' )
        selList += ls( type = 'p_HairTK' )
        selList += ls( type = 'gluk_hair' )

        for each in selList:
                for i in xrange( 3, 16 ):
                        if i != 10:
                                conn = listConnections( each + '.specialC' + str( i ), s = True, d = False, p = True )
                                if conn != None:
                                        disconnectAttr( conn[0], each + '.specialC' + str( i ) )

                                setAttr( each + '.specialC' + str( i ), 0, 0, 0, type = 'double3' )
                                setAttr( each + '.use_SpecialC' + str( i ), 0 )


# PROMPT REPLACEMENT STRING
def sag_megaMasks_promptReplace():
        prompt = promptDialog(
                title = 'Replacement',
                message = 'replaceFrom replaceTo:',
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        replacement = ''
        if prompt == 'OK':
                replacement = promptDialog( query = True, text = True )

        return replacement


# MAIN PROCEDURE
def sag_megaMasks( mode ):
        if mode == 'store':
                fileName = fileDialog( mode = 1 )

                if fileName == '':
                        return

                sag_dataStore( sag_megaMasks_gather(), fileName )


        elif mode == 'restore' or mode == 'restore_detailed':
                fileName = fileDialog( mode = 0 )

                if fileName == '':
                        return

                specialDict = sag_dataRestore( fileName )

                repl = sag_megaMasks_promptReplace()
                if repl == '':
                        repl = [ '', '' ]
                elif len( repl.split() ) != 2:
                        repl = [ '', '' ]
                else:
                        repl = repl.split()

                conns = 0
                used = { 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 11:0, 12:0, 13:0, 14:0, 15:0 }
                shdMsg = []
                mskMsg = []
                for each in specialDict:
                        for i in xrange( 3, 16 ):
                                if i != 10:
                                        replShd = each.replace( repl[0], repl[1] )
                                        if objExists( replShd ):
                                                if not len( specialDict[ each ] ) / 3 < i - 3:
                                                        if str( type( specialDict[ each ][ (i-3)*3 ] ) ) != '<type \'float\'>' :
                                                                if objExists( specialDict[ each ][ (i-3)*3 ].split( '.' )[0] ):
                                                                        setAttr( replShd + '.use_SpecialC' + str( i ), 1 )
                                                                        used[ i ] += 1
                                                                        conns += 1
                                                                        if not isConnected( specialDict[ each ][ (i-3)*3 ], replShd + '.specialC' + str( i ) ):
                                                                                connectAttr( specialDict[ each ][ (i-3)*3 ], replShd + '.specialC' + str( i ), force = True )
                                                                        if mode == 'restore_detailed':
                                                                                mskMsg.append( ' Connecting: ' + specialDict[ each ][ (i-3)*3 ] + ' -> ' + replShd + '.specialC' + str( i ) )
                                                                else:
                                                                        mskMsg.append( ' Mask ' + specialDict[ each ][ (i-3)*3 ].split( '.' )[0] + ' doesn\'t exist!' )
                                                        else:
                                                                # IF ONE OF RGB CHANNELS IS LARGER THAT 0, ENABLE SPECIALC CHANNGEL, OTHERWISE DISABLE IT
                                                                if specialDict[ each ][ (i-3)*3 ] > 0 or specialDict[ each ][ (i-3)*3 + 1 ] > 0 or specialDict[ each ][ (i-3)*3 + 2 ] > 0:
                                                                        setAttr( replShd + '.use_SpecialC' + str( i ), 1 )
                                                                        used[ i ] += 1
                                                                else:
                                                                        setAttr( replShd + '.use_SpecialC' + str( i ), 0 )

                                                                # IF CHANNEL HAS INCOMING CONNECTION, BREAK IT
                                                                conn = listConnections( replShd + '.specialC' + str( i ), s = True, d = False, p = True )
                                                                if conn != None:
                                                                        disconnectAttr( conn[0], replShd + '.specialC' + str( i ) )

                                                                # ASSIGN SPECIALC COLOR VALUE	
                                                                setAttr( replShd + '.specialC' + str( i ), specialDict[ each ][ (i-3)*3 ], specialDict[ each ][ (i-3)*3 + 1 ], specialDict[ each ][ (i-3)*3 + 2 ], type = 'double3' )

                                                                if mode == 'restore_detailed':
                                                                        mskMsg.append( ' Setting: ' + replShd + '.specialC' + str( i ) + ' -> ' + str( specialDict[ each ][ (i-3)*3 ] ) + ' ' + str( specialDict[ each ][ (i-3)*3 + 1 ] ) + ' ' + str( specialDict[ each ][ (i-3)*3 + 2 ] ) )
                                                else:
                                                        setAttr( replShd + '.use_SpecialC' + str( i ), 0 )
                                                        setAttr( replShd + '.specialC' + str( i ), 0, 0, 0, type = 'double3' )
                                        else:
                                                shdMsg.append( ' Shader ' + replShd + ' doesn\'t exist!' )

                # FEEDBACK
                shdMsg = list( set( shdMsg ) )
                mskMsg = list( set( mskMsg ) )
                shdMsg.sort()
                mskMsg.sort()

                count = 0
                usedMsg = ' Channels used:'
                for usedChan in used:
                        if used[ usedChan ] > 0:
                                usedMsg += ' ' + str( usedChan )
                                count += used[ usedChan ]
                setMsg = ' Evaluated ' + str( count - conns ) + ' channels...'
                conMsg = ' Made ' + str( conns ) + ' connections...'

                liner = '##'
                maxLiner = max( max( len( usedMsg ), len( setMsg ) ), len( conMsg ) )
                for each in shdMsg:
                        maxLiner = max( maxLiner, len( each ) )
                for each in mskMsg:
                        maxLiner = max( maxLiner, len( each ) )
                for i in xrange( maxLiner ):
                        liner += '#'

                print ''
                print liner
                if shdMsg != []:
                        for each in shdMsg:
                                print each
                        print ''
                if mskMsg != []:
                        for each in mskMsg:
                                print each
                        print ''
                print setMsg
                print conMsg
                print usedMsg
                print liner
                print ''
