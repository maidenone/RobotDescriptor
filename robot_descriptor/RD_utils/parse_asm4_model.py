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
    
    #get all objects of type part feature 
    objs=FreeCAD.ActiveDocument.findObjects("Part::Feature")
    #get objects in the parts group  
    parts=FreeCAD.ActiveDocument.Parts.Group
    #get fasteners since fasteners might not be  accesed through links 
    #remove objects in parts , coordinate systems 
    #coordinate systems are removed by checking the MapMode attribute
    #hopefully this is will get only fasteners 
    fasteners=[fast for fast in objs if fast not in parts and not hasattr(fast,'MapMode')]

    #ensure that the link and the fastener are not the same object 
    #this might occur when the parts folder contains some parts that are used in the  assembly 
    #get link documents 
    lnk_docs=[lnk.LinkedObject.Document for lnk in links]
    for fastener in fasteners:
        if fastener.Document not  in lnk_docs:
            links.append(fastener) 
   
        #links in Assembly4 are of type "App::Link" 
        #this is a list 
        #this will store a list of dictionaries 
    def create_structure(data,dest):
        #check the parent objects 
        #since data is a list of dictionaries 
        #for every element int he list check  if its parent is  dest 
        children=[child for child in data if child["parent"]==dest["name"]]
        #return of no children are found 
        if len (children)==0:
            return
        #append the children to the current item 
        for ch in children:
            dest["children"].append(ch)
            create_structure(data,ch)
        
            
    link_data=[]
    #create the root parent
    structured_data={}
    
    #links that have been iterated and not references 
    non_refs=[]
    for child in links:
        
        name=child.Label
            #attachedTo returns a string of the format 'Parent Assembly#LCS_Origin' hence
            #hence separating by the the '#' and  taking the first element will be the parent 
            #the 2nd the coordinate system its attached to 
        parent,attachement=child.AttachedTo.split('#')
        #returned type has '#' preceeding the coordinate remove it 
        attached_by=child.AttachedBy.replace('#','')
        if hasattr(child,"LinkedObject") :
            #get links  which refer to the same document
            ref=[r for r in non_refs if r.LinkedObject.Document ==child.LinkedObject.Document]
            if len(ref)==1:
            #set type as reference i.e its a copy of a link that already exists in the assembly 
                link_data.append({"ref_label":ref[0].Label,"type":"ref","link":child,"name":name,"parent":parent,"attached_to":attachement,"attached_by":attached_by,'children':[]})
            elif len(ref)==0:
               link_data.append({"ref_label":None,"type":"link","link":child,"name":name,"parent":parent,"attached_to":attachement,"attached_by":attached_by,'children':[]})
               non_refs.append(child)
            else:
                FreeCAD.Console.PrintDeveloperError("parse_asm4:error getting refs no than 1 were found, this is  a bug \n")
                return
        else:
            #add fasterners and other too 
            link_data.append({"ref_label":None,"type":"link","link":child,"name":name,"parent":parent,"attached_to":attachement,"attached_by":attached_by,'children':[]})
            
        #create a  hierarchial data 
        if hasattr(child,"LinkedObject"):
            if hasattr(child.LinkedObject.Document,"Assembly"):
                FreeCAD.Console.PrintError("Sub assemblies not supported yet \n")
                return None
        root_lcs=FreeCAD.ActiveDocument.findObjects("PartDesign::CoordinateSystem")
        structured_data={"ref_label":None,"type":"link","link":None,'name':"Parent Assembly","attachment":None,"coordinate_systems":root_lcs,"children":[]}
        
        #this will just create a hierarchial data representation 
    create_structure(link_data,structured_data)
    del link_data
    del non_refs
    return structured_data

    
