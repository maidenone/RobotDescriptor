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
import FreeCAD
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

        
#==================================================
# road material 
#==================================================   
class material_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#script uri 
    @property 
    def script_uri(self):
        return self.ui.material_script_uri_input.text()
    @script_uri.setter
    def script_uri(self,text):
        self.ui.material_script_uri_input.setText(text)
        
#script name 
    @property
    def script_name(self):
        return self.ui.material_script_name.text()
    @script_name.setter
    def script_name(self,text):
        self.ui.material_script_name.setText(text)
        
#shader_type
    @property
    def shader_type(self):
        return self.ui.shader_type.currentText()
    @shader_type.setter
    def shader_type(self,text):
        self.ui.shader_type.setCurrentText(text)
#normal map
    @property
    def normal_map(self):
        return self.ui.material_normal_map_input.text()
    @normal_map.setter
    def normal_map(self,text):
        self.ui.material_normal_map_input.setText(text)

#this checkebox is not part of the sdf data its just used to enable and disable the normal_map input 
# so no need to convert bool to strinf 
    @property
    def normal_map_checkbox(self):
        return self.ui.normal_map_checkBox.isChecked()
        
    @normal_map_checkbox.setter
    def normal_map_checkbox(self,state):
        if state is True:
            self.ui.normal_map_checkBox.setState(QtCore.Qt.Checked)
        else:
            self.ui.normal_map_checkBox.setState(QtCore.Qt.Unchecked)
            
#render order
    @property
    def render_order(self):
        return self.ui.material_render_order_sp.value()
    @render_order.setter
    def render_order(self,value):
        self.ui.material_render_order_sp.setValue(value)

#shininess
    @property
    def shininess(self):
        return self.ui.materroad_pointsial_shininess_sp.value()
    @shininess.setter
    def shininess(self,value):
        self.ui.material_shininess_sp.setValue(value)
    
#lighting
    @property
    def lighting(self):
        state= self.ui.material_lighting_checkbox.isChecked()
        if state is True:
            return str('true')
        else:
            return str('false')
    @lighting.setter
    def lighting(self,state):
        if state is True:
            self.ui.material_lighting_checkbox.setState(QtCore.Qt.Checked)
        else:
            self.ui.material_lighting_checkbox.setState(QtCore.Qt.Unchecked)
            
    
#ambient 
    @property
    def ambient(self):
        return  [self.ui.material_ambient_R_sp.value(),self.ui.material_ambient_G_sp.value(),
                self.ui.material_ambient_B_sp.value(),self.ui.material_ambient_A_sp.value()]
    @ambient.setter
    def ambient(self,vals):
        self.ui.material_ambient_R_sp.setValue(vals[0])
        self.ui.material_ambient_G_sp.setValue(vals[1])
        self.ui.material_ambient_B_sp.setValue(vals[2])
        self.ui.material_ambient_A_sp.setValue(vals[3])
#diffuse
    @property
    def diffuse(self):
        return  [self.ui.material_diffuse_R_sp.value(),self.ui.material_diffuse_G_sp.value(),
                self.ui.material_diffuse_B_sp.value(),self.ui.material_diffuse_A_sp.value()]
    @diffuse.setter
    def diffuse(self,vals):
        self.ui.material_diffuse_R_sp.setValue(vals[0])
        self.ui.material_diffuse_G_sp.setValue(vals[1])
        self.ui.material_diffuse_B_sp.setValue(vals[2])
        self.ui.material_diffuse_A_sp.setValue(vals[3])
#specular
    @property
    def specular(self):
        return  [self.ui.material_specular_R_sp.value(),self.ui.material_specular_G_sp.value(),
                self.ui.material_specular_B_sp.value(),self.ui.material_specular_A_sp.value()]
    @specular.setter
    def specular(self,vals):
        self.ui.material_specular_R_sp.setValue(vals[0])
        self.ui.material_specular_G_sp.setValue(vals[1])
        self.ui.material_specular_B_sp.setValue(vals[2])
        self.ui.material_specular_A_sp.setValue(vals[3])
#emissive
    @property
    def emissive(self):
        return  [self.ui.material_emissive_R_sp.value(),self.ui.material_emissive_G_sp.value(),
                self.ui.material_emissive_B_sp.value(),self.ui.material_emissive_A_sp.value()]
    @emissive.setter
    def emissive(self,vals):
        self.ui.material_emissive_R_sp.setValue(vals[0])
        self.ui.material_emissive_G_sp.setValue(vals[1])
        self.ui.material_emissive_B_sp.setValue(vals[2])
        self.ui.material_emissive_A_sp.setValue(vals[3])

