#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 29 Jun 2015 11:28:01
#========================================
import maya.cmds as mc
import maya.mel as mel
import os
import modulesPath
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def pupMaya2mental(mentalVersion):
        destPath = os.getenv('DEST_PATH_WIN')
        rootPath, shadersPath = {	
                3.8:('c:/Program Files/Autodesk/mrstand3.8.1-adsk2011/bin', destPath + '/mental3.8.1'),
                3.11:('c:/Program Files/Autodesk/mrstand3.11.1-adsk2014/bin', destPath + '/mental3.11.1')
                }[mentalVersion]

        os.putenv('RAY_COMMAND', '"' + rootPath + '/ray.exe"')

        os.putenv('MR_VERSION', str( mentalVersion ) )

        miModulesPaths, binModulesPaths = modulesPath.getMiBinString()
        #os.putenv('MI_RAY_INCPATH', shadersPath + '/mi;' +  miModulesPaths)
        #os.putenv('MI_LIBRARY_PATH', shadersPath + '/bin;' +  binModulesPaths)
        #os.putenv('MI_ROOT', rootPath)
        mel.eval('pup_maya_2_mental(3);')

        mc.checkBoxGrp('pup_m2mrOverrideEnv', e=True, v1=1)
        mc.textFieldGrp('pup_m2mrMiRoot', e=True, tx= rootPath )
        mc.textFieldGrp('pup_m2mrMiInclude', e=True, tx= shadersPath + '/mi;' +  miModulesPaths )
        mc.textFieldGrp('pup_m2mrMiLib', e=True, tx= shadersPath + '/bin;' +  binModulesPaths )
        mc.textFieldGrp('pup_m2mrMiDir', e=True, tx= "C:/Temp/" )
        mc.optionMenuGrp('pup_m2mrVerboseM', e=True, sl=5)
        #mc.textFieldGrp('pup_m2mrCommandLine', e=True, tx= '-finalgather_passes 0 -memory 1000000' )
        mc.textFieldGrp('pup_m2mrCommandLine', e=True, tx= '-memory 1000000' )
        mc.checkBoxGrp('pup_m2mrUniqueMI', e=True, v1=1)
        mc.optionMenuGrp('pup_m2mrPriority', e=True, sl=3)
