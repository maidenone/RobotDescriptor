import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore

import xml.etree.ElementTree as ET
from  .. import RD_globals 
#reponsible for creating an element tree using xml.etree
from ..RD_parser import  initialize_element_tree

_icon_dir__=os.path.join(RD_globals.ICON_PATH,"world_properties.svg")




# this  class will provide be the interface to the ui 
class world_properties():
    def __init__(self,loaded_ui):
        self.form=loaded_ui
#initialize the atmosphere class 
        
    #world name poperty , this will be used to get and set the wold property name 
    @property
    def name(self):
        return  self.form.world_name_input.text()
    @name.setter
    def name(self,new_world_name:str):
        self.form.world_name_input.setText(new_world_name) 
    
    #gravity property 
    @property 
    def gravity(self)->list:
        return [self.form.gravity_x.value(),self.form.gravity_y.value(),self.form.gravity_z.value()]
    
    @gravity.setter
    def gravity(self,gravity_vect:list):
        self.form.gravity_x.setValue(gravity_vect[0])
        self.form.gravity_y.setValue(gravity_vect[1])
        self.form.gravity_z.setValue(gravity_vect[2])
        return True
    
    #magnetic field property
    @property
    def magnetic_field(self):
        #return the vector if the group has been enabled
        '''returns None if group is disabled'''
        if self.form.magnetic_field_group.isChecked():
            self.form.magn_x.value()
            self.form.magn_y.value()
            self.form.magn_z.value()
        else:
        # return none if the group is not enabled
            return None
    
    @magnetic_field.setter
    def magnetic_field(self,magn_vec:list):
            self.form.magn_x.setValue(magn_vec[0])
            self.form.magn_y.setValue(magn_vec[1])
            self.form.magn_z.setValue(magn_vec[2])
    
    #audio property
    @property
    def audio(self)->str:
        "returns none if group is disabled"
        if self.form.audio_group.isChecked():
            return self.form.device_string_input.text()
        else:
            return None
    @audio.setter
    def audio(self,device_str:str)->bool:
        self.form.device_string_input.setText(device_str)
    
    #wind property 
    @property
    def wind(self):
        '''returns none if property is disabled'''
        if self.form.wind_property.isChecked():
            return [self.form.wind_x.text(),self.form.wind_y.text(),self.form.wind_z.text()]
        else:
            return None
    @wind.setter
    def wind(self,wind_vec:list)->bool:
        self.form.wind_x.setValue(wind_vec[0])
        self.form.wind_y.setValue(wind_vec[1])
        self.form.wind_z.setValue(wind_vec[2])
        
    #to implement an atmosphere class 
                
    
class world(QtGui.QWidget):
    def __init__(self):
        super(world,self).__init__()

        self.parent_path=["sdf"]
        self.tag='world'
        self.file_name="world.sdf"
# a variable to track if a widget is already open to prevent multiple widgets
        self.widget_active=False
# get world element 
        self.world_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        # print(initialize_element_tree.ET.tostring(self.world_elem,encoding="unicode"))
        
        self.ui_path=os.path.join(RD_globals.UI_PATH,"world_properties.ui")
        self.world_form=FreeCADGui.PySideUic.loadUi(self.ui_path,self)
        self.world_form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # create the properties 
        self.properties=world_properties(self.world_form)
        self.properties.magnetic_field=[5.5645e-6 ,22.8758e-6 ,-42.3884e-6]
        self.update_ui()
        # initialize atmosphere properties 
        from . import atmosphere
        self.atmosphere=atmosphere.atmosphere(self.world_form)
#call initUI  method
        self.configUI()
    def update_ui(self):
        self.properties.name=RD_globals.get_xml_data(self.world_elem,["world","name"],True)
        self.properties.gravity=RD_globals.get_xml_data(self.world_elem,"gravity",False)
        self.properties.wind=RD_globals.get_xml_data(self.world_elem,"linear_velocity",False)
        self.properties.audio=RD_globals.get_xml_data(self.world_elem,"device",False)
        self.properties.magnetic_field=RD_globals.get_xml_data(self.world_elem,"magnetic_field",False)
