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

#matreial 
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
        return self.ui.material_shininess_sp.value()
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
        if state =='true':
            self.ui.material_lighting_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.material_lighting_checkbox.setCheckState(QtCore.Qt.Unchecked)
            
    
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
        
#pbr 
#=================================================
    @property
    def double_sided(self):
        return str('true') if self.ui.material_double_sided_checkBox.isChecked() else str('false')
    
    @double_sided.setter
    def double_sided(self,state):
        self.ui.material_double_sided_checkBox.setCheckState(QtCore.Qt.Checked) if state else self.ui.material_double_sided_checkBox.setCheckState(QtCore.Qt.Unchecked)

#metal_albedo_map
    @property
    def metal_albedo_map(self):
        return self.ui.metal_albedo_map_lineEdit.text()
    @metal_albedo_map.setter
    def metal_albedo_map(self,text):
        self.ui.metal_albedo_map_lineEdit.setText(text)
        
#metal_roughness_map
    @property
    def metal_roughness_map(self):
        return self.ui.metal_roughness_map_lineEdit.text()
    @metal_roughness_map.setter
    def metal_roughness_map(self,text):
        self.ui.metal_roughness_map_lineEdit.setText(text)
        
#metal_roughness
    @property
    def metal_roughness(self):
        return self.ui.metal_roughness_lineEdit.text()
    @metal_roughness.setter
    def metal_roughness(self,text):
        self.ui.metal_roughness_lineEdit.setText(text)
        
#metalness_map
    @property
    def metalness_map(self):
        return self.ui.metalness_map_lineEdit.text()
    @metalness_map.setter
    def metalness_map(self,text):
        self.ui.metalness_map_lineEdit.setText(text)
        
#metalness
    @property
    def metalness(self):
        return self.ui.metalness_sp.value()
    @metalness.setter
    def metalness(self,val):
       
        self.ui.metalness_sp.setValue(val)
        
#metal_environment_map
    @property
    def metal_environment_map(self):
        return self.ui.metal_environment_map_lineEdit.text()
    @metal_environment_map.setter
    def metal_environment_map(self,text):
        self.ui.metal_environment_map_lineEdit.setText(text)
        
#metal_ambient_occlusion_map
    @property
    def metal_ambient_occlusion_map(self):
        return self.ui.metal_ambient_occlusion_map_lineEdit.text()
    @metal_ambient_occlusion_map.setter
    def metal_ambient_occlusion_map(self,text):
        self.ui.metal_ambient_occlusion_map_lineEdit.setText(text)
        
#metal_emissive_map
    @property
    def metal_emissive_map(self):
        return self.ui.metal_emissive_map_lineEdit.text()
    @metal_emissive_map.setter
    def metal_emissive_map(self,text):
        self.ui.metal_emissive_map_lineEdit.setText(text)
        
#metal_light_map
    @property
    def metal_light_map(self):
        return self.ui.metal_light_map_lineEdit.text()
    @metal_light_map.setter
    def metal_light_map(self,text):
        self.ui.metal_light_map_lineEdit.setText(text)
        
#metal_uv_set
    @property
    def metal_uv_set(self):
        def metal_uv_set(self):
            return self.ui.metal_uv_set_sp.value()
    @metal_uv_set.setter
    def metal_uv_set(self,value):
        self.ui.metal_uv_set_sp.setValue(value)
        
#metal_normal_map
    @property
    def metal_normal_map(self):
        return self.ui.metal_normal_map_lineEdit.text()
    @metal_normal_map.setter
    def metal_normal_map(self,text):
        self.ui.metal_normal_map_lineEdit.setText(text)
        
#metal_normal_map_type
    @property
    def metal_normal_map_type(self):
        return self.ui.metal_normal_map_type_comboBox.currentText()
    
    @metal_normal_map_type.setter
    def metal_normal_map_type(self,text):
        self.ui.metal_normal_map_type_comboBox.setCurrentText(text)

#==========
#specular 

#specular_albedo_map
    @property
    def specular_albedo_map(self):
        return self.ui.specular_albedo_map_lineEdit.text()
    @specular_albedo_map.setter
    def specular_albedo_map(self,text):
        self.ui.specular_albedo_map_lineEdit.setText(text)
        
