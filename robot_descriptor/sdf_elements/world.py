import FreeCAD
import FreeCADGui
import os 
from PySide import QtGui,QtCore
import copy

import xml.etree.ElementTree as ET
from  .. import common 
#reponsible for creating an element tree using xml.etree
from ..RD_utils import  initialize_element_tree

_icon_dir__=os.path.join(common.ICON_PATH,"world_properties.svg")


'''setters will do nothing for optional part '''
#------------------------------------------------------------
#world properties 
#-------------------------------------------------------------
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
        
    
    #magnetic field property
    @property
    def magnetic_field(self):
        #return the vector if the group has been enabled
        '''returns None if group is disabled'''
        x=self.form.magn_x.value()
        y=self.form.magn_y.value()
        z=self.form.magn_z.value()
        return [x,y,z]
        
# check optional properties for none  
  
    @magnetic_field.setter
    def magnetic_field(self,magn_vec:list):
        if magn_vec is not None:
            self.form.magn_x.setValue(magn_vec[0])
            self.form.magn_y.setValue(magn_vec[1])
            self.form.magn_z.setValue(magn_vec[2])
        else:
            pass
    
    #optional audio property
    #check for None
    @property
    def audio(self)->str:
        if self.form.audio_group.isChecked():
            return self.form.device_string_input.text()
        else:
            return None
    @audio.setter
    def audio(self,device_str:str)->bool:
        if str!=None:
            self.form.device_string_input.setText(device_str)
        else:
            pass
    
    #optional wind property 
    #check for none
    @property
    def wind(self):
        '''returns none if property is disabled'''
        if self.form.wind_group.isChecked():
            return [self.form.wind_x.text(),self.form.wind_y.text(),self.form.wind_z.text()]
        else:
            return None
    @wind.setter
    def wind(self,wind_vec:list)->bool:
        if wind_vec!=None:
            self.form.wind_x.setValue(wind_vec[0])
            self.form.wind_y.setValue(wind_vec[1])
            self.form.wind_z.setValue(wind_vec[2])
        else:
            pass
        
    #to implement an atmosphere cincase lass 
                
#------------------------------------------------------
#world 
#------------------------------------------------------ 
class world():
    def __init__(self):
        
        self.parent_path=["sdf"]
        self.tag='world'
        self.file_name="world.sdf"
        self.ui_path=os.path.join(common.UI_PATH,"world.ui")
        self.world_form=FreeCADGui.PySideUic.loadUi(self.ui_path)
        #get main window for  use in aligning 
        mw=FreeCADGui.getMainWindow()
        #centre dialog to main window 
        self.world_form.move(
            mw.frameGeometry().topLeft() + mw.rect().center() - self.world_form.rect().center()
        )
        self.properties=world_properties(self.world_form)
# get world element 
        self.world_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
#initialize atmosphere properties 
        from . import atmosphere
        self.atmosphere=atmosphere.atmosphere(self.world_form)
#initialize physics 
        from . import physics
        self._physics=physics.physics(self.world_form)
#initialize spherical coordinates
        from . import spherical_coordinates
        self._spherical_coordinates=spherical_coordinates.spherical_coordinates(self.world_form)
#initialize light
        from . import light
        self._lights=light.light(self.world_form)
        
#initialize scene 
        from . import scene
        self._scene=scene.scene(self.world_form)
        
#initialize road
        from . import road
        self._road=road.road(self.world_form)

        self.configUI()
#update ui with previously configured values if available     
       
        self.reset(False)
        #display window
        self.world_form.exec_()
#window close event  this is called when the (x) widget icon is pressed 
    def closeEvent(self, event):
        print('closing widget\n')
        event.accept()

    def update_ui(self):
        self.properties.name=common.get_xml_data(self.world_elem,["world","name"],True)
        self.properties.gravity=common.get_xml_data(self.world_elem,"gravity",False)
        self.properties.wind=common.get_xml_data(self.world_elem,"linear_velocity",False)
        self.properties.audio=common.get_xml_data(self.world_elem,"device",False)
        self.properties.magnetic_field=common.get_xml_data(self.world_elem,"magnetic_field",False)
        
