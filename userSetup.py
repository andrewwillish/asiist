#General User Setup

#import module
import maya.utils as utils
import maya.cmds as cmds
import maya.mel as mel
import os, asiistMain
import maya.OpenMaya as om
import xml.etree.ElementTree as ET

#determining window root
winRoot=os.environ['ProgramFiles']
winRoot=winRoot[:winRoot.find('\\')+1]

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

#environmentPrep function to start build and connect a menu.
def environmentPrep(*args):
    #get environment selection
    selItem=cmds.textScrollList('startupTextScroll',q=True,si=True)
    if selItem==None:
        cmds.confirmDialog(icn='warning', t='Error', message='Please select an environment.',\
                           button=['Ok'])
    else:
        #close layoutdialog
        cmds.layoutDialog(dismiss='Set Selected Envi')

        #declare project credential
        try:
            #write temporary file
            asiistMain.declareProjectEnvi(selItem[0])

            #run menuBuilder
            asiistMain.hash()
        except Exception as e:
            print e
            cmds.confirmDialog(icn='warning', t='Error',\
                               message='Unable to create temporary file. Switching to default environment.',\
                               button=['Ok'])
    return

#UI function script for the startup. This function to be called by layoutDialog
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

#startup function. This is the entry point of the whole session
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
            cmds.layoutDialog(ui=uiFunction,t='ASIIST Startup')
        except:
            pass

    #start callback function
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave,beforeSaveCallbackFun)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave,afterSaveCallbackFun)
    return

#initialize startup sequence
utils.executeDeferred(startup)