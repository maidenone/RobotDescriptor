import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore

_icon_dir__=os.path.join(FreeCAD.getUserAppDataDir(), "Mod", "RobotDescriptor")+"/robot_descriptor/icons/world_properties.svg"

class world_properties(QtGui.QWidget):
    def __init__(self):
        pass
    
class init_sdf_world:
  
    def GetResources(self):
        return {"Pixmap"  :_icon_dir__, # the name of a svg file available in the resources
                "Accel"   : "Shift+w", # a default shortcut (optional)
                "MenuText": "sdf world stuff",
                "ToolTip" : "edit world properties"}

    def Activated(self):
        """Do something here"""
        
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand("world_properties", init_sdf_world())