#specular_map
    @property
    def specular_map(self):
        self.ui.specular_map_lineEdit.text()
    @specular_map.setter
    def specular_map(self,text):
        self.ui.specular_map_lineEdit.setText(text)
        
#specular_glossiness
    @property
    def specular_glossiness(self):
        return self.ui.specular_glossiness_sp.value()
    @specular_glossiness.setter
    def specular_glossiness(self,val):
        self.ui.specular_glossiness_sp.setValue(val)
        
#specular_environment_map
    @property
    def specular_environment_map(self):
        return self.ui.specular_environment_map_lineEdit.text()
    @specular_environment_map.setter
    def specular_environment_map(self,text):
        self.ui.specular_environment_map_lineEdit.setText(text)
        
#specular_ambient_occlusion_map
    @property
    def specular_ambient_occlusion_map(self):
        return self.ui.specular_ambient_occlusion_map_lineEdit.text()
    @specular_ambient_occlusion_map.setter
    def specular_ambient_occlusion_map(self,text):
        self.ui.specular_ambient_occlusion_map_lineEdit.setText(text)
    
#specular_emissive_map
    @property
    def specular_emissive_map(self):
        return self.ui.specular_emissive_map_lineEdit.text()
    @specular_emissive_map.setter
    def specular_emissive_map(self,text):
        self.ui.specular_emissive_map_lineEdit.setText(text)
    
#specular_glossiness_map
    @property
    def specular_glossiness_map(self):
        return self.ui.specular_glossiness_map_lineEdit.text()
    @specular_glossiness_map.setter
    def specular_glossiness_map(self,text):
        self.ui.specular_glossiness_map_lineEdit.setText(text)
        
#specular_light_map
    @property
    def specular_light_map(self):
        return self.ui.specular_light_map_lineEdit.text()
    @specular_light_map.setter
    def specular_light_map(self,text):
        self.ui.specular_light_map_lineEdit.setText(text)
        
#specular_uv_set
    @property
    def specular_uv_set(self):
        return self.ui.specular_uv_set_sp.value()
    @specular_uv_set.setter
    def specular_uv_set(self,val):
        self.ui.specular_uv_set_sp.setValue(val)
        
#specular_normal_map
    @property
    def specular_normal_map(self):
        return self.ui.specular_normal_map_lineEdit.text()
    @specular_normal_map.setter
    def specular_normal_map(self,text):
        self.ui.specular_normal_map_lineEdit.setText(text)

#specular_normal_map_type
    @property
    def specular_normal_map_type(self):
        return self.ui.specular_normal_map_type_comboBox.currentText()
    @specular_normal_map_type.setter
    def specular_normal_map_type(self,text):
        self.ui.specular_normal_map_type_comboBox.setCurrentText(text)
        
#Read only attributes 
#used  for optional properties 
#pbr 
    #metal
    @property
    def metal_albedo_map_cb(self):
        return self.ui.metal_albedo_map_checkBox.isChecked()
    
    @property
    def metal_roughness_map_cb(self):
        return self.ui.metal_roughness_map_checkBox.isChecked()
    
    @property
    def metal_roughness_cb(self):
        return self.ui.metal_roughness_checkBox.isChecked()
    @property
    def metalness_map_cb(self):
        return self.ui.metalness_map_checkBox.isChecked()
    
    @property
    def metalness_cb(self):
        return self.ui.metalness_checkBox.isChecked()
    @property
    def metal_environment_map_cb(self):
        return self.ui.metal_environment_map_checkBox.isChecked()
    @property
    def metal_ambient_occlusion_map_cb(self):
        return self.ui.metal_ambient_occlusion_map_checkBox.isChecked()
    
    @property
    def metal_emissive_map_cb(self):
        return self.ui.metal_emissive_map_checkBox.isChecked()
    @property
    def metal_normal_map_cb(self):
        return self.ui.metal_normal_map_groupBox.isChecked()
    
    @property
    def metal_light_map_cb(self):
        return self.ui.metal_light_map_groupBox.isChecked()
    
    #specular
    @property
    def specular_albedo_map_cb(self):
        return self.ui.specular_albedo_map_checkBox.isChecked()
    @property
    def specular_map_cb(self):
        return self.ui.specular_map_checkBox.isChecked()
    @property
    def specular_glossiness_cb(self):
        return self.ui.specular_glossiness_checkBox.isChecked()
    @property
    def specular_environment_map_cb(self):
        return self.ui.specular_environment_map_checkBox.isChecked()
    @property
    def specular_ambient_occlusion_map_cb(self):
        return self.ui.specular_ambient_occlusion_map_checkBox.isChecked()
    @property
    def specular_emissive_map_cb(self):
        return self.ui.specular_emissive_map_checkBox.isChecked()
    @property
    def specular_glossiness_map_cb(self):
        return  self.ui.specular_glossiness_map_checkBox.isChecked()
    @property
    def specular_light_map_cb(self):
        return self.ui.specular_light_map_groupBox.isChecked()
    @property
    def specular_normal_map_cb(self):
        return self.ui.specular_normal_map_groupBox.isChecked()
    
    #pbr cb
    @property
    def pbr_enabled(self):
        return self.ui.material_pbr_groupbox.isChecked()
    #metal cb 
    @property
    def metal_enabled(self):
        return self.ui.material_metal_groupbox.isChecked()
    #speculat cb 
    @property
    def specular_enabled(self):
        return self.ui.pbr_specular_groupBox.isChecked()
    
    
    
