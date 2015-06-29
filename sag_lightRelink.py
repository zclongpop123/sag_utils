#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:17:12
#========================================
from maya.cmds import *
from sag_fileTools import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# GATHER LIGHT LINKS
def sag_lightRelink_gather( lightList ):

        lightLinks = {}
        lightIgnores = {}
        shadowLinks = {}
        shadowIgnores = {}

        for each in lightList:
                lLinks = []
                lIgnores = []
                sLinks = []
                sIgnores = []

                conns = [ eachConn for eachConn in listConnections( each, s = False, d = True, c = False, p = True ) if eachConn[:eachConn.find( '.' )] == 'lightLinker1' ]
                for eachConn in conns:
                        eachConnSplit = eachConn.split( '.' )

                        objConn = eachConnSplit[0] + '.' + eachConnSplit[1] + '.' + eachConnSplit[2].replace( 'light', 'object' )
                        obj = listConnections( objConn, s = True, d = False )
                        if obj != None:
                                obj = obj[0]

                                linkType = eachConnSplit[1]
                                if linkType.find( 'shadowLink' ) > -1:
                                        sLinks.append( obj )
                                elif linkType.find( 'shadowIgnore' ) > -1:
                                        sIgnores.append( obj )
                                elif linkType.find( 'link' ) > -1:
                                        lLinks.append( obj )
                                elif linkType.find( 'ignore' ) > -1:
                                        lIgnores.append( obj )

                if lLinks != []:
                        lightLinks[ each ] = list( set( lLinks ) )
                if lIgnores != []:
                        lightIgnores[ each ] = list( set( lIgnores ) )
                if sLinks != []:
                        shadowLinks[ each ] = list( set( sLinks ) )
                if sIgnores != []:
                        shadowIgnores[ each ] = list( set( sIgnores ) )

        return lightLinks, lightIgnores, shadowLinks, shadowIgnores


# CLEANUP LIGHTLINKER
def sag_lightRelink_cleanup( mode ):

        lightLinker = 'lightLinker1'

        # CLEANUP LINKS
        indices = getAttr( lightLinker + '.link', multiIndices = True )
        if indices != None:
                for each in indices:
                        removeMultiInstance( lightLinker + '.link[' + str( each ) + ']', b = True )

        # CLEANUP IGNORES
        indices = getAttr( lightLinker + '.ignore', multiIndices = True )
        if indices != None:
                for each in indices:
                        removeMultiInstance( lightLinker + '.ignore[' + str( each ) + ']', b = True )

        # CLEANUP SHADOWLINKS
        indices = getAttr( lightLinker + '.shadowLink', multiIndices = True )
        if indices != None:
                for each in indices:
                        removeMultiInstance( lightLinker + '.shadowLink[' + str( each ) + ']', b = True )

        # CLEANUP SHADOWIGNORES
        indices = getAttr( lightLinker + '.shadowIgnore', multiIndices = True )
        if indices != None:
                for each in indices:
                        removeMultiInstance( lightLinker + '.shadowIgnore[' + str( each ) + ']', b = True )

        # RELINK DEFAULT SHADING GROUPS AND LIGHT SET
        connectAttr( 'defaultLightSet.message', lightLinker + '.link[0].light', force = True )
        connectAttr( 'initialShadingGroup' + '.message', lightLinker + '.link[0].object', force = True )
        connectAttr( 'defaultLightSet.message', lightLinker + '.shadowLink[0].shadowLight', force = True )
        connectAttr( 'initialShadingGroup' + '.message', lightLinker + '.shadowLink[0].shadowObject', force = True )

        connectAttr( 'defaultLightSet.message', lightLinker + '.link[1].light', force = True )
        connectAttr( 'initialParticleSE' + '.message', lightLinker + '.link[1].object', force = True )
        connectAttr( 'defaultLightSet.message', lightLinker + '.shadowLink[1].shadowLight', force = True )
        connectAttr( 'initialParticleSE' + '.message', lightLinker + '.shadowLink[1].shadowObject', force = True )

        if mode == 'relink':
                sgList = ls( type = 'shadingEngine' )
                sgList.remove( 'initialShadingGroup' )
                sgList.remove( 'initialParticleSE' )

                i = 2
                for eachSG in sgList:
                        connectAttr( eachSG + '.message', lightLinker + '.link[' + str( i ) + '].object' )
                        connectAttr( eachSG + '.message', lightLinker + '.shadowLink[' + str( i ) + '].shadowObject' )
                        connectAttr( 'defaultLightSet.message', lightLinker + '.link[' + str( i ) + '].light' )
                        connectAttr( 'defaultLightSet.message', lightLinker + '.shadowLink[' + str( i ) + '].shadowLight' )
                        i += 1

