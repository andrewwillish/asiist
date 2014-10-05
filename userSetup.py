#General User Setup

#import module
import maya.utils as utils
import maya.cmds as cmds
import maya.mel as mel
import os, sys
import maya.OpenMaya as om
import xml.etree.ElementTree as ET


#CALLBACK==============================================================================================
def beforeSaveCallbackFun(*args):
    global currentLayerVar,daStatLis,allPanelLis
    currentLayerVar=cmds.editRenderLayerGlobals(q=True, crl=True)
    cmds.editRenderLayerGlobals(crl='defaultRenderLayer')
    allPanelLis=cmds.getPanel(type='modelPanel')
    daStatLis=[]
    for chk in allPanelLis:
        daStatLis.append(cmds.modelEditor(chk,q=True,da=True))
        cmds.modelEditor(chk,e=True,da='wireframe')
    return

def afterSaveCallbackFun(*args):
    global currentLayerVar,daStatLis,allPanelLis
    cmds.editRenderLayerGlobals(crl=currentLayerVar)
    cnt=0
    for chk in allPanelLis:cmds.modelEditor(chk,e=True,da=daStatLis[cnt]);cnt+=1
    return
#CALLBACK==============================================================================================

#SCRIPTJOB=============================================================================================
#note:  this scriptjob will check for new module installed. If it follow standard system, it will
#       add it to the system whenever the system is idle. This method strictly for python only.
def moduleCheck(*args):

    return
#SCRIPTJOB=============================================================================================

def environmentPrep(*args):
    #get environment selection
    selItem=cmds.textScrollList('startupTextScroll',q=True,si=True)
    if selItem==None:
        cmds.confirmDialog(icn='warning', t='Error', message='Please select an environment.',\
                           button=['Ok'])
    else:
        #close layoutdialog
        cmds.layoutDialog(dismiss='Set Selected Envi')

        #get root
        root=ET.parse('startup.xml').getroot()

        #get project path
        selItem=selItem[0]
        for chk in root[1]:
            if str(chk.tag)==str(selItem):projPath=str(chk.text)

        #prepare python general directory and make one if not available then add it to system path
        genPyLis=[]
        for chk in root[0][0]:genPyLis.append(chk.text)
        for chk in genPyLis: os.makedirs(chk) if os.path.isdir(chk)==False else None
        for chk in genPyLis: sys.path.append(chk);

        #add general python path to system
        if os.path.isdir(projPath)==False: os.makedirs(projPath)
        sys.path.append(projPath)

        #declare scriptjob
        cmds.scriptJob(ie=moduleCheck)
    return

def uiFunction(*args):
    #startup found
    tree=ET.parse('startup.xml')
    root=tree.getroot()

    #ui script
    cmas=cmds.columnLayout(adj=True)
    cmds.textScrollList('startupTextScroll',w=250)
    cmds.separator()
    cmds.rowColumnLayout(nc=3,cw=[(1,100),(2,100),(3,50)])
    cmds.button(l='Set Selected Envi',c=environmentPrep)
    cmds.button(l='Set Default Envi',c="cmds.layoutDialog(dis='Set Default Envi')")
    cmds.button(l='Close', bgc=[125,0,0,],c='cmds.quit(f=True)')

    #populating ui script
    cmds.textScrollList('startupTextScroll',e=True,ra=True)
    for chk in root[1]:cmds.textScrollList('startupTextScroll',e=True,a=str(chk.tag))
    return

def startup(*args):
    #validate startup.xml
    if os.path.isfile('startup.xml')==False:
        #startup not found
        repVar=cmds.confirmDialog(icn='critical',t='error',message='There is no startup.xml found!',\
                           button=['Start Default','Close'])
        if repVar=='Close':cmds.quit(f=True)
    else:
        #call layoutdialog
        try:
            cmds.layoutDialog(ui=uiFunction)
        except:
            pass

    #start callback function
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave,beforeSaveCallbackFun)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave,afterSaveCallbackFun)
    return

#initialize startup
utils.executeDeferred(startup)