#===========================================
#===========================================
#material element 
#============================================
#============================================     
class material(common.color_pickr):
    #since material has multiple parents let the parent class 
    # the  parent and parent path data 
    def __init__(self,ui) -> None:
        super().__init__()
        self.ui=ui
        #use the road tag since material will be implemented  as part of the road element
        self.tag='road'
        self.parent_path=''
        self.file_name='material.sdf'

        self._material_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=material_properties(self.ui)
        self.configUI()
        # self.reset(default=False)
        
    def configUI(self):
        self.ui.material_script_uri_input.textEdited.connect(self.on_uri)
        self.ui.material_script_name.textEdited.connect(self.on_uri_name)
        self.ui.shader_type.currentTextChanged.connect(self.on_shader_type)
        self.ui.material_normal_map_input.textEdited.connect(self.on_normal_map)
        self.ui.material_render_order_sp.valueChanged.connect(self.on_material_render_ord)
        self.ui.material_shininess_sp.valueChanged.connect(self.on_shininess)
        
        self.ui.material_lighting_checkbox.stateChanged.connect(
            lambda : common.set_xml_data(self._material_element,"lighting",False,self.properties.lighting)
        )
        
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
        
        
#pbr
    #metal 
    #properties under the metal element 
        self.ui.metal_albedo_map_lineEdit.textEdited.connect(self.on_metal_albedo_map)
        
        self.ui.metal_roughness_map_lineEdit.textEdited.connect(self.on_metal_roughness_map)
        self.ui.metal_roughness_lineEdit.textEdited.connect(self.on_metal_roughness)
        
        self.ui.metalness_map_lineEdit.textEdited.connect(self.on_metalness_map)
        
        self.ui.metalness_sp.valueChanged.connect(self.on_metalness)
        
        self.ui.metal_environment_map_lineEdit.textEdited.connect(self.on_metal_environment_map)
        
        self.ui.metal_ambient_occlusion_map_lineEdit.textEdited.connect(self.on_metal_ambient_occlusion_map)
        
        self.ui.metal_emissive_map_lineEdit.textEdited.connect(self.on_metal_emissive_map)
        
        self.ui.metal_light_map_lineEdit.textEdited.connect(self.on_metal_light_map)
        
        self.ui.metal_uv_set_sp.valueChanged.connect(self.on_metal_uv_set)
        
        self.ui.metal_normal_map_lineEdit.textEdited.connect(self.on_metal_normal_map)
        self.ui.metal_normal_map_type_comboBox.currentTextChanged.connect(self.on_metal_normal_map_type)
        
    #specular
    #elements under the specular subelement
        specular=self._material_element.find(".//pbr/specular")
        self.ui.specular_albedo_map_lineEdit.textEdited.connect(self.on_specular_albdedo_map)
        
        self.ui.specular_map_lineEdit.textEdited.connect(self.on_specular_map)
        
        self.ui.specular_glossiness_sp.valueChanged.connect(self.on_specular_glossiness)
        
        self.ui.specular_environment_map_lineEdit.textEdited.connect(self.on_specular_environment_map)
        self.ui.specular_ambient_occlusion_map_lineEdit.textEdited.connect(self.on_specular_ambient_occlusion_map)
        self.ui.specular_emissive_map_lineEdit.textEdited.connect(self.on_specular_emissive_map)
        self.ui.specular_glossiness_map_lineEdit.textEdited.connect(self.on_specular_glossiness_map)
        self.ui.specular_light_map_lineEdit.textEdited.connect(self.on_specular_light_map)
        
        self.ui.specular_uv_set_sp.valueChanged.connect(self.on_specular_uv_set)
        
        self.ui.specular_normal_map_lineEdit.textEdited.connect(self.on_specular_normal_map
        )
        self.ui.specular_normal_map_type_comboBox.currentTextChanged.connect(self.on_specular_normal_map_type
        )
       
