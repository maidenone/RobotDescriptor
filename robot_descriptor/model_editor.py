import FreeCAD
import FreeCADGui
import robot_descriptor.common as common
import os

from .RD_utils import parse_asm4_model
from PySide.QtGui import QStandardItemModel,QStandardItem


class standard_item(QStandardItem):
    def __init__(self,text):
        super().__init__()
        self.model_elem=None
        self.setText(text)
        
class ModelEditor:
    def __init__(self):
        # find all objects of type 'App::Link'
        #doc=FreeCAD.ActiveDocument
        self.links_hierarchy=parse_asm4_model.read_assembly()
        self.ModelEditorUi=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'model_editor.ui'))
        self.link_model=QStandardItemModel()
        self.root_node=self.link_model.invisibleRootItem()
        self.tree_setup(self.links_hierarchy["children"],self.root_node)
        #hide header
        self.ModelEditorUi.link_tree.setHeaderHidden(True)
        self.ModelEditorUi.link_tree.setModel(self.link_model)
        self.ModelEditorUi.exec()
        
    def tree_setup(self,link_hierarchy,item):
        for child in link_hierarchy:
            row=standard_item(child["name"])
            item.appendRow(row)
            self.tree_setup(child["children"],row)
        return 
            
    
    
class Model_properties():
    """My new command"""

    def GetResources(self):
        return {"Pixmap"  : os.path.join(common.ICON_PATH,"edit.svg"),# the name of a svg file available in the resources
                "Accel"   : "Shift+E", # a default shortcut (optional)
                "MenuText": "Model Edits",
                "ToolTip" : "Edit link and joint properties"}

    def Activated(self):
        self.edits=ModelEditor()
        return 

    def IsActive(self):
        if hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
            return True
        else:
            return False

FreeCADGui.addCommand("Model_Editor", Model_properties())
