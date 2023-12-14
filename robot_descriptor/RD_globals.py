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
ICON_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/icons"
UI_PATH=FreeCAD.getUserAppDataDir()+"Mod/RobotDescriptor/robot_descriptor/forms"
DOCUMENT=FreeCAD.ActiveDocument

import xml.etree.ElementTree as ET

import re
from typing import Union


#will be used to extract vectors from element types of vector3,pose ....
def extract_vector_n(input_string):
    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', input_string)
    return [float(num) for num in numbers]

#define and exception()
class tag_not_found(Exception):
    pass

#-----------------------------------------------------------

# this will check if a string is a vector of numbers 
# will be used bu get_xml_content to validate objects of type vector3,pose ... e.t.c
def assert_vect(s):
    pattern = r'(?<![\d.-])\-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?:\s+\-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)+(?![\d.-])'
    return bool(re.match(pattern, s))

 
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
    except:
        return None
        # ensure no dictionaries are sent for non attributes 
    if Is_Attribute== False and isinstance(value,dict)== False:
        if isinstance(value,list):
            # equivalent string 
            string_eq=' '.join(map(str,value))
            elem.text=string_eq
        else:
            elem.text=str(value)
    else:
        #add/edit  attributes 
        for key in value.keys():
            elem.set(key,value[key])
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
    def get_value(elem:ET.Element):
        if assert_vect(elem):
            # equivalent string 
            vect_eq=extract_vector_n(elem)
            return vect_eq
        else:
            #the caller will handle the conversion of this value to the relevant data type 
            return elem
    if Is_Attribute!=True:
        elem_iter=element.iter(tag)
    else:
        elem_iter=element.iter(tag[0])
    #only a single element exists no need to use a for loop
    try:
        elem=elem_iter.__next__()
    except:
        return None
    if Is_Attribute== False:
        txt=elem.text
        return get_value(txt)  
    else:
        # return the  the attribute dictionary 
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
    if len(path)==1:
        if path[-1]=='sdf':
                return root_dict[path[-1]]
        elif path[-1] in list(root_dict.keys()):
                return root_dict[path[-1]]
        else: 
            return None
    else:
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
    if parent_dict!=None:
        if child_tag==None:
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
   
#deleting elements
def del_elem(elem:ET.Element,child_identity):
    pass

#==============================================================
#merge elements 
#==============================================================
def merge_elements(destination_el:ET.Element,source_el:ET.Element):
    '''this function will be used by reset functions to merge elements\n
    basically this will update the previous element with new values 
    1.destination element: the element to update \n
    2.source_el : element to get updated values from '''
    
    #iterate through all elements in source element
    elements_dict = {elem.tag: elem for elem in destination_el}
    #add attributes 
    destination_el.attrib.update(source_el.attrib)
    for elem in source_el:
        if elem.tag in elements_dict:
            # If the element exists in destibnation_el, replace attributes and content
            existing_elem = elements_dict[elem.tag]
            destination_el.remove(existing_elem)
            destination_el.append(source_el.find(elem.tag))
        else:
            # If the element doesn't exist, add it to destination_el
    #dont append additional elements 
            destination_el.append(elem)
           