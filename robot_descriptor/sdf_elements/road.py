from .. import common
from ..RD_utils import initialize_element_tree
import copy 
from PySide import QtGui,QtCore
import re 
import math
import csv
# import Spreadsheet
import os
import  xml.etree.ElementTree as ET
import FreeCAD ,FreeCADGui
#========================================
#road properties
#========================================
class road_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#name property       
    @property
    def name(self):
        return self.ui.road_name.text()
    @name.setter
    def name(self,text):
        self.ui.road_name.setText(text)

#width 
    @property
    def width(self):
        return self.ui.road_width_sp.value()
    @width.setter
    def width(self,value):
        self.ui.road_width_sp.setValue(value)

#=================================================
#=================================================
#road
#==================================================
#=================================================
class road():
    def __init__(self,ui):
        self.ui=ui
        self.parent_path=['sdf','world']
        self.tag='road'
        self.file_name='road.sdf'
        self._road_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self._road_properties=road_properties(self.ui)
        #material element
        from . import material
        self.material_widget=FreeCADGui.PySideUic.loadUi(os.path.join(common.UI_PATH,"material.ui"))
        self._material=material.material(self.material_widget,self.parent_path+[self.tag])
        
        #disable unused material ui elements 
        self.material_widget.material_pbr_groupbox.setEnabled(False)
        self.material_widget.material_double_sided_checkBox.setEnabled(False)
        self.point_element=copy.deepcopy(self._road_element.find('.//point'))
        #disable the scroll widget
        
        self.ui.road_scroll.setWidget(self.material_widget.widget)
        self.ui.road_scroll.setEnabled(False)
        
        
        #configure the Ui and callbacks 
        self.configUI()
        self.reset(default=False)
        
    def configUI(self):
        self.ui.road_name.textEdited.connect(self.on_road_name)
        self.ui.road_width_sp.valueChanged.connect(self.on_road_width)
        self.ui.road_Reset_btn.clicked.connect(self.on_road_reset)
        self.ui.enable_road_checkbox.clicked.connect(self.on_road_checkbox)

    def on_road_checkbox(self):
        state=self.ui.enable_road_checkbox.isChecked()
        if state:
            self.ui.road_scroll.setEnabled(True)
        else:
            self.ui.road_scroll.setEnabled(False)
        
    def on_road_reset(self):
        self.reset(default=True)
        print('road resets applied\n')
        
    def on_road_name(self):
        common.set_xml_data(self._road_element,'road',True,{'name':self._road_properties.name})
        
    def on_road_width(self):
        common.set_xml_data(self._road_element,'width',False,self._road_properties.width)
        
    def get_sheet_data(self):
        #get  spread sheet  with points data
        sheet=FreeCAD.ActiveDocument.points
        data_cells=sheet.getNonEmptyCells()
        #ensure all point data is available since a vector 3 is required
        #all filled cells need to be a multiple of 3 
        if len(data_cells)%3 !=0:
            FreeCAD.Console.PrintUserWarning("some data is missing \n points not updated\n")
        else:
            #remove all points previously available in the tree
            for point in self._road_element.iter('point'):
                self._road_element.remove(point)
            #use list comprehension to extract  spreadsheet items 3 at a time
            #produces
            #start from 3 since the first 3 are the labels
            for row in [ [sheet.getContents(data_cells[i]),  sheet.getContents(data_cells[i+1]), sheet.getContents(data_cells[i+2])] 
                                            for i in range(3,len(data_cells),3)]:
                point=copy.deepcopy(self.point_element)
                point.text=' '.join(map(str,row))
                self._road_element.append(point)
    
            
    def updateUI(self):
        self._road_properties.name=common.get_xml_data(self._road_element,['road','name'],True)
        self._road_properties.width=common.get_xml_data(self._road_element,'width',False)
        
    
    def reset(self,default=True):
        if default:
            self._road_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
            self._material.reset(default=True)
            self._road_properties.point=None
        else:
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=common.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict is not None:
                elem=ET.fromstring(el_dict['elem_str'])
                self._road_element=elem
                #remove material from the element
                mat=self._road_element.find('.//material')
                #material is an optional element hence might not  be included 
                
                if mat is not None:
                    self._road_element.remove(mat)
                self._material.reset(default=False)
        
        #remove unused material elements 
        self._material._material_element.remove(self._material._material_element.find('.//pbr'))
        self._material._material_element.remove(self._material._material_element.find('.//double_sided'))
        
        self.updateUI() 
                
    @property
    def element(self):
        #update data in sheet before export 
        self.get_sheet_data()
        
        _elem=copy.deepcopy(self._road_element)
        #check if materialis enabled 
        if self.ui.include_material_info.isChecked():
            mat_el=self._material.element
            _elem.append(mat_el)
        return _elem
    
       