#===========================================
#===========================================
#material element 
#============================================
#============================================     
class material(common.color_pickr):
    def __init__(self,ui) -> None:
        super().__init__()
        self.ui=ui
        #use the road tag since material will be implemented  as part of the road element
        self.tag='road'
        self.parent_path=['sdf','world']
        self.file_name='material.sdf'

        self._material_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=material_properties(self.ui)
        #remove unused material elements 
        self._material_element.remove(self._material_element.find('.//pbr'))
        self._material_element.remove(self._material_element.find('.//double_sided'))
        self.configUI()
        self.reset(default=False)
        
    def configUI(self):
        self.ui.material_script_uri_input.textEdited.connect(self.on_uri)
        self.ui.material_script_name.textEdited.connect(self.on_uri_name)
        self.ui.shader_type.currentTextChanged.connect(self.on_shader_type)
        self.ui.normal_map_checkBox.stateChanged.connect(self.on_normal_map_state)
        self.ui.material_normal_map_input.textEdited.connect(self.on_normal_map)
        self.ui.material_render_order_sp.valueChanged.connect(self.on_material_render_ord)
        self.ui.material_shininess_sp.valueChanged.connect(self.on_shininess)
        
        #ambient
        self.ui.material_ambient_R_sp.valueChanged.connect(self.on_ambient)
        self.ui.material_ambient_G_sp.valueChanged.connect(self.on_ambient)
        self.ui.material_ambient_B_sp.valueChanged.connect(self.on_ambient)
        self.ui.material_ambient_A_sp.valueChanged.connect(self.on_ambient)
        #diffuse
        self.ui.material_diffuse_R_sp.valueChanged.connect(self.on_diffuse)
        self.ui.material_diffuse_G_sp.valueChanged.connect(self.on_diffuse)
        self.ui.material_diffuse_B_sp.valueChanged.connect(self.on_diffuse)
        self.ui.material_diffuse_A_sp.valueChanged.connect(self.on_diffuse)
        #specular
        self.ui.material_specular_R_sp.valueChanged.connect(self.on_specular)
        self.ui.material_specular_G_sp.valueChanged.connect(self.on_specular)
        self.ui.material_specular_B_sp.valueChanged.connect(self.on_specular)
        self.ui.material_specular_A_sp.valueChanged.connect(self.on_specular)
        #emissive
        self.ui.material_emissive_R_sp.valueChanged.connect(self.on_emissive)
        self.ui.material_emissive_G_sp.valueChanged.connect(self.on_emissive)
        self.ui.material_emissive_B_sp.valueChanged.connect(self.on_emissive)
        self.ui.material_emissive_A_sp.valueChanged.connect(self.on_emissive)
        
        #color picker buttons 
        self.ui.material_ambient_color_pkr.clicked.connect(self.on_ambient_color_pkr)
        self.ui.material_diffuse_color_pkr.clicked.connect(self.on_diffuse_color_pkr)
        self.ui.material_specular_color_pkr.clicked.connect(self.on_specular_color_pkr)
        self.ui.material_emissive_color_pkr.clicked.connect(self.on_emissive_color_pkr)
        
    
    def on_uri(self):
        common.set_xml_data(self._material_element,'uri',False,self.properties.script_uri)
        
    def on_uri_name(self):
        common.set_xml_data(self._material_element,'name',False,self.properties.script_name)
        
    def on_shader_type(self):
        common.set_xml_data(self._material_element,'shader',True,{'type':self.properties.shader_type})
        
#enable and disable normal map 
    def on_normal_map_state(self):
        if self.properties.normal_map_checkbox:
            self.ui.material_normal_map_input.setEnabled(True)
        else:
            self.ui.material_normal_map_input.setEnabled(False)
    
#normal map 
    def on_normal_map(self):
        common.set_xml_data(self._material_element,'normal_map',False,self.properties.normal_map)
        
