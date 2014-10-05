__author__ = 'Andrewwillish'

import maya.cmds as cmds
import os, imp
import maya.mel as mel
import asiistMenuBuilder

#Determining root path
rootPathVar=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

#module launcher
def moduleLauncher(name,path):
    imp.load_compiled(name,path) if path.endswith('.pyc')==True else imp.load_source(name,path)
    return

#get main window name
mainWindow = mel.eval('$temp1=$gMainWindow')

#delete previous menu
try:
    cmds.deleteUI('asiistMenu',menu=True)
except:
    pass

#create menu
cmds.menu('asiistMenu',l='ASIIST', tearOff=True,p=mainWindow)
cmds.menuItem('rehash',l='Rehash Menu',p='asiistMenu',\
              c=asiistMenuBuilder.hash)
