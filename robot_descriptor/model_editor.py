import FreeCAD
import FreeCADGui
import robot_descriptor.common as common
import os

from .RD_utils import parse_asm4_model
from PySide.QtGui import QStandardItemModel,QStandardItem,QHeaderView

#start standard item
class standard_item(QStandardItem):
    def __init__(self,text,elements):
        super().__init__()
        # data to describe the model 
        self.link_elem=elements[0]
        self.collision_elem=elements[1]
        self.material_elem=elements[2]
        #set the text to be displayed
        self.setText(text)
        self.setEditable(False)
    
#end standard Item   
#==============================================
#model editor 
class ModelEditor:
    def __init__(self,elem_struct):
        # find all objects of type 'App::Link'
        #doc=FreeCAD.ActiveDocument
        self._elem_struct=elem_struct
        self.links_hierarchy=parse_asm4_model.read_assembly()
        if self.links_hierarchy is None:
            return 
        self.ModelEditorUi=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'model_editor.ui'))
        self.link_model=QStandardItemModel()
        self.link_model.setColumnCount(1)
        self.root_node=self.link_model.invisibleRootItem()
        self.tree_setup(self.links_hierarchy["children"],self.root_node)
        
    # start header related 
        self.ModelEditorUi.link_tree.setHeaderHidden(False)
        self.link_model.setHorizontalHeaderLabels(["Model Tree"])
        #set the  tree to resize automatically based on the display requirements
        header = self.ModelEditorUi.link_tree.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
    #end header related 
    
        self.ModelEditorUi.link_tree.setModel(self.link_model)
        
        self.ModelEditorUi.exec()
        
    #create the tree structure   
    def tree_setup(self,link_hierarchy,item):
        #iterate throuhg all children create items and the to tree
        for child in link_hierarchy:
            row=standard_item(child["name"])
            
            item.appendRow(row)
            self.tree_setup(child["children"],row)
        return 
        
        
        
        

#+===============================
#start command
#================================
class Model_properties():
    """My new command"""

    def GetResources(self):
        return {"Pixmap"  : os.path.join(common.ICON_PATH,"edit.svg"),# the name of a svg file available in the resources
                "Accel"   : "Shift+E", # a default shortcut (optional)
                "MenuText": "Model Edits",
                "ToolTip" : "Edit link and joint properties"}

    def Activated(self):
        if hasattr(FreeCAD.ActiveDocument,"Assembly"):
            doc=FreeCAD.ActiveDocument
            self._root_dict=doc.Robot_Description.Proxy.element_dict
            self.edits=ModelEditor(self._root_dict)
        else:
            FreeCAD.Console.PrintMessage("document does not contain an assembly\n")
        return 

    def IsActive(self):
        if hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
            return True
        else:
            return False

FreeCADGui.addCommand("Model_Editor", Model_properties())