#this will be called by the reset callback 
    def reset(self):
        self.world_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.update_ui()
       
    def configUI(self):
        if self.widget_active==False:
            self.widget_active=True
            self.world_form.world_name_input.textEdited.connect(self.on_world_name)
        # all gravity inputs should call the same callback 
            self.world_form.gravity_x.valueChanged.connect(self.on_gravity)
            self.world_form.gravity_y.valueChanged.connect(self.on_gravity)
            self.world_form.gravity_z.valueChanged.connect(self.on_gravity)
        #magnetic field
            self.world_form.magn_x.valueChanged.connect(self.on_magn)
            self.world_form.magn_y.valueChanged.connect(self.on_magn)
            self.world_form.magn_z.valueChanged.connect(self.on_magn)
        # wind
            self.world_form.wind_x.valueChanged.connect(self.on_wind)
            self.world_form.wind_y.valueChanged.connect(self.on_wind)
            self.world_form.wind_z.valueChanged.connect(self.on_wind)
        
        #audio 
            self.world_form.device_string_input.textEdited.connect(self.on_audio)
            self.world_form.ok_pb.clicked.connect(self.on_ok)
        
            
        #apply pushbutton
            self.world_form.apply_pb.clicked.connect(self.on_apply_pb)
        
            self.world_form.setGeometry(400,250,610,709)
        #display window
            self.world_form.show()
        else:
            pass
                 
    def update_element(self):
#make a temporary copy to prevent altering the original element 
        temp_el=self.world_elem
        if not self.world_form.magnetic_field_group.isChecked():
            el=temp_el.iter("magnetic_field").__next__()
            temp_el.remove(el)
        if not self.world_form.audio_group.isChecked():
            el=temp_el.iter("audio").__next__()
            temp_el.remove(el)
        if not self.world_form.wind_group.isChecked():
            el=temp_el.iter("wind").__next__()
            temp_el.remove(el)
        return temp_el
#callbacks 

    def closeEvent(self,event):
        self.widget_active=False
        event.accept()
        
    def on_world_name(self):
        name=self.properties.name
        RD_globals.set_xml_data(self.world_elem,"world",True,{"name":name})  
    def on_gravity(self):
        RD_globals.set_xml_data(self.world_elem,"gravity",False,self.properties.gravity)
    def on_magn(self):
        RD_globals.set_xml_data(self.world_elem,"magnetic_field",False,self.properties.magnetic_field)
    def on_wind(self):
        RD_globals.set_xml_data(self.world_elem,"linear_velocity",False,self.properties.wind)
    def on_audio(self):
        RD_globals.set_xml_data(self.world_elem,"device",False,self.properties.audio)
    def on_ok(self):
        self.widget_active=False
        self.world_form.close()
        
    def on_apply_pb(self):
        #read string element data from RD_description proxy 
        if RD_globals.DEBUG==True:
            import pdb
            pdb.set_trace()
        updated_elem=self.update_element()
        if RD_globals.update_dictionary(self.parent_path,self.tag,updated_elem)==None:
            FreeCAD.Console.PrintWarning("initialize work bench")
#append elements in hierachy as they are supposed to appear in the tree e.g world is appended 
#before atmosphere since its atmospheres parent, this helps reduce the complexity 
#of having to implement a way of  ensuring parents are available 

# dont  add atmosphere element if the group box is not checked
        if self.atmosphere.is_checked():
            RD_globals.update_dictionary(self.atmosphere.parent_path,self.atmosphere.tag,self.atmosphere.atmosphere_element)
#end callbacks
#initialize  class      
class init_sdf_world:
  
    def GetResources(self):
        return {"Pixmap"  :_icon_dir__, # the name of a svg file available in the resources
                "Accel"   : "Shift+w", # a default shortcut (optional)
                "MenuText": "sdf world stuff",
                "ToolTip" : "edit world properties"}

    def Activated(self):
        """Do something here"""
        self.w=world()
        # w.world_form.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand("world_properties", init_sdf_world())

