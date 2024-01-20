import FreeCAD
from .. import common
from ..RD_utils import initialize_element_tree
import copy
from PySide import QtCore
import xml.etree.ElementTree as ET

class link_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
        
#gravity   
    @property
    def gravity(self):
        
        state= self.ui.link_gravity_checkbox.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
        
    @gravity.setter
    def gravity(self,state):
        if state=='true':
            self.ui.link_gravity_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.link_gravity_checkbox.setCheckState(QtCore.Qt.Unchecked)
            
#enable wind
    @property
    def enable_wind(self):
        state=self.ui.link_enable_wind_checkbox.isChecked(QtCore.Qt.Checked)
        if state:
            return str('true')
        else:
            return str('false')
        
    @enable_wind.setter
    def enable_wind(self,state):
        if state=='true':
            self.ui.link_enable_wind_checkbox.setCheckState(QtCore.Qt.Ckecked)
        else:
            self.ui.link_enable_wind_checkbox.setCheckState(QtCore.Qt.Unchecked)

#self_collide
    @property
    def self_collide(self):
        return str('true') if self.ui.link_self_collide_checkbox.isChecked() else str('false')

    @self_collide.setter
    def self_collide(self,state):
        self.ui.link_self_collide_checkbox.setCheckState(QtCore.Qt.Ckecked) if state=='true' else self.ui.link_self_collide_checkbox.setCheckState(QtCore.Qt.Unchecked)
        
#kinematic
    @property
    def kinematic(self):
        return str('true') if self.ui.link_kinematic_checkbox.isChecked() else str('false')
    @kinematic.setter
    def kinematic(self,state):
        self.ui.link_kinematic_checkbox.setCheckState(QtCore.Qt.Ckecked) if state=='true' else self.ui.link_kinematic_checkbox.setCheckState(QtCore.Qt.Unchecked)
        
#velocity decay 
    #linear
    @property
    def linear(self):
       return  self.ui.velocity_decay_linear_sp.value()
    @linear.setter
    def linear(self,value):
        self.ui.velocity_decay_linear_sp.setValue(value)

    #angular
    @property
    def angular(self):
       return  self.ui.link_angular_vel_decay_sp.value()
    @angular.setter
    def angular(self,value):
        self.ui.link_angular_vel_decay_sp.setValue(value)
        
#inertial 
#fam -> fluid added mass
#xx
    @property
    def fam_xx(self):
        return self.ui.fam_xx_sp.value()
    @fam_xx.setter
    def fam_xx(self,value):
        self.ui.fam_xx_sp.setValue(value)
#xy    
    @property
    def fam_xy(self):
        return self.ui.fam_xy_sp.value()
    @fam_xy.setter
    def fam_xy(self,value):
        self.ui.fam_xy_sp.setValue(value)
#xz  
    @property
    def fam_xz(self):
        return self.ui.fam_xz_sp.value()
    @fam_xz.setter
    def fam_xz(self,value):
        self.ui.fam_xz_sp.setValue(value)
        
#p       
    @property
    def fam_xp(self):
        return self.ui.fam_xp_sp.value()
    @fam_xp.setter
    def fam_xp(self,value):
        self.ui.fam_xp_sp.setValue(value)
        
#xq
    @property
    def fam_xq(self):
        return self.ui.fam_xq_sp.value()
    
    @fam_xq.setter
    def fam_xq(self,value):
        self.ui.fam_xq_sp.setValue(value)
        
#xr
    @property
    def fam_xr(self):
        return self.ui.value()
    @fam_xr.setter
    def fam_xr(self,value):
        self.ui.fam_xr_sp.setValue(value)
        
#yy
    @property
    def fam_yy(self):
        return self.ui.fam_yy_sp.value()
    @fam_yy.setter
    def fam_yy(self,val):
        self.ui.fam_yy_sp.setValue(val)
        
#yz 
    @property
    def fam_yz(self):
        return self.ui.fam_yz_sp.value()
    @fam_yz.setter
    def fam_yz(self,val):
        self.ui.fam_yz_sp.setValue(val)
        
#yp 
    @property 
    def fam_yp(self):
        return self.ui.fam_yp_sp.value()
    @fam_yp.setter
    def fam_yp(self,value):
        self.ui.fam_yp_sp.setValue(value)
        
#yq
    @property
    def fam_yq(self):
        return self.ui.fam_yq_sp.value()
    @fam_yq.setter
    def fam_yq(self,val):
        self.ui.fam_yq.setValue(val)
