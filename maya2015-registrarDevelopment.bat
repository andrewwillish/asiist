::Get current directory
set mypath=%~dp0

::Set maya script path
set MAYA_SCRIPT_PATH=%mypath:~0,-1%;

::Set maya plugin path
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;

::Set python path
set PYTHONPATH=%mypath:~0,-1%;Z:\development\pyDevPackage

::Start maya
"C:\Program Files\Autodesk\Maya2015\bin\maya.exe"