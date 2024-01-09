import FreeCAD
import FreeCADGui
import robot_descriptor.common as common
import os

'''
assembly4 Technical manual 
https://github.com/Zolko-123/FreeCAD_Assembly4/blob/master/TECHMANUAL.md

'''

def read_assembly():
    links=FreeCAD.ActiveDocument.findObjects("App::Link")
        #links in Assembly4 are of type "App::Link" 
        #this is a list 
        #this will store a list of dictionaries 
    def create_structure(data,dest):
        #check the parent objects 
        children=[child for child in data if child["parent"]==dest["name"]]
        if len (children)==0:
            return
        for ch in children:
            dest["children"].append(ch)
            create_structure(data,ch)
        
            
    link_data=[]
    #create the root parent
    structured_data={}
    for child in links:
        name=child.Label
            #attachedTo returns a string of the format 'Parent Assembly#LCS_Origin' hence
            #hence separating by the the '#' and  taking the first element will be the parent 
            #the 2nd the coordinate system its attached to 
        parent,attachement=child.AttachedTo.split('#')
            #Attachmensts are usually made with reference to coordiante systems of type "PartDesign::CoordinateSystem" find them in all links
            # and remove  lcs with label 'LCS_Origin' in case it exists in model 
        coordinate_systems=[ lcs for lcs in child.Document.findObjects("PartDesign::CoordinateSystem") if lcs.Label !='LCS_Origin' ]
        link_data.append({"link":child,"name":name,"parent":parent,"attachment":attachement,"coordinate_systems":coordinate_systems,'children':[]})
        #
        #create a  hierarchial data 
        
        root_lcs=FreeCAD.ActiveDocument.findObjects("PartDesign::CoordinateSystem")
        structured_data={"link":None,'name':"Parent Assembly","attachment":None,"coordinate_systems":root_lcs,"children":[]}
        
        #this will just create a hierarchial data representation 
    create_structure(link_data,structured_data)
    del link_data
    return structured_data

    
