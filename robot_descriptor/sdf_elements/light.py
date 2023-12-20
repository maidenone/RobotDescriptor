import xml.etree.ElementTree as ET
from PySide import QtCore
from PySide.QtGui import  QMessageBox
import FreeCAD
from ..RD_parser import initialize_element_tree
from .. import RD_globals
import copy
import re
#=============================================================
#light properties
#=============================================================
class light_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#name     
    @property
    def name(self):
        return self.ui.light_name.text()
    @name.setter
    def name(self,text):
        self.ui.light_name.setText(text)
    
#type 
    @property
    def type(self):
        return self.ui.light_type.currentText()
    @type.setter
    def type(self,text:str):
        self.ui.light_type.setCurrentText(text)
        
#intensity 
    @property
    def intensity(self):
        return self.ui.intensity_sp.value()

    @intensity.setter
    def intensity(self,value):
        self.ui.intensity_sp.setValue(value)

#light on 
    @property
    def light_on(self):
        state= self.ui.light_on_check_b.isChecked()
        if state:
            return str('true')
        else:
            return  str('false')
    @light_on.setter
    def light_on(self,state:bool):
        if state:
            self.ui.light_on_check_b.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.light_on_check_b.setCheckState(QtCore.Qt.Unchecked)
#visualize
    @property
    def visualize(self):
        state=self.ui.visualize_checkBox.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
    @visualize.setter
    def visualize(self,state:bool):
        if state is True:
            self.ui.visualize_checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.visualize_checkBox.setCheckState(QtCore.Qt.Unchecked)
            
#cast shadows 
    @property
    def cast_shadows(self):
        state=self.ui.cast_shadows_check_b.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
    @cast_shadows.setter
    def cast_shadows(self,state:bool):
        if state:
            self.ui.cast_shadows_check_b.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.cast_shadows_check_b.setCheckState(QtCore.Qt.Unchecked)
#diffuse
    @property
    def diffuse(self):
        return [self.ui.diffuse_R.value(),self.ui.diffuse_G.value(),self.ui.diffuse_B.value(), self.ui.diffuse_A.value()]
    @diffuse.setter
    def diffuse(self,vals:list):
        self.ui.diffuse_R.setValue(vals[0])
        self.ui.diffuse_G.setValue(vals[1])
        self.ui.diffuse_B.setValue(vals[2])
        self.ui.diffuse_A.setValue(vals[3])
    
#specular
    @property
    def specular(self):
        return [self.ui.specular_R.value(),self.ui.specular_G.value(),self.ui.specular_B.value(),self.ui.specular_A.value()]
    @specular.setter
    def specular(self,vals:list):
        self.ui.specular_R.setValue(vals[0])
        self.ui.specular_G.setValue(vals[1])
        self.ui.specular_B.setValue(vals[2])
        self.ui.specular_A.setValue(vals[3])
        
#range
    @property
    def range(self):
        return self.ui.range_sp.value()
    @range.setter
    def range(self,value):
        self.ui.range_sp.setValue(value)

#constant 
    @property
    def constant(self):
        return self.ui.constant_sp.value()
    @constant.setter
    def constant(self,value):
        self.ui.constant_sp.setValue(value)
    
#linear 
    @property
    def linear(self):
        return self.ui.linear_sp.value()
    @linear.setter
    def linear(self,value):
        self.ui.linear_sp.setValue(value)

#quadratic 
    @property
    def quadratic(self):
        return self.ui.quadratic_sp.value()
    @quadratic.setter
    def quadratic(self,value):
        self.ui.quadratic_sp.setValue(value)

#direction 
    @property
    def direction(self):
        return [self.ui.direction_x.value(),self.ui.direction_y.value(),self.ui.direction_z.value()]
    @direction.setter
    def direction(self,vals:list):
        self.ui.direction_x.setValue(vals[0])
        self.ui.direction_y.setValue(vals[1])
        self.ui.direction_z.setValue(vals[2])
#inner angle 
    @property
    def inner_angle(self):
        return self.ui.inner_angle_sp.value()
    @inner_angle.setter
    def inner_angle(self,value):
        self.ui.inner_angle_sp.setValue(value)
        
