from .. import RD_globals
import copy 
import xml.etree.ElementTree as ET
import FreeCAD
from ..RD_parser import initialize_element_tree
from PySide import QtCore
from PySide.QtGui import QColorDialog
import math
#===================================
#scene properties
#======================================
#=====================================
class scene_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#ambient    
    @property
    def scene_ambient(self):
        return [self.ui.scene_ambient_R_sp.value(),self.ui.scene_ambient_G_sp.value()
                ,self.ui.scene_ambient_B_sp.value(),self.ui.scene_ambient_A_sp.value()]
    @scene_ambient.setter
    def scene_ambient(self,vals):
        self.ui.scene_ambient_R_sp.setValue(vals[0])
        self.ui.scene_ambient_G_sp.setValue(vals[1])
        self.ui.scene_ambient_B_sp.setValue(vals[2])
        self.ui.scene_ambient_A_sp.setValue(vals[3])
    
#background
    @property 
    def background(self):
        return [self.ui.scene_background_R_sp.value(),self.ui.scene_background_G_sp.value(),
                self.ui.scene_background_B_sp.value(),self.ui.scene_background_A_sp.value()]
    @background.setter
    def background(self,vals):
        self.ui.scene_background_R_sp.setValue(vals[0])
        self.ui.scene_background_G_sp.setValue(vals[1])
        self.ui.scene_background_B_sp.setValue(vals[2])
        self.ui.scene_background_A_sp.setValue(vals[3])
        
#time
    @property
    def time(self):
        return self.ui.sky_time_sp.value()
    @time.setter
    def time(self,value):
        self.ui.sky_time_sp.setValue(value)
        
#sunrise
    @property
    def sunrise(self):
        return self.ui.sky_sunrise_sp.value()
    @sunrise.setter
    def sunrise(self,value):
        self.ui.sky_sunrise_sp.setValue(value)
        
#sunset
    @property
    def sunset(self):
        return self.ui.sky_sunset_sp.value()
    @sunset.setter
    def sunset(self,value):
        self.ui.sky_sunset_sp.setValue(value)
        
#clouds speed
    @property
    def speed(self):
        return  self.ui.clouds_speed_sp.value()
    @speed.setter
    def speed(self,value):
        self.ui.clouds_speed_sp.setValue(value)
        
#clouds direction
    @property
    def direction(self):
        return self.ui.clouds_direction_sp.value()
    @direction.setter
    def direction(self,value):
        self.ui.clouds_direction_sp.setValue(value)
        
#clouds humidity
    @property
    def humidity(self):
        return  self.ui.clouds_humidity_sp.value()
    @humidity.setter
    def humidity(self,value):
        self.ui.clouds_humidity_sp.setValue(value)
    
#clouds mean_size
    @property
    def mean_size(self):
        return self.ui.cloud_mean_size_sp.value()
    @mean_size.setter
    def mean_size(self,value):
        self.ui.cloud_mean_size_sp.setValue(value)
        
#clouds ambient
    @property
    def clouds_ambient(self):
        return [self.ui.cloud_ambient_R_sp.value(),self.ui.cloud_ambient_G_sp.value(),
                self.ui.cloud_ambient_B_sp.value(),self.ui.cloud_ambient_A_sp.value()]
        
    @clouds_ambient.setter
    def clouds_ambient(self,vals):
        self.ui.cloud_ambient_R_sp.setValue(vals[0])
        self.ui.cloud_ambient_G_sp.setValue(vals[1])
        self.ui.cloud_ambient_B_sp.setValue(vals[2])
        self.ui.cloud_ambient_A_sp.setValue(vals[3])
        
#cubemap_uri
    @property
    def cubemap_uri(self):
        txt=self.ui.cubemap_uri_lineEdit.text()
        if txt is None:
            txt=''
        return txt
    @cubemap_uri.setter
    def cubemap_uri(self,text):
        self.ui.cubemap_uri_lineEdit.setText(text)
#shadows
    @property
    def shadows(self):
        state=self.ui.shadows_checkBox.isChecked()
        if state:
            return str("true")
        else:
            return str("false")
    @shadows.setter
    def shadows(self,state):
        if state =='true':
            self.ui.shadows_checkBox.setCheckState(QtCore.Qt.Checked)
        elif state=='false':
            self.ui.shadows_checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            print("unsupported state\n")
            
#grid
    @property
    def grid(self):
        state=self.ui.grid_checkbox.isChecked()
        if state:
            return str("true")
        else:
            return str("false")
    @grid.setter
    def grid(self,state):
        if state=='true':
            self.ui.grid_checkbox.setCheckState(QtCore.Qt.Checked)
        elif state=='false':
            self.ui.grid_checkbox.setCheckState(QtCore.Qt.Unchecked)
        else:
            print("unsupported state\n")

