__author__ = 'Andrewwillish'

#import module
import maya.cmds as cmds
import os,sys, imp
import maya.mel as mel
import xml.etree.ElementTree as ET

#determining win root
winRoot=os.environ['ProgramFiles']
winRoot=winRoot[:winRoot.find('\\')+1]

#call project environment
def getEnvi(*args):
    global projEnvi
    #get project path of the projEnvi
    projPath=''
    root=ET.parse('startup.xml').getroot()
    for chk in root[1]:
        if str(chk.tag)==str(projEnvi):projPath=str(chk.text)

    #get information from projInfo.xml following projPath
    if os.path.isfile(projPath+'/projInfo.xml')==False:raise StandardError, 'error : projInfo file not found'

    root=ET.parse(projPath+'/projInfo.xml').getroot()
    returnLis=[]
    for chk in root:returnLis.append((chk.tag,chk.text))
    return returnLis

#function to declare current project environment
def declareProjectEnvi(enviSel):
    global projEnvi
    #declare projEnvi
    if 'projEnvi' not in globals():
        projEnvi=''

    #get old project path
    projPath=''
    root=ET.parse('startup.xml').getroot()
    for chk in root[1]:
        if str(chk.tag)==str(projEnvi):
            projPath=str(chk.text)

    #remove old project path from sys.path
    if projPath!='':sys.path.remove(projPath)

    #assign projEnvi with new project
    projEnvi=enviSel

    #get new project path
    for chk in root[1]:
        if str(chk.tag)==str(projEnvi):
            projPath=str(chk.text)

    #set new project path to sys.path
    sys.path.append(projPath)
    return projEnvi

#function to process project switching procedure
def switchProc(*args):
    global projEnvi
    #get selection
    selItem=cmds.textScrollList('switchEnviTextScroll',q=True,si=True)
    if selItem==None:
        raise StandardError, 'error : no environment selected'

    #declare new environement
    declareProjectEnvi(str(selItem[0]))

    #rehash menu file
    hash()

    cmds.confirmDialog(icn='information', t='Done',\
                       m='Envrinoment has been switched.', button=['Ok'])
    return

#function to start project switching environment
def switchEnvi(*args):
    #get startup.xml root
    tree=ET.parse('startup.xml')
    root=tree.getroot()

    #create window
    if cmds.window('switchEnvi',exists=True):
        cmds.deleteUI('switchEnvi',window=True)
    cmds.window('switchEnvi', t='Switch Environment', s=False)
    cmds.columnLayout(adj=True)
    cmds.textScrollList('switchEnviTextScroll', w=150,dcc=switchProc)
    for chk in root[1]:cmds.textScrollList('switchEnviTextScroll',e=True,a=str(chk.tag))
    cmds.showWindow()
    return

#function to destroy and re-build system menu
def hash(*args):
    global projEnvi
    #delete all previous menu
    #menu indicated by prefix m_
    for chk in cmds.lsUI(menus=True):
        if chk.startswith('m_'):
            cmds.deleteUI(chk, menu=True)

    #get project path
    root=ET.parse('startup.xml').getroot()
    selItem=projEnvi
    for chk in root[1]:
        if str(chk.tag)==str(selItem):
            projPath=str(chk.text)

    #add general python path to system
    genPyLis=[]
    for chk in root[0][0]:genPyLis.append(chk.text)
    for chk in genPyLis: os.makedirs(chk) if os.path.isdir(chk)==False else None
    for chk in genPyLis:
        try:
            sys.path.remove(chk)
        except:
            pass
        sys.path.append(chk)

    #add projects python path to system
    if os.path.isdir(projPath)==False:
        os.makedirs(projPath)
    try:
        sys.path.remove(projPath)
    except:
        pass
    sys.path.append(projPath)

    #generating menu
    mainWindow = mel.eval('$temp1=$gMainWindow')
    for sourcePath in sys.path:
        if os.path.isdir(sourcePath):
            if sourcePath.endswith('/')==True:sourcePath=sourcePath[:sourcePath.rfind('/')]
            if os.path.isfile(sourcePath+'/asiistMenu.py'):
                sourceName=sourcePath[sourcePath.rfind('/')+1:]
                imp.load_source(sourceName,sourcePath+'/asiistMenu.py')

    #setup data information to maya
    for chk in getEnvi():
        if chk[0]=='unit': cmds.currentUnit(time=chk[1])
    return