#fall_off
    @property
    def falloff(self):
        return self.ui.falloff_sp.value()
    @falloff.setter
    def falloff(self,value):
        self.ui.falloff_sp.setValue(value)

#outer_angle
    @property
    def outer_angle(self):
        return self.ui.outer_angle_sp.value()
    @outer_angle.setter
    def outer_angle(self,value):
        self.ui.outer_angle_sp.setValue(value)

     #pose 
    @property 
    def pose(self):
        xyz=[self.ui.pose_x_sp.value(),self.ui.pose_y_sp.value(),self.ui.pose_z_sp.value()]
        rpy=[self.ui.pose_roll_sp.value(),self.ui.pose_pitch_sp.value(),self.ui.pose_yaw_sp.value()]
        return xyz+rpy
    @pose.setter
    def pose(self,vals:list):
        self.ui.pose_x_sp.setValue(vals[0])
        self.ui.pose_y_sp.setValue(vals[1])
        self.ui.pose_z_sp.setValue(vals[2])
        self.ui.pose_roll_sp.setValue(vals[3])
        self.ui.pose_pitch_sp.setValue(vals[4])
        self.ui.pose_yaw_sp.setValue(vals[5])

#=================================================================
#light
#=================================================================
   
class light:
    def __init__(self,ui) -> None:
        self.ui=ui
        self.file_name='light.sdf'
        self.parent_path=['sdf','world']
        self.tag='light'
        self.initialize()
    #create variable to element that is currently selected 
        self._current_light_element=None
        self.properties=light_properties(self.ui)
    #this variable will store of all available lights in a dictionary 
        self.add_sun()
        self.reset(default=False)
    #configure the ui 
        self.configUI()
        

#initialize 
    def initialize(self):
        self._light_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.pose=initialize_element_tree.convdict_2_tree('pose.sdf').get_element
        #remove pose attributes that will not be edited
        del self.pose.attrib["relative_to"]
        del self.pose.attrib["rotation_format"]
        del self.pose.attrib["degrees"]
        # append pose to  light 
        self._light_element.append(self.pose)
        self.lights={}
      #the lights dictionary format
      #
      
#     {
#         key:light tag name
#         value:light element
#       }
      

#add a default light source 
    def add_sun(self):
        sun=copy.deepcopy(self._light_element)
        sun.attrib['type']='directional'
        sun.attrib['name']='sun'
        sun_properties={'direction':[-0.5,0.5,1],'pose':[0,0,10,0,0,0],'cast_shadows':'true','diffuse':[0.8,0.8,0.8,1],'specular':[0.1,0.1,0.1,1],
         "range":1000,'constant':0.9,'linear':0.01,'quadratic':0.001}
        
        for key in sun_properties.keys():
            RD_globals.set_xml_data(sun,key,False,sun_properties[key])
#append to sun 

        self.lights['sun']=copy.deepcopy(sun)
        #add item to list 
        self.ui.light_listWidget.addItem('sun')
        #select the item 
        item=self.ui.light_listWidget.item(0)
        item.setSelected(True)
        self.ui.light_listWidget.setCurrentItem(item)
#set the current light element 
        self._current_light_element=sun
        #disable spot groupbox
        self.ui.spot_groupbox.setEnabled(False)
        #disable directional groupbox
        self.ui.direction_groupbox.setEnabled(True)

