import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore
from  .. import RD_globals 
from ..RD_parser import RD_parse_sdf
_icon_dir__=os.path.join(RD_globals.ICON_PATH,"world_properties.svg")
class world():
    def __init__(self):
        pass 

class world_properties(QtGui.QWidget):
    def __init__(self):
        super(world_properties,self).__init__()
        self.parent="root"
        self.name='world'
        self.world_elems=RD_parse_sdf.sdf_parse(file="world.sdf").data_structure
        self.initUI()
        #This  is initialized to allow the restore defaults function
        #it basically stores the default values for later acces 
    
    def initUI(self):
        self.ui_path=os.path.join(RD_globals.UI_PATH,"world_properties.ui")
        self.world_form=FreeCADGui.PySideUic.loadUi(self.ui_path,self)
        self.world_form.show()


#initialize  class      
class init_sdf_world:
  
    def GetResources(self):
        return {"Pixmap"  :_icon_dir__, # the name of a svg file available in the resources
                "Accel"   : "Shift+w", # a default shortcut (optional)
                "MenuText": "sdf world stuff",
                "ToolTip" : "edit world properties"}

    def Activated(self):
        """Do something here"""
        w=world_properties()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand("world_properties", init_sdf_world())

