
1. RC_parsexml.py is the main file to parse sdf description files and  creates a dictionary to store the elements and attributes and text 

illustration 
{
    tag: str  , element tag

    attributes: a list of Element_attribute class 

    parent: Element  ,link to parent element

    value: str    value stored in the element 

    chldren: a list of dictionaries  , stores a list on children elements 

    description: str this will have data from the description tag 

    default: default value 

    required: can either be (0,1 or *)
    
    type: this is the type of the value in the attributes 
}

2. all parsing will start from the root.sdf file   

3. include tag names  have a filname attribute that  conatains the name of a functions or methodds when needed
    they can be parsed separately and appended to tha root  element tree as children 


#Tasks 
 1.add an iterator method to be used when traversing the tree to find children e.g when model is called the parent  element needs to be identified the search needs to begin from the root hence an iterator to help in selecting the right elements to visit
 

NOTE: 
    watch the ElemDict variable and Main_ElemDict