# PROMPT REPLACEMENT STRING
def sag_lightRelink_promptReplace():
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
def sag_lightRelink( mode ):

        lightList = ls( type = 'light' )

        if mode == 'store':
                fileName = fileDialog( mode = 1 )

                if fileName == '':
                        return

                sag_dataStore( sag_lightRelink_gather( lightList ), fileName )

        elif mode == 'view':
                fileName = fileDialog( mode = 0 )

                if fileName == '':
                        return

                lightLinks, lightIgnores, shadowLinks, shadowIgnores = sag_dataRestore( fileName )

                print ''
                print '-------------------------LIGHT LINKS---------------------------'
                if lightLinks == {}:
                        print ''
                for each in lightLinks:
                        print each + ':'
                        for eachLink in lightLinks[ each ]:
                                print ' - ' + eachLink
                        print ''
                print '------------------------LIGHT BREAKS---------------------------'
                if lightIgnores == {}:
                        print ''
                for each in lightIgnores:
                        print each + ':'
                        for eachLink in lightIgnores[ each ]:
                                print ' - ' + eachLink
                        print ''
                print '------------------------SHADOW LINKS---------------------------'
                if shadowLinks == {}:
                        print ''
                for each in shadowLinks:
                        print each + ':'
                        for eachLink in shadowLinks[ each ]:
                                print ' - ' + eachLink
                        print ''
                print '-----------------------SHADOW BREAKS---------------------------'
                if shadowIgnores == {}:
                        print ''
                for each in shadowIgnores:
                        print each + ':'
                        for eachLink in shadowIgnores[ each ]:
                                print ' - ' + eachLink
                        print ''
                print ''

        elif mode == 'restore':
                fileName = fileDialog( mode = 0 )

                if fileName == '':
                        return

                lightLinks, lightIgnores, shadowLinks, shadowIgnores = sag_dataRestore( fileName )

                repl = sag_lightRelink_promptReplace()
                if repl == '':
                        repl = [ '', '' ]
                elif len( repl.split() ) != 2:
                        repl = [ '', '' ]
                else:
                        repl = repl.split()

                sag_lightRelink_cleanup( 'clear' )

                for each in lightLinks:
                        for eachLink in lightLinks[ each ]:
                                if objExists( eachLink.replace( repl[0], repl[1] ) ):
                                        lightlink( light = each, object = eachLink.replace( repl[0], repl[1] ), make = True )
                                else:
                                        print 'Object ' + eachLink.replace( repl[0], repl[1] ) + ' doesn\'t exist!'
                for each in lightIgnores:
                        for eachLink in lightIgnores[ each ]:
                                if objExists( eachLink.replace( repl[0], repl[1] ) ):
                                        lightlink( light = each, object = eachLink.replace( repl[0], repl[1] ), b = True )
                                else:
                                        print 'Object ' + eachLink.replace( repl[0], repl[1] ) + ' doesn\'t exist!'
                for each in shadowLinks:
                        for eachLink in shadowLinks[ each ]:
                                if objExists( eachLink.replace( repl[0], repl[1] ) ):
                                        lightlink( light = each, object = eachLink.replace( repl[0], repl[1] ), make = True, shadow = True )
                                else:
                                        print 'Object ' + eachLink.replace( repl[0], repl[1] ) + ' doesn\'t exist!'
                for each in shadowIgnores:
                        for eachLink in shadowIgnores[ each ]:
                                if objExists( eachLink.replace( repl[0], repl[1] ) ):
                                        lightlink( light = each, object = eachLink.replace( repl[0], repl[1] ), b = True, shadow = True )
                                else:
                                        print 'Object ' + eachLink.replace( repl[0], repl[1] ) + ' doesn\'t exist!'
