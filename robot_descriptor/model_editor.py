from typing import Any
import FreeCAD
import FreeCADGui
import robot_descriptor.common as common
import os
from PySide2 import QtGui
import copy 

from .RD_utils import parse_asm4_model
from PySide2.QtGui import QStandardItemModel,QStandardItem
from PySide2.QtCore import Qt,QModelIndex


link_img=QtGui.QImage(os.path.join(common.ICON_PATH,"link16.png"))
ref_img=QtGui.QImage(os.path.join(common.ICON_PATH,"ref16.png"))
#start standard item
class standard_item(QStandardItem):
    def __init__(self,text,type='link',ref_idx=None):
        super().__init__()
        # data to describe the model 
        self.text=text
        self.type=type
        #index of the refered to  link/object 
        self.ref_idx=ref_idx
        #set the text to be displayed
        self.setText(text)
        self.setEditable(False)
        
    def data(self, role: int = ...) -> Any:
        if role==Qt.DisplayRole:
            return self.text
        
        if role==Qt.DecorationRole:
            if self.type=='link':
                return link_img
            elif self.type=='ref':
                return ref_img
            else:
                return 
            
    
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
        
        #subelements 
        from .sdf_elements import link
        #link
        self._link=link.link(self.ModelEditorUi)
        #visual
        from .sdf_elements import visual
        self._visual=visual.visual(self.ModelEditorUi)
        #collision
        from .sdf_elements import collision
        self._collision=collision.collison(self.ModelEditorUi)
        
        self.current_elems=[]
        #dictionary of all links and their  associated elements 
        #{link name: [link,collison,visual], ...}
        self.elems={}
        #used for creating refernces for item of type ref
        self.referenced_elems={}
        
        #create model 
        self.link_model=QStandardItemModel()
        self.link_model.setColumnCount(1)
        self.root_node=self.link_model.invisibleRootItem()
        self.model_tree_config(self.links_hierarchy["children"],self.root_node)
        
        #add callback 
        self.config()
        
    # start header related 
        self.ModelEditorUi.link_tree.setHeaderHidden(False)
        self.link_model.setHorizontalHeaderLabels(["Model Tree"])
        #set the  tree to resize automatically based on the display requirements
    #end header related 
    
        self.ModelEditorUi.link_tree.setModel(self.link_model)
        
        self.ModelEditorUi.exec()
        
#end __init__()

    def config(self):
        self.ModelEditorUi.link_tree.clicked[QModelIndex].connect(self.on_tree_item)
        
    def on_tree_item(self,index):
        item = self.link_model.itemFromIndex(index)
        label=item.data(Qt.DisplayRole)
        #update data related  to elems 
        self.current_elems=self.elems[label]
        self._link.update_elem(self.current_elems[0])
        self._collision.update_elem(self.current_elems[1])
        self._visual.update_elem(self.current_elems[2])
        

    def model_tree_config(self,link_str,std_itm):
        ref_links=[]
    #create the tree view structure   
        def setup(link_hierarchy,item):
            #iterate throuhg all children create items and the to tree
            #seee parse_asm4_model.py 
            for child in link_hierarchy:
                name=child["name"]
                row=standard_item(child["name"],child['type'])
                item.appendRow(row)
                #make reference to the index of referenced link
                #This assumes the link already exists in the referenced_elems dictionary 
                if child['type']=='ref':
                    # row.ref_idx=self.referenced_elems[child["ref_label"]]
                    # #refer to the data in the refered link 
                    # #since the links are similar 
                    # #this can be  updated by right clicking on the  tree element and clicking break reference 
                    # self.elems[child['name']]=self.elems[child["ref_label"]]
                    
                    #just update the ref_links since the link might not be defined yet 
                    ref_links.append([row,child["ref_label"],name])
                #store index to referred link
                elif child['type']=='link':
                    #add to referenced elements 
                    self.referenced_elems[child['name']]=self.link_model.indexFromItem(row)
                    # get data and store it in corresponding list 
                    link_elem=copy.deepcopy(self._link.get_default_elem())
                    collision_elem=copy.deepcopy(self._collision.get_default_elem())
                    visual_elem=copy.deepcopy(self._visual.get_default_elem())
                    #update element data
                    self.elems[child['name']]=[link_elem,collision_elem,visual_elem]
                else:
                    pass 
                #deb
                ####
                #recursion 
                setup(child["children"],row)
            return 
        setup(link_str,std_itm)
        #add ref_link related data 
        for item,ref_label,name in ref_links:
            item.ref_idx=self.referenced_elems[ref_label]
            self.elems[name]=self.elems[ref_label]
        

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
        if hasattr(FreeCAD.ActiveDocument,"Assembly") or hasattr(FreeCAD.ActiveDocument,"Model"):
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