#yr
    @property
    def fam_yr(self):
        return self.ui.fam_yr_sp.value()
    @fam_yr.setter
    def fam_yr(self,val):
        self.ui.fam_yr_sp.setValue(val)

#zz
    @property
    def fam_zz(self):
        return self.ui.fam_zz_sp.value()
    @fam_zz.setter
    def fam_zz(self,value):
        self.ui.fam_zz_sp.setValue(value)
#zp  
    @property
    def fam_zp(self):
        return self.ui.fam_zp_sp.value()
    @fam_zp.setter
    def fam_zp(self,val):
        self.ui.fam_zp_sp.setValue(val)

#zq
    @property
    def fam_zq(self):
        return self.ui.fam_zq_sp.value()
    @fam_zq.setter
    def fam_zp(self,val):
        self.ui.fam_zq_sp.setValue(val)
        
#zr
    @property
    def fam_zr(self):
        return self.ui.fam_zr_sp.value()
    @fam_zr.setter
    def fam_zr(self,val):
        return self.ui.fam_zr_sp.setValue(val)

#pp 
    @property
    def fam_pp(self):
        return self.ui.fam_pp_sp.value()
    @fam_pp.setter
    def fam_pp(self,value):
        self.ui.fam_pp_sp.setValue(value)

#pq
    @property
    def fam_pq(self):
        return self.ui.fam_pq_sp.value()
    @fam_pq.setter
    def fam_pq(self,val):
        self.ui.fam_pq_sp.setValue(val)
        
#pr 
    @property
    def fam_pr(self):
        return self.ui.fam_pr_sp.value()
    @fam_pr.setter
    def fam_pr(self,val):
        self.ui.fam_pr_sp.setValue(val)
#qq
    @property
    def fam_qq(self):
        return self.ui.fam_qq_sp.value()
    @fam_qq.setter
    def fam_qq(self,val):
        self.ui.fam_qq_sp.setValue(val)
        
#qr
    @property
    def fam_qr(self):
        return self.ui.fam_qr_sp.value()
    @fam_qr.setter
    def fam_qr(self,val):
        self.ui.fam_qr_sp.setValue(val)

#rr 
    @property
    def fam_rr(self):
        return self.ui.fam_rr_sp.value()
    @fam_rr.setter
    def fam_rr(self,val):
        self.ui.fam_rr_sp.setValue(val)

#======================
#link
#====================
class link:
    def __init__(self,ui,elem_struct=None):
        self.ui=ui
        self.file_name='link.sdf'
        self.tag='link'
        #models will be store as children of sdf 
        self.parent_path=['sdf','model']
        self.properties=link_properties(self.ui)
        self._inertial_element=initialize_element_tree.convdict_2_tree("inertial.sdf").get_element
        
        self.link_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        # self.link_element.append(self._inertial_element)
        self._root_dict=elem_struct
        self.configUI()
        self.UpdateUi()
    
    def get_default_elem(self):
        default_el=copy.deepcopy(self.link_element)
        default_el.append(copy.deepcopy(self._inertial_element))
        return default_el
    
    def update_elem(self,new_elem:ET.Element):
        inertial=new_elem.find("inertial")
        if inertial is not None:
            self.link_element=new_elem
            self._inertial_element=inertial
        self.UpdateUi()
        
    def configUI(self):
        self.ui.link_gravity_checkbox.stateChanged.connect(self.onGravity)
        self.ui.link_enable_wind_checkbox.stateChanged.connect(self.onEnableWind)
        self.ui.link_self_collide_checkbox.stateChanged.connect(self.onSelfCollide)
        self.ui.link_kinematic_checkbox.stateChanged.connect(self.onKinematic)
        self.ui.velocity_decay_linear_sp.valueChanged.connect(self.onLinear)
        self.ui.link_angular_vel_decay_sp.valueChanged.connect(self.onAngular)
        #inertial
        # fam=self.link_element.find(".//inertia/fluid_added_mass")
        # fam  every time the lmbda is called fam gets updated 
        self.ui.fam_xx_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xx',False,self.properties.fam_xx) )
        self.ui.fam_xy_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xy',False,self.properties.fam_xy) )
        self.ui.fam_xz_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xz',False,self.properties.fam_xz) )
        
        self.ui.fam_xp_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xp',False,self.properties.fam_xp) )
        self.ui.fam_xq_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xq',False,self.properties.fam_xq) )
        self.ui.fam_xr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'xr',False,self.properties.fam_xr) )
        
        #y
        self.ui.fam_yy_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"):common.set_xml_data(fam,'yy',False,self.properties.fam_yy))
        self.ui.fam_yz_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"):common.set_xml_data(fam,'yz',False,self.properties.fam_yz))
        
        self.ui.fam_yp_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"):common.set_xml_data(fam,'yp',False,self.properties.fam_yp))
        self.ui.fam_yq_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"):common.set_xml_data(fam,'yq',False,self.properties.fam_yq))
        self.ui.fam_yr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"):common.set_xml_data(fam,'yr',False,self.properties.fam_yr))
        
        #z
        self.ui.fam_zz_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'zz',False,self.properties.fam_zz))
        self.ui.fam_zp_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'zp',False,self.properties.fam_zp))
        self.ui.fam_zq_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'zq',False,self.properties.fam_zq))
        self.ui.fam_zr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'zr',False,self.properties.fam_zr))
        
        #p 
        self.ui.fam_pp_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'pp',False,self.properties.fam_pp))
        self.ui.fam_pq_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'pq',False,self.properties.fam_pq))
        self.ui.fam_pr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'pr',False,self.properties.fam_pr))
        
        self.ui.fam_qq_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'qq',False,self.properties.fam_qq))
        self.ui.fam_qr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'qr',False,self.properties.fam_qr))
        self.ui.fam_rr_sp.valueChanged.connect(lambda val,fam=self.link_element.find(".//inertia/fluid_added_mass"): common.set_xml_data(fam,'rr',False,self.properties.fam_rr))
        
        
  
        
