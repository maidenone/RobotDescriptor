from .. import RD_globals
import xml.etree.ElementTree as ET
from ..RD_parser import initialize_element_tree
import copy
import FreeCAD


#==========================================================
#spherical coordinate properties 
#===========================================================
class spherical_coordinates_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#all optional properties
#surface model       
    @property
    def surface_model(self):
        return self.ui.surface_model_cb.currentText()
    #optional property ,check for none
    @surface_model.setter
    def surface_model(self,text:str):
        if text!=None:
            self.ui.surface_model_cb.setCurrentText(text)
        else:
            pass
#world frame properties       
    @property
    def world_frame_orientation(self):
        return self.ui.world_frame_orientation_cb.currentText()
    #optional property, check for none
    @world_frame_orientation.setter
    def world_frame_orientation(self,text):
        if text!=None:
            self.ui.world_frame_orientation_cb.setCurrentText(text)
        else:
            pass
#latitude_deg
    @property
    def latitude_deg(self):
        return self.ui.latitude_deg_sp.value()
    #optional property, check for none
    @latitude_deg.setter
    def latitude_deg(self,value):
        if value!=None:
            self.ui.latitude_deg_sp.setValue(value)
        else:
            pass
#longitude_deg
    @property
    def longitude_deg(self):
        return self.ui.longitude_deg_sp.value()
    #optional property , check for none
    @longitude_deg.setter
    def longitude_deg(self,value):
        if value!=None:
            self.ui.longitude_deg_sp.setValue(value)
        else:
            pass

#elevation
    @property
    def elevation(self):
        return self.ui.elevation_sp.value()
    #optional property ,check for none
    @elevation.setter
    def elevation(self,value):
        if value!=None:
            self.ui.elevation_sp.setValue(value)
        else:
            pass
        
#surface_axis_equatorial
    @property
    def surface_axis_equatorial(self):
        return self.ui.surface_axis_equatorial_sp.value()
    #optional property ,check for none
    @surface_axis_equatorial.setter
    def surface_axis_equatorial(self,value):
        if value!=None:
            self.ui.surface_axis_equatorial_sp.setValue(value)
        else:
            pass
#surface_axis_polar
    @property
    def surface_axis_polar(self):
        return self.ui.surface_axis_polar_sp.value()
    #optional property , check for none
    @surface_axis_polar.setter
    def surface_axis_polar(self,value):
        if value!=None:
            self.ui.surface_axis_polar_sp.setValue(value)   
#heading_deg
    @property
    def heading_deg(self):
        return self.ui.heading_deg_sp.value()
    #optional property , check for none
    @heading_deg.setter
    def heading_deg(self,value):
        if value!=None:
            self.ui.heading_deg_sp.setValue(value)
        
#=========================================================
#spherical coordinates 
#==========================================================
class spherical_coordinates:
    def __init__(self,ui) -> None:
        self.ui=ui
        
        self.parent_path=['sdf','world']
        self.tag_name='spherical_coordinates'
        self.file_name='spherical_coordinates.sdf'
        self._spherical_coord_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        
        self.properties=spherical_coordinates_properties(self.ui)
        self.configUI()

        self.reset(default=False)
    
    def configUI(self):
        self.ui.surface_model_cb.currentIndexChanged.connect(self.on_surface_model)
        self.ui.world_frame_orientation_cb.currentIndexChanged.connect(self.on_world_frame)
        self.ui.latitude_deg_sp.valueChanged.connect(self.on_latitude_deg)
        self.ui.longitude_deg_sp.valueChanged.connect(self.on_longitude)
        self.ui.elevation_sp.valueChanged.connect(self.on_elevation)
        self.ui.surface_axis_equatorial_sp.valueChanged.connect(self.on_s_a_eq)
        self.ui.surface_axis_polar_sp.valueChanged.connect(self.on_s_a_p)
        self.ui.heading_deg_sp.valueChanged.connect(self.on_heading)
        self.ui.spherical_coord_rst_btn.clicked.connect(self.on_reset)
        
    
#callbacks 
    def on_reset(self):
        self.reset(default=True)
        print("spherical resets applied \n")

    def on_surface_model(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"surface_model",False,self.properties.surface_model)
    
    def on_world_frame(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"world_frame_orientation",False,self.properties.world_frame_orientation)
        
    def on_latitude_deg(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"latitude_deg",False,self.properties.latitude_deg)
        
    def on_longitude(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"longitude_deg",False,self.properties.longitude_deg)
        
    def on_elevation(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"elevation",False,self.properties.elevation)
    
    def on_s_a_eq(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"surface_axis_equatorial",False,self.properties.surface_axis_equatorial)
        
    def on_s_a_p(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"surface_axis_polar",False,self.properties.surface_axis_polar)
        
    def on_heading(self):
        RD_globals.set_xml_data(self._spherical_coord_elem,"heading_deg",False,self.properties.heading_deg)
#end callbacks 
  
    def update_ui(self):
        if self.ui.spherical_coordinates_groupbox.isChecked():
            self.properties.surface_model=RD_globals.get_xml_data(self._spherical_coord_elem,"surface_model",False)
            self.properties.world_frame_orientation=RD_globals.get_xml_data(self._spherical_coord_elem,"world_frame_orientation",False)
            self.properties.latitude_deg=float(RD_globals.get_xml_data(self._spherical_coord_elem,"latitude_deg",False))
            self.properties.longitude_deg=float(RD_globals.get_xml_data(self._spherical_coord_elem,"longitude_deg",False))
            self.properties.elevation=float(RD_globals.get_xml_data(self._spherical_coord_elem,"elevation",False))
            self.properties.surface_axis_equatorial=float(RD_globals.get_xml_data(self._spherical_coord_elem,"surface_axis_equatorial",False))
            self.properties.surface_axis_polar=float(RD_globals.get_xml_data(self._spherical_coord_elem,"surface_axis_polar",False))
            self.properties.heading_deg=float(RD_globals.get_xml_data(self._spherical_coord_elem,"heading_deg",False))
        else:
            pass
    
    def reset(self,default:bool=True):
        if default:
            self._spherical_coord_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element   
        else:
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=RD_globals.parse_dict(_root_dict,self.parent_path+[self.tag_name])
            if el_dict!=None:
                el_str=el_dict['elem_str']
                RD_globals.merge_elements(self._spherical_coord_elem,ET.fromstring(el_str))
            else:
                pass
               
        self.update_ui()
         
     
    @property
    def spherical_cood_elem(self):
        el=copy.deepcopy(self._spherical_coord_elem)
        if self.ui.surface_axis_equatorial_groupBox.isChecked():
            el.remove(el.iter("surface_axis_equatorial").__next__())
        if self.ui.surface_axis_polar_groupBox.isChecked():
            el.remove(el.iter("surface_axis_polar").__next__())
            
        return el
    