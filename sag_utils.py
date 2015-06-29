#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:17:49
#========================================
from maya.cmds import *
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#####################################################################################################
# SELECT ALL MESHES IN HIERARCHY

def sag_utils_hiGeo():
        select( hierarchy = True )
        selList = ls( selection = True )

        geoList = []
        for each in selList:
                if objectType( each ) == 'mesh':
                        geoList.append( each )

        if geoList != []:
                select( geoList, replace = True )
        else:
                select( clear = True )

#####################################################################################################
# SELECT MEGA/GLUK SHADERS ON SELECTED GEOMETRY

def sag_utils_selShd():
        select( hierarchy = True )
        selList = ls( selection = True )

        geoList = []
        for each in selList:
                if objectType( each ) == 'mesh' or objectType( each ) == 'nurbsSurface':
                        par = listRelatives( each, allParents = True, fullPath = True )
                        if par > 1:
                                each = par[0] + '|' + each.split( '|' )[-1]
                        if each not in geoList:
                                geoList.append( each )

        newList = []
        for each in geoList:
                conns = listConnections( each, s = False, d = True, type = 'shadingEngine' )
                conns = list( set( conns ) )
                for eachConn in conns:
                        hist = listHistory( eachConn )
                        for eachHist in hist:
                                if objectType( eachHist ) == 'p_MegaTK' or objectType( eachHist ) == 'p_HairTK' or objectType( eachHist ) == 'gluk_hair':
                                        if eachHist not in newList:
                                                newList.append( eachHist )

        if newList != []:
                select( newList, noExpand = True, replace = True )
        else:
                select( clear = True )

#####################################################################################################
# SELECT SHADING GROUPS ON SELECTED GEOMETRY

def sag_utils_selSG():
        select( hierarchy = True )
        selList = ls( selection = True )

        geoList = []
        for each in selList:
                if objectType( each ) == 'mesh' or objectType( each ) == 'nurbsSurface':
                        par = listRelatives( each, allParents = True, fullPath = True )
                        if par > 1:
                                each = par[0] + '|' + each.split( '|' )[-1]
                        if each not in geoList:
                                geoList.append( each )

        newList = []
        for each in geoList:
                conns = listConnections( each, s = False, d = True, type = 'shadingEngine' )
                conns = list( set( conns ) )
                for eachConn in conns:
                        hist = listHistory( eachConn )
                        for eachHist in hist:
                                if objectType( eachHist ) == 'shadingEngine':
                                        if eachHist not in newList:
                                                newList.append( eachHist )

        if 'forestGeoShader' in listNodeTypes( 'rendernode/mentalray/geometry' ):
                allPar = []
                for each in geoList:
                        allPar += listRelatives( each, allParents = True, fullPath = True )
                allPar = list( set( allPar ) )

                for par in allPar:
                        allFst = listConnections( par + '.miGeoShader', s = True, d = False, type = 'forestGeoShader' )
                        if allFst != None:
                                for fst in allFst:
                                        allSg = listConnections( fst + '.material', s = True, d = False, type = 'shadingEngine' )
                                        if allSg != None:
                                                for sg in allSg:
                                                        if sg not in newList:
                                                                newList.append( sg )

        if newList != []:
                select( newList, noExpand = True, replace = True )
        else:
                select( clear = True )

#####################################################################################################
# ASSIGN A SHADER TO SELECTED SHADINGGROUPS VIA OVERRIDES