#this will be called by the reset callback 
    def reset(self,default:bool=True):

        if default:
            self.world_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
#reset all elements ?
            self.atmosphere.reset(default=True)
        else:
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=common.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict is not None:
                el_str=el_dict['elem_str']
                self.merge(el_str)
            else:
                pass
            self.atmosphere.reset(False)

        self.update_ui()

    def merge(self, el_str):
        common.merge_elements(self.world_elem,ET.fromstring(el_str))
       
    def configUI(self):
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
 # reset Pb
        self.world_form.world_reset_btn.clicked.connect(self.on_reset)
        
        
        
 
    def update_element(self):
#make a temporary copy to prevent altering the original element 
        temp_el=copy.deepcopy(self.world_elem)
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
#reset pushbutton
    def on_reset(self):
        self.reset()
        print("world resets applied")
 
        
    def on_world_name(self):
        name=self.properties.name
        common.set_xml_data(self.world_elem,"world",True,{"name":name})  
    def on_gravity(self):
        common.set_xml_data(self.world_elem,"gravity",False,self.properties.gravity)
    def on_magn(self):
        common.set_xml_data(self.world_elem,"magnetic_field",False,self.properties.magnetic_field)
    def on_wind(self):
        common.set_xml_data(self.world_elem,"linear_velocity",False,self.properties.wind)
    def on_audio(self):
        common.set_xml_data(self.world_elem,"device",False,self.properties.audio)

#ok push button pressed callback 
    def on_ok(self):
        self.world_form.close()

#apply pb
    def on_apply_pb(self):
        #read string element data from RD_description proxy 
        updated_elem=self.update_element()
        common.update_dictionary(self.parent_path,self.tag,updated_elem)
            
#append elements in hierachy as they are supposed to appear in the tree e.g world is appended 
#before atmosphere since its atmospheres parent, this helpsFreeCADGui.PySideUic.loadUi(self.ui_path,self) reduce the complexity 
#of having to implement a way of  ensuring parents are available 
# dont  add atmosphere element if the group box is not checked
        if self.atmosphere.is_checked():
            common.update_dictionary(self.atmosphere.parent_path,self.atmosphere.tag,self.atmosphere.atmosphere_element)
        
#add physics properties
        common.update_dictionary(self._physics.parent_path,self._physics.tag,self._physics.element)
#add spherical coordiates     
        if self.world_form.spherical_coordinates_groupbox.isChecked():
            common.update_dictionary(
                                         self._spherical_coordinates.parent_path,
                                         self._spherical_coordinates.tag_name,
                                         self._spherical_coordinates.spherical_cood_elem)

#dont attempt to add a lights if there are no light sources    
        if len(self._lights.lights) >0:
            common.update_dictionary(self._lights.parent_path,self._lights.tag,self._lights.element)
#add scene based on state of a checkbox 
        if  self.world_form.enable_scene_checkBox.isChecked():
            common.update_dictionary(self._scene.parent_path,self._scene.tag,self._scene.element)
#append the  road element 
        if self.world_form.include_material_info.isChecked():
            common.update_dictionary(self._road.parent_path,self._road.tag,self._road.element)
            
        print("updated\n")
    

#==========================================================
#=========================================================
#=========================================================  
class init_sdf_world:
  
    def GetResources(self):
        return {"Pixmap"  :_icon_dir__, # the name of a svg file available in the resources
                "Accel"   : "Shift+w", # a default shortcut (optional)
                "MenuText": "sdf world stuff",
                "ToolTip" : "edit world properties"}

    def Activated(self):
        """intiialize workbench"""

        
        if FreeCAD.activeDocument() is None:
            return
            # import pdb
            # pdb.set_trace()
        if hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
            #todo
            #prevent opening duplicate windows
            self.w=world()
        
        else:
            FreeCAD.Console.PrintError("workbench not initialized\n")
            return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""

        if hasattr(FreeCAD.ActiveDocument, "Robot_Description"):
            return True
        else:
            return False


FreeCADGui.addCommand("world_properties", init_sdf_world())