#configure ui 
    def configUI(self):
        #name
        self.ui.light_name.textEdited.connect(self.on_name)
        #type
        self.ui.light_type.currentTextChanged.connect(self.on_type)
        #intensity
        self.ui.intensity_sp.valueChanged.connect(self.on_intensity)
        #shadows
        self.ui.cast_shadows_check_b.stateChanged.connect(self.on_cast_shadows)
        #visualize
        self.ui.visualize_checkBox.stateChanged.connect(self.on_visualize)
        #light on 
        self.ui.light_on_check_b.stateChanged.connect(self.on_light)
        #diffuse
        self.ui.diffuse_R.valueChanged.connect(self.on_diffuse)
        self.ui.diffuse_G.valueChanged.connect(self.on_diffuse)
        self.ui.diffuse_B.valueChanged.connect(self.on_diffuse)
        self.ui.diffuse_A.valueChanged.connect(self.on_diffuse)
        #specular
        self.ui.specular_R.valueChanged.connect(self.on_specular)
        self.ui.specular_G.valueChanged.connect(self.on_specular)
        self.ui.specular_B.valueChanged.connect(self.on_specular)
        self.ui.specular_A.valueChanged.connect(self.on_specular)
        #attenuation 
        self.ui.range_sp.valueChanged.connect(self.on_range)
        self.ui.constant_sp.valueChanged.connect(self.on_constant)
        self.ui.linear_sp.valueChanged.connect(self.on_linear)
        self.ui.quadratic_sp.valueChanged.connect(self.on_quadratic)
        #pose
        self.ui.pose_x_sp.valueChanged.connect(self.on_pose)
        self.ui.pose_y_sp.valueChanged.connect(self.on_pose)
        self.ui.pose_z_sp.valueChanged.connect(self.on_pose)
        self.ui.pose_roll_sp.valueChanged.connect(self.on_pose)
        self.ui.pose_pitch_sp.valueChanged.connect(self.on_pose)
        self.ui.pose_yaw_sp.valueChanged.connect(self.on_pose)
        #direction 
        self.ui.direction_x.valueChanged.connect(self.on_direction)
        self.ui.direction_y.valueChanged.connect(self.on_direction)
        self.ui.direction_z.valueChanged.connect(self.on_direction)
        #spot 
        self.ui.inner_angle_sp.valueChanged.connect(self.on_inner_angle)
        self.ui.outer_angle_sp.valueChanged.connect(self.on_outer_angle)
        self.ui.falloff_sp.valueChanged.connect(self.on_falloff)
        #addpush button
        self.ui.add_light_pb.clicked.connect(self.on_add)
        #remove pushbuton
        self.ui.remove_light_pb.clicked.connect(self.on_remove)
        
        #listwidget row changed
        self.ui.light_listWidget.currentRowChanged.connect(self.on_list_row_change)
        #reset 
        self.ui.light_Reset.clicked.connect(self.on_reset)
        
#callbacks   
    def on_reset(self):
        self.reset()
        print("light reset has been applied \n")

    def on_list_row_change(self):
        if self.ui.light_listWidget.count()!=0:
            currentIndex=self.ui.light_listWidget.currentRow()
            item=self.ui.light_listWidget.item(currentIndex)
            if item is not None:
                label=item.text()
                self.current_light=label
                self._current_light_element=self.lights[str(label)]
                type=self._current_light_element.attrib['type']
    #disable  spot and direction ui elements base on the  
    #selected type
                if type =='spot':
                    self.ui.spot_groupbox.setEnabled(True)
                else:
                    self.ui.spot_groupbox.setEnabled(False)
        
                if type=='spot' or type=='directional':
                    self.ui.direction_groupbox.setEnabled(True)
                else:
                    self.ui.direction_groupbox.setEnabled(False)
                self.update_ui()
       
        
    def on_name(self):
        #RD_globals.set_xml_data(self._current_light_element,self.tag,True,{"name":self.properties.name})
        name=self.properties.name
        count=1
        ok=False
        #ensure no duplicate names are added 
        #please dont add 1000 light sources 
        while not ok:
            if name in self.lights.keys():
                name=name.split('_')[0]+'_'+str(count)
                count+=1
            else:
                ok=True
        self._current_light_element.attrib["name"]=name
        #update dictionary 
        self.lights[name]=self.lights.pop(self.current_light)
        #update the current name 
        self.current_light=name
        #update the values in the ui 
        self.properties.name=RD_globals.get_xml_data(self._current_light_element,[self.tag,'name'],True)