#origin_visual
    @property
    def origin_visual(self):
        state= self.ui.origin_visual_checkBox.isChecked()
        if state:
            return str("true")
        else:
            return str("false")
    @origin_visual.setter
    def origin_visual(self,state):
        if state =='true':
            self.ui.origin_visual_checkBox.setCheckState(QtCore.Qt.Checked)
        elif state=='false':
            self.ui.origin_visual_checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            print("unsupported state \n")
        
#fog color
    @property
    def fog_color(self):
        return  [self.ui.fog_color_R_sp.value(),self.ui.fog_color_G_sp.value(),
                self.ui.fog_color_B_sp.value(),self.ui.fog_color_A_sp.value()]
    @fog_color.setter
    def fog_color(self,vals):
        self.ui.fog_color_R_sp.setValue(vals[0])
        self.ui.fog_color_G_sp.setValue(vals[1])
        self.ui.fog_color_B_sp.setValue(vals[2])
        self.ui.fog_color_A_sp.setValue(vals[3])

#fog type
    @property
    def fog_type(self):
        return self.ui.fog_type_cb.currentText()
    @fog_type.setter
    def fog_type(self,type):
        self.ui.fog_type_cb.setCurrentText(type)
    
#fog start
    @property
    def fog_start(self):
        return self.ui.fog_start_sp.value()
    @fog_start.setter
    def fog_start(self,value):
        self.ui.fog_start_sp.setValue(value)
        
#fog end
    @property
    def fog_end(self):
        return self.ui.fog_end_sp.value()
    @fog_end.setter
    def fog_end(self,value):
        self.ui.fog_end_sp.setValue(value)
    
#fog density
    @property
    def fog_density(self):
        return self.ui.fog_density_sp.value()
    @fog_density.setter
    def fog_density(self,value):
        self.ui.fog_density_sp.setValue(value)

#============================================
#===============================================
#scene 
#==============================================
#===============================================
   
class scene:
    def __init__(self,ui):
        self.ui=ui
        self.parent_path=['sdf','world']
        self.tag="scene"
        self.file_name="scene.sdf"
        self._scene_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=scene_properties(self.ui)
        
        self.reset(default=False)
        #check if scene is enabled
        self.on_scene()
        self.configUI()
        
    def configUI(self):
#scene ambient callback 
        self.ui.scene_ambient_R_sp.valueChanged.connect(self.on_scene_ambient)
        self.ui.scene_ambient_G_sp.valueChanged.connect(self.on_scene_ambient)
        self.ui.scene_ambient_B_sp.valueChanged.connect(self.on_scene_ambient)
        self.ui.scene_ambient_A_sp.valueChanged.connect(self.on_scene_ambient)
#scene background 
        self.ui.scene_background_R_sp.valueChanged.connect(self.on_background)
        self.ui.scene_background_G_sp.valueChanged.connect(self.on_background)
        self.ui.scene_background_B_sp.valueChanged.connect(self.on_background)
        self.ui.scene_background_A_sp.valueChanged.connect(self.on_background)
        
#time 
        self.ui.sky_time_sp.valueChanged.connect(self.on_time)
#sunrise 
        self.ui.sky_sunrise_sp.valueChanged.connect(self.on_sunrise)
#sunset 
        self.ui.sky_sunset_sp.valueChanged.connect(self.on_sunset)
#speed 
        self.ui.clouds_speed_sp.valueChanged.connect(self.on_speed)
#direction 
        self.ui.clouds_direction_sp.valueChanged.connect(self.on_direction)
#hunidity 
        self.ui.clouds_humidity_sp.valueChanged.connect(self.on_humidity)
##cloud ambient 
        self.ui.cloud_ambient_R_sp.valueChanged.connect(self.on_cloud_ambient)
        self.ui.cloud_ambient_G_sp.valueChanged.connect(self.on_cloud_ambient)
        self.ui.cloud_ambient_B_sp.valueChanged.connect(self.on_cloud_ambient)
        self.ui.cloud_ambient_A_sp.valueChanged.connect(self.on_cloud_ambient)
#mean_size
        self.ui.cloud_mean_size_sp.valueChanged.connect(self.on_mean_size)
#cubemap uri 
        self.ui.cubemap_uri_lineEdit.textEdited.connect(self.on_cube_map)
#shadows
        self.ui.shadows_checkBox.stateChanged.connect(self.on_shadow)
#grid 
        self.ui.grid_checkbox.stateChanged.connect(self.on_grid)
#origin visual 
        self.ui.origin_visual_checkBox.stateChanged.connect(self.on_origin_visual)
