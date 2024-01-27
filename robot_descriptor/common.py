'''
This contains variables and functions that will be used globally \n
by many functions 
functions:\n
set_xml_data(): to write data to xml elements\n
get_xml_data: to read data from xml elements

variable:
UI_PATH
ICON_PATH

'''
DEBUG=True



import os 
import FreeCAD
ICON_PATH=os.path.join(FreeCAD.getUserAppDataDir()+"Mod","RobotDescriptor","robot_descriptor","icons")
UI_PATH=os.path.join(FreeCAD.getUserAppDataDir()+"Mod","RobotDescriptor","robot_descriptor","forms")
DOCUMENT=FreeCAD.ActiveDocument
import copy
import xml.etree.ElementTree as ET

import re
from typing import Union


#will be used to extract vectors from element types of vector3,pose ....
def extract_vector_n(input_string):
    '''this extracts a vector from a string of  numbers '''
    #input_string.strip().split(' ') could aslo work here 
    #well lets go with some regex 
    #because this might also be used  for comma separated values 
    
    numbers=re.findall(r'-?(?:\d+\.\d+|\.\d+|\d+)(?:e-?\d+)?',input_string)

    return [float(num) for num in numbers]

#define and exception()
class tag_not_found(Exception):
    pass

#-----------------------------------------------------------
re_pattern=re.compile(
    (
    r"((\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*)|"
    r"((\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*)|"
    r"((\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*)|"
    r"(\s*(-|\+)?\d+\s+(-|\+)?\d+\s*)|"
    r"((\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*)|"
    r"(\d+ \d+)|"
    r"((\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*)"
)
)
# this will check if a string is a vector of numbers 
# will be used bu get_xml_content to validate objects of type vector3,pose ... e.t.c
def assert_vect(s):
    #original
    #pattern = r'(?<![\d.-])\-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?:\s+\-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)+(?![\d.-])'
    #update
    return bool(re_pattern.match(s))

 
# ==============================================================================
# write data to xml file 
#===============================================================================
def set_xml_data(element:ET.Element,tag:str,Is_Attribute:bool,value:Union[dict,float,int,list,str])->ET.Element:
    '''
    tag is the tag name of the element to be edited \n
    Element is
    Is Attribute  can either be true or false , True if th value is an attribute \n
    if Is_Attribute is True value has to be a dictionary with one or more key value pairs \n
    The value parameter will contain the actual value to be updated
    '''
    #get the affected element
    elem_iter=element.iter(tag)
    #no need for a loop
    try:
        elem=elem_iter.__next__()
    except Exception:
        return None
        # ensure no dictionaries are sent for non attributes 
    if Is_Attribute is False and isinstance(value,dict) is False:
        if isinstance(value,list):
            # equivalent string 
            elem.text=' '.join(map(str,value))
        else:
            elem.text=str(value)
    else:
        #add/edit  attributes 
        for key in value.keys():
            elem.set(key,str(value[key]))
    return element


#================================================================================
#get data from xml file 
def get_xml_data(element:ET.Element,tag:Union[str,list],Is_Attribute:bool=False)->Union[list,dict,str]:
    '''
    see set_xml_data()
    The functions have  similar parameters
    except for the value parameter which is not included and tag \n
    for attributes a list is used in place of tag with the parent tag at index 0 and attribute name at index 1  \n
    This e.g ['world','name'] will return the name attribute of the world element\n
    ->for none string values the caller  is responsible for converting to appropriate types'''
    def get_value(elem_data):
        if assert_vect(elem_data):
            # equivalent string 
            vect_eq=extract_vector_n(elem_data)
            return vect_eq
        else:
            #try converting to int or float date type 
            try:
                try:
                    return int(elem_data)
                except Exception:
                    return float(elem_data)    
            except Exception:
                return elem_data
    
    if Is_Attribute is not True:
        elem_iter=element.iter(tag)
    else:
        elem_iter=element.iter(tag[0])
    #only a single element exists no need to use a for loop
    try:
        elem=elem_iter.__next__()
    except Exception:
        return None
    if Is_Attribute is False:
        txt=elem.text
        if txt is None:
            txt=''
        return get_value(txt)  
    else:
        # return the  the attribute dictionary 
        try:
            try:
                return   int(elem.attrib[tag[1]])
            except Exception:
                return float(elem.attrib[tag[1]])
        except Exception:
            return   elem.attrib[tag[1]]

#deleting attributes
def del_attribute(elem:ET.Element):
    # delete all available attributes  first
        # some attributes may be disabled hence 
        #  remove the previous ones
        for key in list(elem.attrib.keys()):
            del elem.attrib[key]
