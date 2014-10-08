__author__ = 'Andrewwillish'

import maya.cmds as cmds
import os, imp,sys
import maya.mel as mel
import asiistMain

#Determining root path
rootPathVar=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

#module launcher
def moduleLauncher(name,path):
    imp.load_compiled(name,path) if path.endswith('.pyc')==True else imp.load_source(name,path)
    return

#get main window name
mainWindow = mel.eval('$temp1=$gMainWindow')


#create menu
try:
    cmds.menu('m_entongTools',l='ENTONG Tools', tearOff=True,p=mainWindow)
except:
    pass