#fog color 
        self.ui.fog_color_R_sp.valueChanged.connect(self.on_fog_color)
        self.ui.fog_color_G_sp.valueChanged.connect(self.on_fog_color)
        self.ui.fog_color_B_sp.valueChanged.connect(self.on_fog_color)
        self.ui.fog_color_A_sp.valueChanged.connect(self.on_fog_color)
#fog type 
        self.ui.fog_type_cb.currentTextChanged.connect(self.on_fog_type)
#fog start
        self.ui.fog_start_sp.valueChanged.connect(self.on_fog_start)
#fog end
        self.ui.fog_end_sp.valueChanged.connect(self.on_fog_end)
#fog density 
        self.ui.fog_density_sp.valueChanged.connect(self.on_fog_density)
#reset
        self.ui.Reset_pb.clicked.connect(self.on_reset)
#scene checkbox 
        self.ui.enable_scene_checkBox.stateChanged.connect(self.on_scene)
        
#color picker callback
        self.ui.fog_color_picker_btn.clicked.connect(self.on_fog_color_picker)
        self.ui.cloud_ambient_color_pkr.clicked.connect(self.on_cloud_ambient_color_pkr)
        self.ui.scene_background_color_pkr.clicked.connect(self.on_scene_background_color_pkr)
        self.ui.scene_ambient_color_pkr.clicked.connect(self.on_scene_ambient_color_pkr)

    def color_picker(self,prop,widget):
        '''
        prop: property string e.g 'fog color'
        widget: the widget to edit its style sheet
                e.g self.ui.fog color picker

        '''
        col_dialog = QColorDialog(self.ui)
        col=col_dialog.getColor()
        if col.isValid():
            color=[col.redF(),col.blueF(),col.greenF(),col.alphaF()]
            setattr(self.properties,prop,color)
            widget.setStyleSheet(f" background-color: {col.name()}; ")
        
#callbacks 
#start
#start of  color picker methods 
    def on_fog_color_picker(self):
        self.color_picker('fog_color',self.ui.fog_color_picker_btn)
    def on_cloud_ambient_color_pkr(self):
        self.color_picker('clouds_ambient',self.ui.cloud_ambient_color_pkr)
    def on_scene_background_color_pkr(self):
        self.color_picker('background',self.ui.scene_background_color_pkr)
    def on_scene_ambient_color_pkr(self):
        self.color_picker('scene_ambient',self.ui.scene_ambient_color_pkr)
    
        
    def on_scene(self):
        state=self.ui.enable_scene_checkBox.isChecked()
        if state:
            self.ui.scene_scroll.setEnabled(True)
        else:
            self.ui.scene_scroll.setEnabled(False)
    
    def on_reset(self):
        self.reset()
        print("scene resets applied")
        
    def on_scene_ambient(self):
        #since multiple ambient tags exist within scene
        #ensure the  correct element is being updated
        ambient=self._scene_element.find("ambient")
        vect=self.properties.scene_ambient
        ambient.text=' '.join(map(str,vect))
    
    def on_background(self):
        RD_globals.set_xml_data(self._scene_element,"background",False,self.properties.background)
        
    def on_time(self):
        RD_globals.set_xml_data(self._scene_element,"time",False,self.properties.time)
    
    def on_sunrise(self):
        RD_globals.set_xml_data(self._scene_element,"sunrise",False,self.properties.sunrise)
        
    def on_sunset(self):
        RD_globals.set_xml_data(self._scene_element,"sunset",False,self.properties.sunset)
        
    def on_speed(self):
        RD_globals.set_xml_data(self._scene_element,"speed",False,self.properties.speed)
        
    def on_direction(self):
        RD_globals.set_xml_data(self._scene_element,"direction",False,self.properties.direction)
    
    def on_humidity(self):
        RD_globals.set_xml_data(self._scene_element,"humidity",False,self.properties.humidity)
    
    def on_cloud_ambient(self):
        #write to the ambient in clouds element 
        RD_globals.set_xml_data(self._scene_element.find("sky"),"ambient",False,self.properties.clouds_ambient)
    
    def on_mean_size(self):
        RD_globals.set_xml_data(self._scene_element,"mean_size",False,self.properties.mean_size)
    
    def on_cube_map(self):
        RD_globals.set_xml_data(self._scene_element,"cubemap_uri",False,self.properties.cubemap_uri)
        
    def on_shadow(self):
        RD_globals.set_xml_data(self._scene_element,"shadows",False,self.properties.shadows)
        
    def on_grid(self):
        RD_globals.set_xml_data(self._scene_element,"grid",False,self.properties.grid)
        
    def on_origin_visual(self):
        RD_globals.set_xml_data(self._scene_element,"origin_visual",False,self.properties.origin_visual)
        
    def on_fog_color(self):
        RD_globals.set_xml_data(self._scene_element,"color",False,self.properties.fog_color)
        
    def on_fog_type(self):
        RD_globals.set_xml_data(self._scene_element,"type",False,self.properties.fog_type)
    
    def on_fog_start(self):
        RD_globals.set_xml_data(self._scene_element,"start",False,self.properties.fog_start)
        
    def on_fog_end(self):
        RD_globals.set_xml_data(self._scene_element,"end",False,self.properties.fog_end)
        
    def on_fog_density(self):
        
        RD_globals.set_xml_data(self._scene_element,"density",False,self.properties.fog_density)