#==============================================
# parse dictionary find parent element and return it 
#====================================================
def parse_dict(root_dict:dict,path:list):
    '''
    root_dict is the dictionary to parse
    path :is how to get from the root element to an element \n
    to get from the root  to model ['sdf','world','model']
    the first string  in the path list should be the tag name \n
    of the root_elemet
    returns a dictionary 
    '''
    
# used to track the current index of the path list  
    current_idx=0
    #if only  one element is left return it 
    if len(path)==1:
        if path[-1]=='sdf':
                return root_dict[path[-1]]
        #check if the element exists
        elif path[-1] in list(root_dict.keys()):
                return root_dict[path[-1]]
        else: 
            return None
    else:
        #get the first item in the dictionary
        parent_key=path[current_idx]
        current_idx+=1
#child element tag
        e_tag=path[current_idx]
#check if tag is in list  return none if not 
        if e_tag in list(root_dict[parent_key]["children"].keys()):
            return parse_dict(root_dict[parent_key]["children"],path[current_idx:])
        else:
            return None
 
#==========================================================================
#the path parameter helps with navigating the  dictionary
#=============================================================================
def update_dictionary(path:list,child_tag:Union[str,None],elem:Union[list,ET.Element])->Union[bool,None]:
    '''
    parameters:
     1. first element is a proxy object that stores the elem dictionary 
     2. Element to append to parent 
     3. path to the parent element implemented a list see RD_globals.parse_dict
     4. elem: element to be updated or inserted
    This parses the dictionary stored in the proxy attribute   for a parent with tag parent_elem \n
    and appends elem_str  and returns True
     if the parent with that tag is not found  False is returned''' 
     
#get the element dictionary 
    elem_dict=FreeCAD.ActiveDocument.Robot_Description.Proxy.element_dict

    parent_dict=parse_dict(elem_dict,path)
    if parent_dict is not None:
        #this allows update of an element  not its children basically None means not the children
        if child_tag is None:
            if isinstance(elem,list):
                parent_dict["elem_str"]=list(map(lambda e:ET.tostring(e,encoding="unicode"),elem))
            else:
                parent_dict["elem_str"]=ET.tostring(elem,encoding="unicode")
        else:
            
            if isinstance(elem,list):
                #check if child is available then create it if not 
                parent_dict["children"][child_tag]=None
                parent_dict["children"][child_tag]={'elem_str':list(map(lambda e:ET.tostring(e,encoding="unicode"),elem)),"recurring":True,"children":{}}
                    
            else:
                parent_dict["children"][child_tag]=None
                parent_dict["children"][child_tag]={'elem_str':ET.tostring(elem,encoding="unicode"),"recurring":False,"children":{}}
               
#I dont know if this is necessary 
        FreeCAD.ActiveDocument.Robot_Description.Proxy.element_dict=elem_dict
        return True
    return False
   

#==============================================================
#merge elements 
#==============================================================
def merge_elements(destination_el:ET.Element,source_el:ET.Element,recursive:bool=False):
    '''this function will be used by reset functions to merge elements\n
    basically this will update the previous element with new values 
    1.destination element: the element to update \n
    2.source_el : element to get updated values from 
    3. This will  be used to determine if a '''
    
#implementatyion for physics element
#its best to just implement it within the physics class
#but for consistency 
#its here 
#++++++++++++++++++++======================
    if recursive is True:
#implemtatation for recusive elements are implementd here 
        pass  
#implemtatation for all other elements 
#the ones that are not recursive and not physics                 
    else:
        # Update attributes of destination_el with source_el
        destination_el.attrib.update(source_el.attrib)
        if source_el.text:
            destination_el.text = source_el.text
    # Merge child elements recursively
        for child in source_el:
            existing_el = destination_el.find(child.tag)
            if existing_el is not None:
                merge_elements(existing_el, child)  # Recursively merge the existing element with the new one
            else:
            # If the element doesn't exist in destination, simply append it
                # destination_el.append(child)
                pass


import math 
from PySide.QtGui import QColorDialog


class color_pickr:
    '''class that implements color picker methods 
    '''
    def __init__(self) -> None:
        pass
    #color picker
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
            
    #color seter
    #used to set color properties of color picker buttons 
    def set_widget_color(self,prop:str,widget):
        color_str=','.join([str(math.ceil(i*255)) for i in getattr(self.properties,prop)])
        widget.setStyleSheet(f"background-color: rgba({color_str});")