#material render order  
    def on_material_render_ord(self):
        common.set_xml_data(self._material_element,'render_order',False,self.properties.render_order)
        
    def on_shininess(self):
        common.set_xml_data(self._material_element,'shininess',False,self.properties.shininess)
        
    def on_ambient(self):
        common.set_xml_data(self._material_element,'ambient',False,self.properties.ambient)
        self.set_widget_color('ambient',self.ui.material_ambient_color_pkr)
        
    def on_diffuse(self):
        common.set_xml_data(self._material_element,'diffuse',False,self.properties.diffuse)
        self.set_widget_color('diffuse',self.ui.material_diffuse_color_pkr)
    
    def on_specular(self):
        common.set_xml_data(self._material_element,'specular',False,self.properties.specular)
        self.set_widget_color('specular',self.ui.material_specular_color_pkr)
        
    def on_emissive(self):
        common.set_xml_data(self._material_element,'emissive',False,self.properties.emissive)
        self.set_widget_color('emissive',self.ui.material_emissive_color_pkr)
    
    def on_ambient_color_pkr(self):
        self.color_picker('ambient',self.ui.material_ambient_color_pkr)
    
    def on_diffuse_color_pkr(self):
        self.color_picker('diffuse',self.ui.material_diffuse_color_pkr)
    
    def on_specular_color_pkr(self):
        self.color_picker('specular',self.ui.material_specular_color_pkr)
        
    def on_emissive_color_pkr(self):
        self.color_picker('emissive',self.ui.material_emissive_color_pkr)
    
    def updateUi(self):
        self.properties.script_uri=common.get_xml_data(self._material_element,'uri',False)
        self.properties.script_name=common.get_xml_data(self._material_element,'name',False)
        self.properties.shader_type=common.get_xml_data(self._material_element,'type')
        self.properties.normal_map=common.get_xml_data(self._material_element,'normal_map',False)
        self.properties.render_order=common.get_xml_data(self._material_element,'render_order',False)
        self.properties.shininess=common.get_xml_data(self._material_element,'shininess',False)
        self.properties.ambient=common.get_xml_data(self._material_element,'ambient',False)
        self.properties.diffuse=common.get_xml_data(self._material_element,'diffuse',False)
        self.properties.specular=common.get_xml_data(self._material_element,'specular',False)
        self.properties.emissive=common.get_xml_data(self._material_element,'emissive',False)
        #style sheets 
        self.set_widget_color('ambient',self.ui.material_ambient_color_pkr)
        self.set_widget_color('diffuse',self.ui.material_diffuse_color_pkr)
        self.set_widget_color('specular',self.ui.material_specular_color_pkr)
        self.set_widget_color('emissive',self.ui.material_emissive_color_pkr)
        
    def reset(self,default=True):
        if default:
            self._material_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
            #remove unused elements 
            self._material_element.remove(self._material_element.find('.//pbr'))
            self._material_element.remove(self._material_element.find('.//double_sided'))
        else:
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=common.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict is not None:
                #find the material element from road 
                elem=ET.fromstring(el_dict['elem_str']).find('.//material')
                #make check since material might not always be included in the final element tree
                # since its optional 
                if elem is not None:
                    self.merge_elements(self._material_element,elem)
        self.updateUi()
    
             
#merger 
#this merge method repeats alot 
    def merge_elements(self,destination_el, source_el):
        common.merge_elements(destination_el,source_el)
    
    @property
    def element(self):
        #make deep copy to avoid altering local element 
        temp_el=copy.deepcopy(self._material_element)
        #script 
        if self.ui.material_script_groupBox.isChecked():
            #if script is checked remove al other color properties 
            tags=['shader','ambient','diffuse','specular','emissive','shininess','render_order'
                  ,'lighting']
            for elem_tag in tags:
                temp_el.remove(temp_el.find('.//'+elem_tag))
        else:
            temp_el.remove(temp_el.find('.//script'))
        #shader 
            if self.ui.material_shader_groupBox.isChecked():
            #if shader is checked check if the normal map is checked and remve it if neccessary
                if self.properties.normal_map_checkbox is False:
                    shader_el=temp_el.find('.//shader')
                    shader_el.remove(shader_el.find('.//normal_map'))
                    
            else:
                temp_el.remove(temp_el.find('.//shader'))
            
            #remove color related configs 
            if self.ui.material_ambient_groupbox.isChecked() is False:
                temp_el.remove(temp_el.find('.//ambient'))
        
            if self.ui.material_diffuse_groupbox.isChecked() is False:
                temp_el.remove(temp_el.find('.//diffuse'))
        
            if self.ui.material_specular_groupbox.isChecked() is False:
                temp_el.remove(temp_el.find('.//specular'))
        
            if self.ui.material_emissive_groupbox.isChecked() is False:
                temp_el.remove(temp_el.find('.//emissive'))
        
        return temp_el
        
        
                
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
        self._material=material(self.ui)
        self.point_element=copy.deepcopy(self._road_element.find('.//point'))
        #disable the scroll widget
        self.ui.road_scroll.setEnabled(False)
        

    #remove elements that will not be edited 
        
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
                    self._road_element.remove(mat )
        self.updateUI() 
                
    @property
    def element(self):
        #update data in sheet before export 
        self.get_sheet_data()
        
        
        _elem=copy.deepcopy(self._road_element)
        #check if materialis enabled 
        if self.ui.road_material_groupbox.isChecked():
            mat_el=self._material.element
            _elem.append(mat_el)
        return _elem
    
       
