__author__ = 'Andrewwillish'

import maya.cmds as cmds
import os,sys, imp
import maya.mel as mel

def hash(*args):
    mainWindow = mel.eval('$temp1=$gMainWindow')
    for sourcePath in sys.path:
        if os.path.isdir(sourcePath):
            if sourcePath.endswith('/')==True:sourcePath=sourcePath[:sourcePath.rfind('/')]
            if os.path.isfile(sourcePath+'/asiistMenu.py'):
                sourceName=sourcePath[sourcePath.rfind('/')+1:]
                imp.load_source(sourceName,sourcePath+'/asiistMenu.py')
    return