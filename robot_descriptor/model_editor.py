from typing import Any
import FreeCAD
import FreeCADGui
import robot_descriptor.common as common
import os
from PySide2 import QtGui
import copy 
from .RD_utils import initialize_element_tree

import xml.etree.ElementTree as ET

from .RD_utils import parse_asm4_model
from PySide2.QtGui import QStandardItemModel,QStandardItem
from PySide2.QtWidgets  import QTreeView,QDialog,QSplitter,QGridLayout,QTabWidget,QHBoxLayout,QWidget
from PySide2.QtCore import QSize, Qt,QModelIndex,QItemSelectionModel,Signal
from .sdf_elements import link
from .sdf_elements import visual
from .sdf_elements import collision

link_img=QtGui.QImage(os.path.join(common.ICON_PATH,"link16.png"))
ref_img=QtGui.QImage(os.path.join(common.ICON_PATH,"ref16.png"))


#start standard item
class ModelItem(QStandardItem):
    def __init__(self,model_editor_cls,text,type='link'):
        super().__init__()
        # data to describe the model 
        
        #types   ref,link ... .
        self.text=text
        self.type=type
        #set the text to be displayed
        self.setText(text)
        self.setEditable(False)
        self.model_cls=model_editor_cls
        #this is the parent ui 
        # self.Model_editor_ui=self.model_cls.Model_editor_ui
    
        #Tasks 
        # 1. Implement function to 
                # i. calculate inertia and write the info to the inertial element ,this might  be
                #   implemented in the inertial class
                # ii. extract maerial data e.g color of link... , and write to material element
                # 
        # 2.  add user roles to get element data after disabled ui icons have been removed 
        #       so that calling the on the item with the role will return the element  after  appending them as required 
        # 3. add slot that can be triggered when user breaks reference  so that an element of type reference can 
        #       create its own links and not refer to parent ref item ,  also  another to  create links to a parent item 
        #       and one to update ui when to item is selected in the tree view 
        
        #linked
        if self.type !='ref':
            self.break_ref()
    
    def init_elements(self):
        self.collision_element=initialize_element_tree.convdict_2_tree('collision.sdf').get_element
        self._link_element=initialize_element_tree.convdict_2_tree('link.sdf').get_element
        self._inertial_element=initialize_element_tree.convdict_2_tree("inertial.sdf").get_element
        self.surface_element=initialize_element_tree.convdict_2_tree("surface.sdf").get_element
        self._visual_element=initialize_element_tree.convdict_2_tree("visual.sdf").get_element
        self._material_element=initialize_element_tree.convdict_2_tree('material.sdf').get_element
        
          
    def  create_ref(self,item):
        
        self.collision_element=item.collision_element
        self._link_element=item._link_element
        self._inertial_element=item._inertial_element
        self.surface_element=item.surface_element
        self._visual_element=item._visual_element
        self._material_element=item._material_element
        self.emitDataChanged()
        
    def break_ref(self):
        self.init_elements()
        self.emitDataChanged()
        
    def selected(self):
        #this will called when an item is clicked 
        #update  elements 
        self.model_cls._link.update_elements(self)
        self.model_cls._visual.update_elements(self)
        self.model_cls._collision.update_elements(self)
        
            
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
class ModelEditor(QWidget):
   
    
    def __init__(self,elem_struct):
        # find all objects of type 'App::Link'
        #doc=FreeCAD.ActiveDocument
        super(ModelEditor,self).__init__()
        
        self._elem_struct=elem_struct
        self.links_hierarchy=parse_asm4_model.read_assembly()
        if self.links_hierarchy is None:
            return 
        # self.ModelEditorUi=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'model_editor.ui'))
        
        #subelements
        self.current_elems=[]
        #dictionary of all links and their  associated elements 
        #{link name: [link,collison,visual], ...}
        self.elems={}
        #used for creating refernces for item of type ref
        self.referenced_elems={}
    #ui's
        self.collision_ui=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'collision.ui'))
        self.link_ui=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'link.ui'))
        self.visual_ui=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,'visual.ui'))
    #end ui's
    #elements 
        self._link=link.link(self.link_ui)
        self._visual=visual.visual(self.visual_ui)
        self._collision=collision.collison(self.collision_ui)
    #end elements 
    
        self.setUpUI()
        
        #create model 
        self.link_model=QStandardItemModel()
        self.link_model.setColumnCount(1)
        self.root_node=self.link_model.invisibleRootItem()
        self.model_tree_config(self.links_hierarchy["children"],self.root_node)
        
        #add callback 
        self.config()
        
    # start header related
        self.link_model.setHorizontalHeaderLabels(["Model Tree"])
        #set the  tree to resize automatically based on the display requirements
    #end header related 
    
    #set view model 
        self.view.setModel(self.link_model)
        mdl_idx0=self.link_model.index(0,0,self.view.rootIndex())
        self.view.selectionModel().select(mdl_idx0,QItemSelectionModel.Select)
    #display dialog 
        self.show()
#end __init__()
   
        
    def sizeHint(self) -> QSize:
        return QSize(1030,764)
    
    def setUpUI(self):
        self.setWindowTitle("ModelEditor")
    #splitter
        self.splitter=QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
    #create the treeview 
        self.view=QTreeView(self.splitter)
        self.view.setHeaderHidden(False)
        self.view.setSelectionMode(self.view.SingleSelection)
    #set layout of the main dialog
        grid=QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.splitter)
    #create the tab widget 
        tab=QTabWidget(self.splitter)
        tab.addTab(self.link_ui,"link")
        tab.addTab(self.collision_ui,"collision")
        tab.addTab(self.visual_ui,"visual")
        
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(tab)
        
        
    
    def config(self):
        self.view.clicked[QModelIndex].connect(self.on_tree_item)
      
    
    def on_tree_item(self,index):
        item = self.link_model.itemFromIndex(index)
        # label=item.data(Qt.DisplayRole)
        item.selected()
        

    def model_tree_config(self,link_str,std_itm):
        ref_links=[]
    #create the tree view structure   
        def setup(link_hierarchy,item):
            #iterate throuhg all children create items and the to tree
            #seee parse_asm4_model.py 
            for child in link_hierarchy:
                name=child["name"]
                row=ModelItem(self,child["name"],child['type'])
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
                    self.referenced_elems[child['name']]=row

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
            # item.ref_idx=self.referenced_elems[ref_label]
            item.create_ref(self.referenced_elems[ref_label])

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