#callbacks
#end


    def update_ui(self):
        self.properties.scene_ambient=RD_globals.extract_vector_n(self._scene_element.find("ambient").text)
        
        self.properties.background=RD_globals.get_xml_data(self._scene_element,"background",False)

        self.properties.time=float(RD_globals.get_xml_data(self._scene_element,"time",False))
        self.properties.sunrise=float(RD_globals.get_xml_data(self._scene_element,"sunrise",False))
        self.properties.sunset=float(RD_globals.get_xml_data(self._scene_element,"sunset",False))
        self.properties.speed=float(RD_globals.get_xml_data(self._scene_element,"speed",False))
        self.properties.direction=float(RD_globals.get_xml_data(self._scene_element,"direction",False))
        self.properties.humidity=float(RD_globals.get_xml_data(self._scene_element,"humidity",False))
        
        self.properties.clouds_ambient=RD_globals.get_xml_data(self._scene_element.find("sky"),"ambient",False)
        self.properties.mean_size=RD_globals.get_xml_data(self._scene_element,"mean_size",False)
     
        self.properties.cubemap_uri=RD_globals.get_xml_data(self._scene_element,"cubemap_uri",False)
        self.properties.shadows=RD_globals.get_xml_data(self._scene_element,"shadows",False)
        self.properties.grid=RD_globals.get_xml_data(self._scene_element,"grid",False)
        self.properties.origin_visual=RD_globals.get_xml_data(self._scene_element,"origin_visual",False)
        self.properties.fog_color=RD_globals.get_xml_data(self._scene_element,"color",False)
        self.properties.fog_type=RD_globals.get_xml_data(self._scene_element,"type",False)
        self.properties.fog_start=RD_globals.get_xml_data(self._scene_element,"start",False)
        self.properties.fog_end=RD_globals.get_xml_data(self._scene_element,"end",False)
        self.properties.fog_density=RD_globals.get_xml_data(self._scene_element,"density",False)
        
        #update color  of the  color picker buttons 
        color_list=[['fog_color',self.ui.fog_color_picker_btn],['clouds_ambient',self.ui.cloud_ambient_color_pkr],
                    ['background',self.ui.scene_background_color_pkr],['scene_ambient',self.ui.scene_ambient_color_pkr]]
        for val in color_list:
            self.set_widget_color(val[0],val[1])

#used to set color properties of color picker buttons 
    def set_widget_color(self,prop:str,widget):
        color_str=','.join([str(math.ceil(i*255)) for i in getattr(self.properties,prop)])
        widget.setStyleSheet(f"background-color: rgba({color_str});")
        
    def reset(self,default:bool=True):
        if default:
            self._scene_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
            self.update_ui()
         
        else:
            
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=RD_globals.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict is not None:
                el_str=el_dict["elem_str"]
                self.merge_elements(self._scene_element,ET.fromstring(el_str))
        self.update_ui()
                
    def merge_elements(self,destination_el, source_el):
    # Update attributes of destination_el with source_el
        destination_el.attrib.update(source_el.attrib)
        if source_el.text:
            destination_el.text = source_el.text
    # Merge child elements recursively
        for child in source_el:
            existing_el = destination_el.find(child.tag)
            if existing_el is not None:
                self.merge_elements(existing_el, child)  # Recursively merge the existing element with the new one
            else:
            # If the element doesn't exist in destination, simply append it
                # destination_el.append(child)
                pass
            
    @property
    def element(self):
        elem=copy.deepcopy(self._scene_element)
        #remove sky if checkbos is not checked 
        if not self.ui.sky_groupBox.isChecked():
            elem.remove(elem.find(".//sky"))
        else:
            #if sky is checked remove child elements based on their
            #check state 
            #find the sky element 
            sky=elem.find('.//sky')
            if not self.ui.scene_clouds_groupbox.isChecked():
                sky.remove(sky.find(".//clouds"))
            if self.properties.cubemap_uri =='':
                 #remove cubemap uri if it does not contain any data
                sky.remove(elem.find(".//cubemap_uri"))
        #remove fog if it's not checked 
        if not self.ui.fog_groupBox.isChecked():
            elem.remove(elem.find(".//fog"))
       
        return elem
            