#callbacks 
    #metal 
    def on_metal_albedo_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,'albedo_map',False,self.properties.metal_albedo_map)
        
    def on_metal_roughness_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,'roughness_map',False,self.properties.metal_roughness_map)
        
    def on_metal_roughness(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"roughness",False,self.properties.metal_roughness)
        
    
    def on_metalness_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"metalness_map",False,self.properties.metalness_map)
        
    def on_metalness(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"metalness",False,self.properties.metalness)
        
    def on_metal_environment_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"environment_map",False,self.properties.metal_environment_map)
        
    def on_metal_ambient_occlusion_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"ambient_occlusion_map",False,self.properties.metal_ambient_occlusion_map)
        
    def on_metal_emissive_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"emissive_map",False,self.properties.metal_emissive_map)
    
    def on_metal_light_map(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"light_map",False,self.properties.metal_light_map)
        
    def on_metal_uv_set(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"light_map",True,{"uv_set":self.properties.metal_uv_set})
    
    
    def on_metal_normal_map(self):
        metal=self._material_element.find(' common.set_xml_data(specular,"albedo_map",False,self.properties.specular_albedo_map).//pbr/metal')
        common.set_xml_data(metal,"normal_map",False,self.properties.metal_normal_map)
    
    
    def on_metal_normal_map_type(self):
        metal=self._material_element.find('.//pbr/metal')
        common.set_xml_data(metal,"normal_map",True,{"type":self.properties.metal_normal_map_type})
        
    #specular
    
    def on_specular_albdedo_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"albedo_map",False,self.properties.specular_albedo_map)
    
    def on_specular_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"specular_map",False,self.properties.specular_map)
        
    def on_specular_glossiness(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"glossiness",False,self.properties.specular_glossiness)
        
        
    def on_specular_environment_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"environment_map",False,self.properties.specular_environment_map)
        
    def on_specular_ambient_occlusion_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"ambient_occlusion_map",False,self.properties.specular_ambient_occlusion_map)
        
    def on_specular_emissive_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"emissive_map",False,self.properties.specular_emissive_map)
          
    def on_specular_glossiness_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"glossiness_map",False,self.properties.specular_glossiness_map)
        
    def on_specular_light_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"light_map",False,self.properties.specular_light_map)

    def on_specular_uv_set(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"light_map",True,{"uv_set":self.properties.specular_uv_set})
    
    def on_specular_normal_map(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"normal_map",False,self.properties.specular_normal_map)
    
    def on_specular_normal_map_type(self):
        specular=self._material_element.find(".//pbr/specular")
        common.set_xml_data(specular,"normal_map",True,{"type":self.properties.specular_normal_map_type})
    

    def on_uri(self):
        common.set_xml_data(self._material_element,'uri',False,self.properties.script_uri)
        
    def on_uri_name(self):
        common.set_xml_data(self._material_element,'name',False,self.properties.script_name)
        
    def on_shader_type(self):
        common.set_xml_data(self._material_element,'shader',True,{'type':self.properties.shader_type})
        
    
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
        self.properties.lighting=common.get_xml_data(self._material_element,"lighting",False)
        #pbr 
            #metal
        metal=self._material_element.find('.//pbr/metal')
        # { tag : property }
        #properties is the property name defined in  the properties class 
        items={'albedo_map':"metal_albedo_map",'roughness_map':"metal_roughness_map","metalness_map":"metalness_map","metalness":"metalness",
               "environment_map":"metal_environment_map","ambient_occlusion_map":"metal_ambient_occlusion_map","emissive_map":"metal_emissive_map",
               "light_map":"metal_light_map","normal_map":"metal_normal_map"}
        #set the data for all items 
        for tag in items.keys():
            setattr(self.properties,items[tag],common.get_xml_data(metal,tag,False))
        #set  element attributes 
        self.properties.metal_uv_set=common.get_xml_data(metal,["light_map","uv_set"],True)
        self.properties.metal_normal_map_type=common.get_xml_data(metal,["normal_map","type"],True)
            #specular 
        specular=self._material_element.find(".//pbr/specular")
        #{tag : attribute}
        specular_items={"albedo_map":"specular_albedo_map","specular_map":"specular_map","glossiness":"specular_glossiness","environment_map":"specular_environment_map",
                       "ambient_occlusion_map": "specular_ambient_occlusion_map","emissive_map":"specular_emissive_map","glossiness_map":"specular_glossiness_map",
                       "light_map":"specular_light_map","normal_map":"specular_normal_map"}
        for tag  in specular_items:
            setattr(self.properties,specular_items[tag],common.get_xml_data(specular,tag,False))
     
        self.properties.specular_uv_set=common.get_xml_data(specular,["light_map","uv_set"],True)
        self.properties.specular_normal_map_type=common.get_xml_data(specular,["normal_map","type"],True)
            
        #style sheets 
        self.set_widget_color('ambient',self.ui.material_ambient_color_pkr)
        self.set_widget_color('diffuse',self.ui.material_diffuse_color_pkr)
        self.set_widget_color('specular',self.ui.material_specular_color_pkr)
        self.set_widget_color('emissive',self.ui.material_emissive_color_pkr)
  
    def reset(self,default=True):
        pass
    
             
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
            
            #logic for materials related to pbr 
            pbr=temp_el.find('pbr')
            if self.properties.pbr_enabled and pbr is not None:
                metal=temp_el.find('.//pbr/metal')
                if self.properties.metal_enabled and metal is not None:
                    #{tag : property}
                    #where propertty are the propertieswhose names end with  with _cb 
                    metal_opt_elems={'albedo_map':"metal_albedo_map_cb",'roughness_map':"metal_roughness_map_cb","metalness_map":"metalness_map_cb"
                             ,"metalness":"metalness_cb",
                        "environment_map":"metal_environment_map_cb","ambient_occlusion_map":"metal_ambient_occlusion_map_cb","emissive_map":"metal_emissive_map_cb",
                        "light_map":"metal_light_map_cb","normal_map":"metal_normal_map_cb"}
                    for tag in metal_opt_elems.keys():
                        if getattr(self.properties,metal_opt_elems[tag]) is not True:
                            metal.remove(metal.find('.//'+tag))
                else:
                    if metal is not None:
                       temp_el.find('.//pbr').remove(metal)
                #related to specular 
                specular=temp_el.find(".//pbr/specular")
                if self.properties.specular_enabled and specular is not None:
                    #{tag : property}
                    #where propertty are the properties whose names end with with _cb 
                    specular_opts={"albedo_map":"specular_albedo_map_cb","specular_map":"specular_map_cb","glossiness":"specular_glossiness_cb",
                                   "environment_map":"specular_environment_map_cb",
                       "ambient_occlusion_map": "specular_ambient_occlusion_map_cb","emissive_map":"specular_emissive_map_cb",
                       "glossiness_map":"specular_glossiness_map_cb",
                       "light_map":"specular_light_map_cb","normal_map":"specular_normal_map_cb"}
                    for tag in specular_opts.keys():
                        if getattr(self.properties,specular_opts[tag]) is not True:
                            specular.remove(specular.find('.//'+tag))
                else:
                    if specular is not None:
                        temp_el.find('.//pbr').remove(specular)
            else:
                if pbr is not None:
                    temp_el.remove(pbr)
        
        return temp_el