#update type name in the list widget 
        #get current iten 
        current_item=self.ui.light_listWidget.currentRow()
        item=self.ui.light_listWidget.item(current_item)
        #set name of the curret item 
        item.setText(name)
    
         
    def on_type(self):
        #RD_globals.set_xml_data(self._current_light_element,self.tag,True,{'type':self.properties.type})
        current_type=self.properties.type
        self._current_light_element.attrib["type"]=current_type
    #disable  spot and direction ui elements base on the  
    #selected type 
        if self._current_light_element.attrib['type'] =='spot':
            self.ui.spot_groupbox.setEnabled(True)
        else:
            self.ui.spot_groupbox.setEnabled(False)
        
        if current_type=='spot' or current_type=='directional':
            self.ui.direction_groupbox.setEnabled(True)
        else:
            self.ui.direction_groupbox.setEnabled(False)
        
    def on_intensity(self):
        RD_globals.set_xml_data(self._current_light_element,"intensity",False,self.properties.intensity)
        
    def on_cast_shadows(self):
        RD_globals.set_xml_data(self._current_light_element,"cast_shadows",False,self.properties.cast_shadows)
        
    def on_visualize(self):
        RD_globals.set_xml_data(self._current_light_element,"visualize",False,self.properties.visualize)
        
    def on_light(self):
        RD_globals.set_xml_data(self._current_light_element,"light_on",False,self.properties.light_on)
        
    def on_diffuse(self):
        RD_globals.set_xml_data(self._current_light_element,"diffuse",False,self.properties.diffuse)
        
    def on_specular(self):
        RD_globals.set_xml_data(self._current_light_element,"specular",False,self.properties.specular)
        
    def on_range(self):
        RD_globals.set_xml_data(self._current_light_element,"range",False,self.properties.range)
        
    def on_constant(self):
        RD_globals.set_xml_data(self._current_light_element,"constant",False,self.properties.constant)
        
    def on_linear(self):
        RD_globals.set_xml_data(self._current_light_element,"linear",False,self.properties.linear)
        
    def on_quadratic(self):
        RD_globals.set_xml_data(self._current_light_element,"quadratic",False,self.properties.quadratic)
        
    def on_pose(self):
        RD_globals.set_xml_data(self._current_light_element,"pose",False,self.properties.pose)
        
    def on_direction(self):
        RD_globals.set_xml_data(self._current_light_element,"direction",False,self.properties.direction)
        
    def on_inner_angle(self):
        RD_globals.set_xml_data(self._current_light_element,"inner_angle",False,self.properties.inner_angle)
        
    def on_outer_angle(self):
        RD_globals.set_xml_data(self._current_light_element,"outer_angle",False,self.properties.outer_angle)
        
    def on_falloff(self):
        RD_globals.set_xml_data(self._current_light_element,"falloff",False,self.properties.falloff)
    

    def on_add(self):
    #will append a new eelement to the lights dictionary 
    #check for duplicate names if duplicates are found in the name append a number to the name
        new_elem=copy.deepcopy(self._light_element)
        name=copy.deepcopy(new_elem.attrib['name'])
        count=1
        ok=False
        #no duplicate names
        while not ok:
            if name in self.lights.keys():
                modified_name = re.sub(r"_[0-9]+$", "", name)
                name=modified_name+"_"+str(count)
                #update name attribute 
                new_elem.attrib['name']=name
                count+=1
            else:
                ok=True
        self.lights[name]=new_elem
        #set current item to new item 
        self._current_light_element=self.lights[name]
        self.ui.light_listWidget.addItem(name)
        #select the item
        item=self.ui.light_listWidget.item(self.ui.light_listWidget.count()-1)
        item.setSelected(True)
        self.ui.light_listWidget.setCurrentItem(item)
        
        #disable spot groupbox 
        self.ui.spot_groupbox.setEnabled(False)
        #disable directional groupbox
        self.ui.direction_groupbox.setEnabled(False)
        self.update_ui()
        
    def on_remove(self):
        #get current item 
        current_index=self.ui.light_listWidget.currentRow()

        item=self.ui.light_listWidget.item(current_index)
        current_light_name=item.text()
        if item is not None:
            question=QMessageBox.question(None,"Delete light","remove "+item.text()+" ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
            if question==QMessageBox.Yes:
                item=self.ui.light_listWidget.takeItem(current_index)
                #this will call on_list_row_change callback 
                del item
                 #delete the light item from the list of names
                if  current_light_name in self.lights:
                    del self.lights[current_light_name]
        #set the previous item as the currently selected item 
                if current_index>=1:
                        pass
                #if there is no previous item 
                else:
                    self._current_light_element=self._light_element
        #update the ui to match the changes 
                self.update_ui()
        
               
#end callbacks 

#update ui 
    def update_ui(self):
        self.properties.name=RD_globals.get_xml_data(self._current_light_element,[self.tag,'name'],True)
        self.properties.type=RD_globals.get_xml_data(self._current_light_element,['light','type'],True)
        self.properties.intensity=float(RD_globals.get_xml_data(self._current_light_element,"intensity",False))
        self.properties.cast_shadows=RD_globals.get_xml_data(self._current_light_element,"cast_shadows",False)
        self.properties.visualize=RD_globals.get_xml_data(self._current_light_element,"visualize",False)
        self.properties.light_on=RD_globals.get_xml_data(self._current_light_element,"light_on",False)
        self.properties.diffuse=RD_globals.get_xml_data(self._current_light_element,"diffuse",False)

        self.properties.specular=RD_globals.get_xml_data(self._current_light_element,"specular",False)
        self.properties.range=float(RD_globals.get_xml_data(self._current_light_element,"range",False))
        self.properties.constant=float(RD_globals.get_xml_data(self._current_light_element,"constant",False))
        self.properties.linear=float(RD_globals.get_xml_data(self._current_light_element,"linear",False))
        self.properties.quadratic=float(RD_globals.get_xml_data(self._current_light_element,"quadratic",False))

        self.properties.pose=RD_globals.get_xml_data(self._current_light_element,"pose",False)
        self.properties.direction=RD_globals.get_xml_data(self._current_light_element,"direction",False)
        self.properties.inner_angle=float(RD_globals.get_xml_data(self._current_light_element,"inner_angle",False))
        self.properties.outer_angle=float(RD_globals.get_xml_data(self._current_light_element,"outer_angle",False))
        self.properties.falloff=float(RD_globals.get_xml_data(self._current_light_element,"falloff",False))
        
    def reset(self,default:bool=True):
        if default:
            #clear lights and list widget 
            self.lights={}
            self.ui.light_listWidget.clear()
            self.initialize()
            self.add_sun()
        else:
            #reset lights
            #==============================================
            #============================================
            #==============================================
            if RD_globals.DEBUG is True:
                import pdb 
                pdb.set_trace()
            #=================================================
            #==================================================
            #=================================================
            spot=self._light_element.find('spot')
            direction=self._light_element.find('direction')
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=RD_globals.parse_dict(_root_dict,self.parent_path+[self.tag])
            if el_dict is not None:
                #clear list widget an light 
                self.ui.light_listWidget.clear()
                self.lights={}
                el_list=el_dict['elem_str']
                for el_str in el_list:
                    el=ET.fromstring(el_str)
                    name=el.attrib['name']
                    type=el.attrib['type']
                    #append previously removed elements since the element might be edited 
                    #and also  the other methods assume the elements are already available
                    if type !='spot':
                        el.append(copy.deepcopy(spot))
                    if type !='spot' and  type !='direction':
                        el.append(copy.deepcopy(direction))
                    #add to the lights dictionary 
                    self.lights[name]=copy.deepcopy(el)
                    #add to the list widget 
                    self.ui.light_listWidget.addItem(name)
            #set the row 
            #set item 0 as the current  selected item 
                item=self.ui.light_listWidget.item(0)
                item.setSelected(True)
                self.ui.light_listWidget.setCurrentItem(item)
            #set current index
                self._current_light_element=self.lights[item.text()]
        
        self.update_ui()
            
                        

    @property
    def element(self):
        el_dict=copy.deepcopy(self.lights)
        el_list=[]
    #remove elements depending on type selection 
        for el in el_dict.keys():
            light_type=el_dict[el].attrib['type']
            if light_type!='spot':
                el_dict[el].remove(el_dict[el].iter('spot').__next__())
                
            if light_type!='spot' and light_type!='directional':
                el_dict[el].remove(el_dict[el].iter("direction").__next__())
            el_list.append(el_dict[el])
   
        return el_list