def sag_utils_shdToSG():
        selList = ls( selection = True )

        prompt = promptDialog(
                title = 'Assign Shader to SGs',
                message = 'Input shader name:',
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        shd = ''
        if prompt == 'OK':
                shd = promptDialog( query = True, text = True )

                if objExists( shd ):
                        for each in selList:
                                conns = listConnections( each + '.miMaterialShader', s = True, d = False, p = True, c = True )
                                if conns != None:
                                        editRenderLayerAdjustment( each + '.miMaterialShader' )
                                        if not isConnected( shd + '.message', each + '.miMaterialShader' ):
                                                connectAttr( shd + '.message', each + '.miMaterialShader', force = True )

                                conns = listConnections( each + '.miLightMapShader', s = True, d = False, p = True, c = True )
                                if conns != None:
                                        editRenderLayerAdjustment( each + '.miLightMapShader' )
                                        disconnectAttr( conns[1], conns[0] )

                                conns = listConnections( each + '.miShadowShader', s = True, d = False, p = True, c = True )
                                if conns != None:
                                        editRenderLayerAdjustment( each + '.miShadowShader' )
                                        disconnectAttr( conns[1], conns[0] )

#####################################################################################################
# SET IRRADIANCE FOR ALL SHADERS TO 1/PI

def sag_utils_set318():
        selList = ls( type = 'p_MegaTK' )
        selList += ls( type = 'p_HairTK' )
        selList += ls( type = 'eyeIrisMaterial' )

        for each in selList:
                setAttr( each + '.cInd', 0.318, 0.318, 0.318, type = 'double3' )

#####################################################################################################
# SELECT ALL NODES BY TYPE

def sag_utils_selectByType( nodeType ):
        if nodeType == 'orig':
                selList = ls( type = 'mesh', io = True )
                if selList != []:
                        select( selList, replace = True )
        else:
                selList = ls( type = nodeType )
                if selList != []:
                        select( selList, replace = True )

#####################################################################################################
# SELECT ALL ORIGS WITHOUT INPUT CONNECTIONS, TOGGLE MAKE NON-INTERMEDIATE

def sag_utils_origs():
        selList = ls( sl = True )

        if selList == []:
                selList = ls( type = 'mesh', io = True )

                outList = []
                for each in selList:
                        if listConnections( each, s = True, d = False ) == None:
                                setAttr( each + '.intermediateObject', 0 )
                                outList.append( each )

                select( outList, replace = True )

        else:
                for each in selList:
                        setAttr( each + '.intermediateObject', 1 )

                select( cl = True )

#####################################################################################################
# ADD OR REMOVE SHADERS FROM SHADINGLIST

def sag_utils_shdList( mode ):
        selList = ls( sl = True )

        for	each in selList:
                conns = listConnections( each + '.message', s = False, d = True, type = 'defaultShaderList', c = False, p = True )

                if mode == 'add':	
                        if conns == None:
                                connectAttr( each + '.message', 'defaultShaderList1.shaders', na = True )

                elif mode == 'remove':
                        if conns != None:
                                disconnectAttr( each + '.message', conns[0] )

#####################################################################################################
# ADD MISSS EXPRESSION

def sag_utils_misssExpr():
        selList = ls( type = 'misss_fast_lmap_maya' )

        lmapsRes = ''
        for each in selList:
                tex = listConnections( each + '.lightmap', s = True, d = False )
                if tex != None:
                        lmapsRes += '\n' + tex[0] + '.miWidth = defaultResolution.width * 2 * 0.5;'
                        lmapsRes += '\n' + tex[0] + '.miHeight = defaultResolution.height * 0.5;'

        expression( s = lmapsRes, name = '_misss_expr' )

#####################################################################################################
# MOVE OBJECTS FROM NAMESPACE TO ROOT AND DELETE THIS NAMESPACE

def sag_utils_nmRemove():

        prompt = promptDialog(
                title = 'Remove Namespace',
                message = 'Namespace to remove (* for all):',
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        line = ''
        if prompt == 'OK':
                line = promptDialog( query = True, text = True )

        if line != '':
                if line == '*':
                        namespace( set = ':' )
                        allNm = namespaceInfo( lon = True )
                        allNm.remove( 'UI' )
                        allNm.remove( 'shared' )
                        while allNm != []:
                                for nm in allNm:
                                        namespace( mv = ( nm, ':' ), f = True )
                                        namespace( rm = nm )
                                allNm = namespaceInfo( lon = True )
                                allNm.remove( 'UI' )
                                allNm.remove( 'shared' )
                else:
                        nms = line.split( ':' )
                        for nm in nms:
                                namespace( mv = ( nm, ':' ), f = True )
                                namespace( rm = nm )

#####################################################################################################
# OVERRIDE CAST/RECEIVE ATTRIBUTES (VISIBLE IN TRANSPARENCY, SHADOW) ON SELECTED

def sag_utils_castReceiveOverride( mode, attr ):
        selList = ls( sl = True )

        rLayer = editRenderLayerGlobals( query = True, crl = True )
        if rLayer != 'defaultRenderLayer':
                for each in selList:
                        eachTr = each
                        if nodeType( each ) == 'mesh':
                                eachTr = listRelatives( each, parent = True, f = True )[0]

                        geoConn = listConnections( eachTr + '.miGeoShader', s = True, d = False )

                        if mode == 'set':
                                editRenderLayerAdjustment( each + '.' + attr[0] )
                                setAttr( each + '.' + attr[0], 0 )

                                if geoConn != None:
                                        if nodeType( geoConn[0] ) == 'forestGeoShader':
                                                editRenderLayerAdjustment( geoConn[0] + '.' + attr[1] )
                                                setAttr( geoConn[0] + '.' + attr[1], 2 )
                                                if attr[1] == 'shadow':
                                                        editRenderLayerAdjustment( geoConn[0] + '.use_various_colors' )
                                                        setAttr( geoConn[0] + '.use_various_colors', 0 )

                        elif mode == 'remove':
                                editRenderLayerAdjustment( each + '.' + attr[0], remove = True )

                                if geoConn != None:
                                        if nodeType( geoConn[0] ) == 'forestGeoShader':
                                                editRenderLayerAdjustment( geoConn[0] + '.' + attr[1], remove = True )
                                                if attr[1] == 'shadow':
                                                        editRenderLayerAdjustment( geoConn[0] + '.use_various_colors', remove = True )
        else:
                confirmDialog( title = 'Error...', message = 'Switch to any render layer!', button = [ 'OK' ] )

        select( cl = True )

#####################################################################################################
# CREATES A SET OF SHADERS FOR RGB-MASKS, SHADOW AND OCCLUSION CATCHING

def sag_auxShaders():
        selList = ls( sl = True )

        # RGBK SHADERS
        if not objExists( 'red_SHD' ):
                shd = shadingNode( 'gluk_constant', asShader = True, name = 'red_SHD' )
                setAttr( shd + '.color', 1, 0, 0, type = 'double3' )
        if not objExists( 'green_SHD' ):
                shd = shadingNode( 'gluk_constant', asShader = True, name = 'green_SHD' )
                setAttr( shd + '.color', 0, 1, 0, type = 'double3' )
        if not objExists( 'blue_SHD' ):
                shd = shadingNode( 'gluk_constant', asShader = True, name = 'blue_SHD' )
                setAttr( shd + '.color', 0, 0, 1, type = 'double3' )
        if not objExists( 'black_SHD' ):
                shd = shadingNode( 'gluk_constant', asShader = True, name = 'black_SHD' )
                setAttr( shd + '.color', 0, 0, 0, type = 'double3' )

        # OCCL SHADER
        if not objExists( 'occl_SHD' ):
                shd = shadingNode( 'gluk_constant', asShader = True, name = 'occl_SHD' )
        if not objExists( 'occl_tex' ):
                tex = shadingNode( 'mib_amb_occlusion', asTexture = True, name = 'occl_tex' )
                setAttr( tex + '.samples', 64 )
                setAttr( tex + '.max_distance', 50 )
                setAttr( tex + '.id_inclexcl', -13 )
                setAttr( tex + '.id_nonself', 13 )
        if not isConnected( 'occl_tex.outValue', 'occl_SHD.color' ):
                connectAttr( 'occl_tex.outValue', 'occl_SHD.color', force = True )

        # SHADOW SHADER
        if not objExists( 'shadow_SHD' ):
                shd = shadingNode( 'mip_matteshadow', asShader = True, name = 'shadow_SHD' )
                setAttr( shd + '.background', 1, 1, 1, type = 'double3' )
                setAttr( shd + '.ao_on', 0 )

        # DIFFUSE SHADER
        if not objExists( 'diffuse_SHD' ):
                shd = shadingNode( 'mia_material', asShader = True, name = 'diffuse_SHD' )
                setAttr( shd + '.diffuse', 1, 1, 1, type = 'double3' )
                setAttr( shd + '.reflectivity', 0 )
                setAttr( shd + '.ao_on', 1 )

        if selList != []:
                select( selList, replace = True )
        else:
                select( cl = True )

#####################################################################################################
# MOVE PIVOT FOR SELECTED OBJECTS

def sag_placePivot( mode ):
        selList = ls( sl = True )

        for each in selList:
                piv = pointPosition( each + '.rotatePivot', w = True )
                if mode == 'origin':
                        xform( each, piv = (0, 0, 0), ws = True )
                elif mode == 'base':
                        xform( each, piv = (piv[0], xform( each, query = True, ws = True, bb = True )[1], piv[2]), ws = True )
                elif mode == 'top':
                        xform( each, piv = (piv[0], xform( each, query = True, ws = True, bb = True )[4], piv[2]), ws = True )
                elif mode == 'y0':
                        xform( each, piv = (piv[0], 0, piv[2]), ws = True )

#####################################################################################################
# CREATE MISSS NETWORK

def sag_misssNetwork( mode ):
        prompt = promptDialog(
                title = 'Network Name',
                message = 'Enter Network Prefix:',
                button = [ 'OK', 'Cancel' ],
                defaultButton = 'OK',
                cancelButton = 'Cancel',
                dismissString = 'Cancel' )

        name = ''
        if prompt == 'OK':
                name = promptDialog( query = True, text = True )

        if name != '':
                tex = shadingNode( 'mentalrayTexture', asTexture = True, name = name + '_lightmap' )
                setAttr( tex + '.miWritable', 1 )
                setAttr( tex + '.miDepth', 4 )
                setAttr( tex + '.miWidth', 2048 )
                setAttr( tex + '.miHeight', 1024 )

                norm = shadingNode( 'misss_set_normal', asUtility = True, name = name + '_set_normal' )

                diff = shadingNode( 'mia_material_x', asShader = True, name = name + '_diffuse_SHD' )
                setAttr( diff + '.diffuse', 0.95, 0.95, 1.0, type = 'double3' )
                setAttr( diff + '.reflectivity', 0 )
                setAttr( diff + '.ao_on', 1 )
                setAttr( diff + '.ao_samples', 32 )
                setAttr( diff + '.ao_distance', 5.0 )

                mia = shadingNode( 'mia_material_x', asShader = True, name = name + '_spec_SHD' )
                setAttr( mia + '.diffuse', 0, 0, 0, type = 'double3' )
                setAttr( mia + '.diffuse_weight', 0 )

                lmap = shadingNode( 'misss_fast_lmap_maya', asUtility = True, name = name + '_lmap' )
                connectAttr( tex + '.message', lmap + '.lightmap' )

                if mode == 'skin' or mode == 'skin2':
                        shdType = 'shader'
                        if mode == 'skin2':
                                shdType = 'shader2'

                        shal = shadingNode( 'misss_fast_' + shdType + '_x', asUtility = True, name = name + '_shallow_SSS' )
                        connectAttr( tex + '.message', shal + '.lightmap' )
                        connectAttr( diff + '.message', shal + '.diffuse_illum' )
                        setAttr( shal + '.screen_composit', 0 )
                        setAttr( shal + '.samples', 128 )
                        setAttr( shal + '.diffuse_weight', 0.3 )
                        setAttr( shal + '.front_sss_color', 1.0, 0.85, 0.6, type = 'double3' )
                        setAttr( shal + '.front_sss_weight', 0.5 )
                        setAttr( shal + '.front_sss_radius', 8 )
                        setAttr( shal + '.back_sss_color', 0, 0, 0, type = 'double3' )
                        setAttr( shal + '.back_sss_weight', 0 )
                        setAttr( shal + '.back_sss_radius', 0 )

                        deep = shadingNode( 'misss_fast_' + shdType + '_x', asShader = True, name = name + '_SHD' )
                        connectAttr( tex + '.message', deep + '.lightmap' )
                        connectAttr( norm + '.outValue', deep + '.bump' )
                        connectAttr( deep + '.result', mia + '.additional_color' )
                        connectAttr( shal + '.result', deep + '.diffuse_illum' )
                        setAttr( deep + '.screen_composit', 0 )
                        setAttr( deep + '.samples', 128 )
                        setAttr( deep + '.diffuse_weight', 1.0 )
                        setAttr( deep + '.front_sss_color', 0.95, 0.5, 0.2, type = 'double3' )
                        setAttr( deep + '.front_sss_weight', 0.4 )
                        setAttr( deep + '.front_sss_radius', 25 )
                        setAttr( deep + '.back_sss_color', 0.7, 0.1, 0.1, type = 'double3' )
                        setAttr( deep + '.back_sss_weight', 0.5 )
                        setAttr( deep + '.back_sss_radius', 25 )
                        setAttr( deep + '.back_sss_depth', 25 )

                elif mode == 'simple' or mode == 'simple2':
                        shdType = 'shader'
                        if mode == 'simple2':
                                shdType = 'shader2'

                        shd = shadingNode( 'misss_fast_' + shdType + '_x', asShader = True, name = name + '_SHD' )
                        connectAttr( tex + '.message', shd + '.lightmap' )
                        connectAttr( diff + '.message', shd + '.diffuse_illum' )
                        connectAttr( norm + '.outValue', shd + '.bump' )
                        connectAttr( shd + '.result', mia + '.additional_color' )
                        setAttr( shd + '.screen_composit', 0 )
                        setAttr( shd + '.samples', 128 )
                        setAttr( shd + '.diffuse_weight', 0.5 )
                        setAttr( shd + '.front_sss_color', 0.8, 0.4, 0.1, type = 'double3' )
                        setAttr( shd + '.front_sss_weight', 0.5 )
                        setAttr( shd + '.front_sss_radius', 10 )
                        setAttr( shd + '.back_sss_color', 0.8, 0.4, 0.1, type = 'double3' )
                        setAttr( shd + '.back_sss_weight', 0.5 )
                        setAttr( shd + '.back_sss_radius', 10 )
                        setAttr( shd + '.back_sss_depth', 10 )

#####################################################################################################
# TRANSFER ALL CONNECTIONS FROM ONE NODE TO ANOTHER

def sag_transferConnections( mode ):
        selList = ls( selection = True )

        #INCOMING CONNECTIONS
        if mode == 'both' or mode == 'in':
                conns = listConnections( selList[0], source = True, destination = False, plugs = True, connections = True )
                if conns != None:
                        for i in xrange(0, len(conns), 2 ):
                                connectAttr( conns[i+1], selList[1] + conns[i][conns[i].find('.'):], force = True )

        #OUTGOING CONNECTIONS
        if mode == 'both' or mode == 'out':
                conns = listConnections( selList[0], source = False, destination = True, plugs = True, connections = True )
                if conns != None:
                        for i in xrange(0, len(conns), 2 ):
                                connectAttr( selList[1] + conns[i][conns[i].find('.'):], conns[i+1], force = True  )

#####################################################################################################
# SET EPISODE LENGTH OF ALL ANIMATED FORESTGEOSHADERS TO THE LENGTH OF THE SCENE BY TIMELINE

def sag_forestLength():
        for each in ls( type = 'forestGeoShader' ):
                if getAttr( each + '.object_filename' ).find( '#' ) > -1:
                        setAttr( each + '.episode_length', int( playbackOptions( query = True, max = True ) ) )


#####################################################################################################
# RETURN STARTUP CAMERAS TO DEFAULT

def sag_utils_startupCamerasFix():
        setAttr( 'persp.t', 2400, 1800, 2400, type = 'double3' )
        setAttr( 'persp.r', -28, 45, 0, type = 'double3' )
        setAttr( 'persp.s', 1, 1, 1, type = 'double3' )
        setAttr( 'persp.v', 0 )
        setAttr( 'persp.nearClipPlane', 1.0 )
        setAttr( 'persp.farClipPlane', 10000.0 )
        setAttr( 'perspShape.horizontalFilmAperture', 1.417 )
        setAttr( 'perspShape.verticalFilmAperture', 0.578 )
        setAttr( 'persp.backgroundColor', 0, 0, 0, type = 'double3' )
        setAttr( 'persp.filmFit', 1 )
        setAttr( 'persp.displayGateMask', 1 )
        setAttr( 'persp.displayGateMaskColor', 0.5, 0.5, 0.5, type = 'double3' )
        setAttr( 'persp.overscan', 1.95 )

        setAttr( 'top.t', 0, 5000, 0, type = 'double3' )
        setAttr( 'top.r', -90, 0, 0, type = 'double3' )
        setAttr( 'top.s', 1, 1, 1, type = 'double3' )
        setAttr( 'top.v', 0 )
        setAttr( 'top.orthographic', 1 )
        setAttr( 'top.orthographicWidth', 1000 )

        setAttr( 'front.t', 0, 0, 5000, type = 'double3' )
        setAttr( 'front.r', 0, 0, 0, type = 'double3' )
        setAttr( 'front.s', 1, 1, 1, type = 'double3' )
        setAttr( 'front.v', 0 )
        setAttr( 'front.orthographic', 1 )
        setAttr( 'front.orthographicWidth', 1000 )

        setAttr( 'side.t', 5000, 0, 0, type = 'double3' )
        setAttr( 'side.r', 0, 90, 0, type = 'double3' )
        setAttr( 'side.s', 1, 1, 1, type = 'double3' )
        setAttr( 'side.v', 0 )
        setAttr( 'side.orthographic', 1 )
        setAttr( 'side.orthographicWidth', 1000 )

#####################################################################################################
# SET ALL TEXTURE PATHS TO LOCAL DIRECTORY

def sag_utils_localizeFileNodes( dirPath ):
        for each in ls( type = 'file' ):
                filePath = getAttr( each + '.fileTextureName' )
                setAttr( each + '.fileTextureName', dirPath + '/' + filePath.replace( '\\', '/' ).split( '/' )[-1], type = 'string' )

#####################################################################################################
# SET ALL FUR MAPS TO LOCAL DIRECTORY

def sag_utils_localizeFurMaps( dirPath ):
        attrs = [   'BaseColorMap', 
                    'TipColorMap', 
                    'BaseAmbientColorMap', 
                    'TipAmbientColorMap', 
                    'SpecularColorMap',
                    'SpecularSharpnessMap',
                    'LengthMap',
                    'BaldnessMap',
                    'InclinationMap',
                    'RollMap',
                    'PolarMap',
                    'BaseOpacityMap',
                    'TipOpacityMap',
                    'BaseWidthMap',
                    'TipWidthMap',
                    'BaseCurlMap',
                    'TipCurlMap',
                    'ScraggleMap',
                    'ScraggleFrequencyMap',
                    'ScraggleCorrelationMap',
                    'ClumpingMap',
                    'ClumpingFrequencyMap',
                    'ClumpShapeMap',
                    'SegmentsMap',
                    'AttractionMap',
                    'OffsetMap'
                    ]

        for each in ls( type = 'FurDescription' ):
                for attr in attrs:
                        for i in getAttr( each + '.' + attr, mi = True ):
                                filePath = getAttr( each + '.' + attr + '[' + str(i) + ']' )
                                if filePath != None:
                                        setAttr( each + '.' + attr + '[' + str(i) + ']', dirPath + '/' + filePath.replace( '\\', '/' ).split( '/' )[-1], type = 'string' )