#end configUI
    def onGravity(self):
        common.set_xml_data(self.link_element,'gravity',False,self.properties.gravity)
    
    def onEnableWind(self):
        common.set_xml_data(self.link_element,'enable_wind',False,self.properties.enable_wind)
        
    def onSelfCollide(self):
        common.set_xml_data(self.link_element,'self_collide',False,self.properties.self_collide)
        
    def onKinematic(self):
        common.set_xml_data(self.link_element,'kinematic',False,self.properties.kinematic)
        
    def onLinear(self):
        common.set_xml_data(self.link_element,'linear',False,self.properties.linear)
        
    def onAngular(self):
        common.set_xml_data(self.link_element,'angular',False,self.properties.angular)
    
    #element to be updaed sent to the list 
    def UpdateUi(self):
        element=self.link_element
        self.properties.gravity=common.get_xml_data(element,'gravity',False)
        self.properties.enable_wind=common.get_xml_data(element,'enable_wind',False)
        self.properties.self_collide=common.get_xml_data(element,'self_collide',False)
        self.properties.kinematic= common.get_xml_data(element,'kinematic',False)
        self.properties.linear=common.get_xml_data(element,'linear',False)
        self.properties.angular=common.get_xml_data(element,'angular',False)
        fam=self._inertial_element.find(".//fluid_added_mass")
        elem_ui_pairs={"xx":"fam_xx_sp","xy":"fam_xy_sp","xz":"fam_xz_sp","xp":"fam_xp_sp","xq":"fam_xq_sp","xr":"fam_xr_sp",
                       "yy":"fam_yy_sp","yz":"fam_yz_sp","yp":"fam_yp_sp","yq":"fam_yq_sp","yr":"fam_yr_sp","zz":"fam_zz_sp",
                       "zp":"fam_zp_sp","zq":"fam_zq_sp","zr":"fam_zr_sp","pp":"fam_pp_sp","pr":"fam_pr_sp","pq":"fam_pq_sp",
                       "qq":"fam_qq_sp","qr":"fam_qr_sp","rr":"fam_rr_sp"}
        for tag in elem_ui_pairs.keys():
            setattr(self.properties,elem_ui_pairs[tag],common.get_xml_data(fam,tag,False))
            
    #this needs to reset the  data of all links in the model 
    #how will this information be extracted 
    def reset(self,default=True):
       pass 
    @property
    def element(self):
        t_link_elem=copy.deepcopy(self.link_element)
        
        if not self.ui.link_state_groupbox.isChecked():
            for tag in ["gravity","enable_wind","self_collide","kinematic"]:
                t_link_elem.remove(t_link_elem.find(tag))
                
        if self.ui.link_velocity_decay_groupbox.isChecked():
            t_link_elem.remove(t_link_elem.find("velocity_decay"))
        
        t_inertial_elem=copy.deepcopy(self._inertial_element)
        if self.ui.fluid_added_mass_groupbox.isChecked():
            t_inertial_elem.remove(t_inertial_elem.find("fluid_added_mass"))
        
        if t_link_elem.find("inertial") is None:
            t_link_elem.append(t_inertial_elem)
        return t_link_elem