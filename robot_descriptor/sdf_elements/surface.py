from ..RD_utils import initialize_element_tree
from .. import common
from PySide2 import QtGui,QtCore
import copy
import xml.etree.ElementTree as ET

class surface_properties:
    def __init__(self,ui):
        self.ui=ui 

#restitution_coefficient
    @property
    def restitution_coefficient(self):
        return self.ui.collision_restitution_coefficient_sp.value()
    @restitution_coefficient.setter
    def restitution_coefficient(self,value):
        self.ui.collision_restitution_coefficient_sp.setValue(value)
        
#threshold
    @property
    def threshold(self):
        return self.ui.collision_bounce_threshold_sp.value()
    @threshold.setter
    def threshold(self,value):
        self.ui.collision_bounce_threshold_sp.setValue(value)
        
#friction 
 #torsional
    #coefficient
    @property
    def coefficient(self):
        return self.ui.torsional_coeff_sp.value()
    @coefficient.setter
    def coefficient(self,value):
        self.ui.torsional_coeff_sp.setValue(value)
    
    #use_patch_radius
    @property
    def use_patch_radius(self):
       return str('true') if  self.ui.use_patch_radius_cb.isChecked() else str('false')
    @use_patch_radius.setter
    def use_patch_radius(self,state):
        self.ui.use_patch_radius_cb.setCheckState(QtCore.Qt.Checked) if state=='true' else self.ui.use_patch_radius_cb.seCheckState(QtCore.Qt.Unchecked)
        
    #patch_radius
    @property
    def patch_radius(self):
        return self.ui.torsional_patch_radius_sp.value()
    @patch_radius.setter
    def patch_radius(self,value):
        self.ui.torsional_patch_radius_sp.setValue(value)
        
    #surface_radius
    @property 
    def surface_radius(self):
        return self.ui.torsional_surface_radius_sp.value()
    @surface_radius.setter
    def surface_radius(self,value):
        self.ui.torsional_surface_radius_sp.setValue(value)
        
    #slip 
    @property
    def torsional_slip(self):
        self.ui.torsional_ode_slip_sp.value()
        
    @torsional_slip.setter
    def torsional_slip(self,value):
        self.ui.torsional_ode_slip_sp.setValue(value)
    
#ode 
    #mu
    @property
    def friction_ode_mu(self):
        return self.ui.surface_ode_mu_sp.value()
    @friction_ode_mu.setter
    def friction_ode_mu(self,value):
        self.ui.surface_ode_mu_sp.setValue(value)
    
    #mu2
    @property
    def friction_ode_mu2(self):
        return self.ui.surface_ode_mu2_sp.value()
    @friction_ode_mu2.setter
    def friction_ode_mu2(self,value):
        self.ui.surface_ode_mu2_sp.setValue(value)
        
    #fdir1
    @property
    def friction_ode_fdir1(self):
        return [self.ui.surface_ode_fdir1_x_sp.value(),self.ui.surface_ode_fdir1_y_sp.value(),self.ui.surface_ode_fdir1_z_sp.value()]
        
    @friction_ode_fdir1.setter
    def friction_ode_fdir1(self,vals):
        self.ui.surface_ode_fdir1_x_sp.setValue(vals[0])
        self.ui.surface_ode_fdir1_y_sp.setValue(vals[1])
        self.ui.surface_ode_fdir1_z_sp.setValue(vals[2])
    
    #slip1
    @property
    def friction_ode_slip1(self):
         return self.ui.surface_ode_slip1_sp.value()
    @friction_ode_slip1.setter
    def friction_ode_slip1(self,value):
        self.ui.surface_ode_slip1_sp.setValue(value)
        
    #slip2
    @property
    def friction_ode_slip2(self):
         return self.ui.surface_ode_slip2_sp.value()
    @friction_ode_slip2.setter
    def friction_ode_slip2(self,value):
        self.ui.surface_ode_slip2_sp.setValue(value)
        

#bullet 
    #friction
    @property
    def friction_bullet_friction(self):
        return self.ui.surface_bullet_friction_sp.value()
    @friction_bullet_friction.setter
    def friction_bullet_friction(self,value):
        self.ui.surface_bullet_friction_sp.setValue(value)
    
    #friction2  
    @property
    def friction_bullet_friction2(self):
        return self.ui.surface_bullet_friction2_sp.value()
    @friction_bullet_friction2.setter
    def friction_bullet_friction2(self,value):
        self.ui.surface_bullet_friction2_sp.setValue(value)
        
    #rolling_friction 
    @property
    def friction_bullet_rolling_friction(self):
        return self.ui.surface_bullet_rolling_friction_sp.value()
    @friction_bullet_rolling_friction.setter
    def friction_bullet_rolling_friction(self,value):
        self.ui.surface_bullet_rolling_friction_sp.setValue(value)
        
    @property
    def friction_bullet_fdir1(self):
        return [self.ui.surface_bullet_fdir1_x_sp.value(),self.ui.surface_bullet_fdir1_x_sp.value(),self.ui.surface_bullet_fdir1_x_sp.value()]
        
    @friction_bullet_fdir1.setter
    def friction_bullet_fdir1(self,vals):
        self.ui.surface_bullet_fdir1_x_sp.setValue(vals[0])
        self.ui.surface_bullet_fdir1_x_sp.setValue(vals[1])
        self.ui.surface_bullet_fdir1_x_sp.setValue(vals[2])
        
        
#contact 
    @property
    def collide_without_contact(self):
        return str('true') if  self.ui.contact_collide_without_contact_cb.isChecked() else str('false')
    @collide_without_contact.setter
    def collide_without_contact(self,state):
        self.ui.contact_collide_without_contact_cb.setCheckState(QtCore.Qt.Checked) if state=='true' else self.ui.contact_collide_without_contact_cb.setCheckState(QtCore.Qt.Unchecked)
        
 #collide_without_contact_bitmask   
    @property
    def collide_without_contact_bitmask(self):
        return self.ui.contact_collide_without_contact_bitmask_sp.value()
    @collide_without_contact_bitmask.setter
    def collide_without_contact_bitmask(self,val):
        self.ui.contact_collide_without_contact_bitmask_sp.setValue(val)
        
    @property
    def collide_bitmask(self):
        return self.ui.contact_collide_bitmask_sp.value()
    @collide_bitmask.setter
    def collide_bitmask(self,value):
        self.ui.contact_collide_bitmask_sp.setValue(value)
        
    @property
    def category_bitmask(self):
        return self.ui.contact_category_bitmask_sp.value()
    @category_bitmask.setter
    def category_bitmask(self,value):
        self.ui.contact_category_bitmask_sp.setValue(value)
        
    @property
    def poissons_ratio(self):
        return self.ui.contact_poissons_ratio_sp.value()
    @poissons_ratio.setter
    def poissons_ratio(self,value):
        self.ui.contact_poissons_ratio_sp.setValue(value)
        
    @property
    def elastic_modulus(self):
        return self.ui.contact_elastic_modulus_sp.value()
    @elastic_modulus.setter
    def elastic_modulus(self,value):
        self.ui.contact_elastic_modulus_sp.setValue(value)
    #ode
    
    @property
    def contact_ode_soft_cfm(self):
        return self.ui.contact_ode_soft_cfm_sp.value()
    @contact_ode_soft_cfm.setter
    def contact_ode_soft_cfm(self,value):
        self.ui.contact_ode_soft_cfm_sp.setValue(value)
        
    @property
    def contact_ode_soft_erp(self):
        return self.ui.contact_ode_soft_erp_sp.value()
    @contact_ode_soft_erp.setter
    def contact_ode_soft_erp(self,value):
        self.ui.contact_ode_soft_erp_sp.setValue(value)
        
    @property
    def contact_ode_kp(self):
        return  self.ui.contact_ode_kp_sp.value()
    @contact_ode_kp.setter
    def contact_ode_kp(self,value):
        self.ui.contact_ode_kp_sp.setValue(value)
        
    @property
    def contact_ode_kd(self):
        return self.ui.contact_ode_kd_sp.value()
    @contact_ode_kd.setter
    def contact_ode_kd(self,value):
        self.ui.contact_ode_kd_sp.setValue(value)
        
    @property
    def contact_ode_max_vel(self):
        return self.ui.contact_ode_max_vel_sp.value()
    @contact_ode_max_vel.setter
    def contact_ode_max_vel(self,value):
        self.ui.contact_ode_max_vel_sp.setValue(value)
        
    @property
    def contact_ode_min_depth(self):
        return self.ui.contact_ode_min_depth_sp.value()
    @contact_ode_min_depth.setter
    def contact_ode_min_depth(self,value):
        self.ui.contact_ode_min_depth_sp.setValue(value)
        
    #bullet
    @property
    def contact_bullet_soft_cfm(self):
        return self.ui.contact_bullet_soft_cfm_sp.value()
    @contact_bullet_soft_cfm.setter
    def contact_bullet_soft_cfm(self,value):
        self.ui.contact_bullet_soft_cfm_sp.setValue(value)
        
    @property
    def contact_bullet_soft_erp(self):
        return self.ui.contact_bullet_soft_erp_sp.value()
    @contact_bullet_soft_erp.setter
    def contact_bullet_soft_erp(self,value):
        self.ui.contact_bullet_soft_erp_sp.setValue(value)
        
    @property
    def contact_bullet_kp(self):
        return  self.ui.contact_bullet_kp_sp.value()
    @contact_bullet_kp.setter
    def contact_bullet_kp(self,value):
        self.ui.contact_bullet_kp_sp.setValue(value)
        
    @property
    def contact_bullet_kd(self):
        return self.ui.contact_bullet_kd_sp.value()
    @contact_bullet_kd.setter
    def contact_bullet_kd(self,value):
        self.ui.contact_bullet_kd_sp.setValue(value)
        
    @property
    def contact_bullet_split_impulse(self):
        return str('true') if self.ui.contact_bullet_split_impulse_cb.isChecked() else str('false')
    @contact_bullet_split_impulse.setter
    def contact_bullet_split_impulse(self,state):
        self.ui.contact_bullet_split_impulse_cb.setCheckState(QtCore.Qt.Checked) if state=='true' else  self.ui.contact_bullet_split_impulse_cb.setCheckState(QtCore.Qt.Unchecked)
        
    @property
    def split_impulse_penetration_threshold(self):
        return self.ui.split_impulse_penetration_threshold_sp.value()
    @split_impulse_penetration_threshold.setter
    def split_impulse_penetration_threshold(self,value):
        self.ui.split_impulse_penetration_threshold_sp.setValue(value)
        
#soft contact 
    @property
    def bone_attachment(self):
        return self.ui.soft_contact_bone_attachment_sp.value()
    @bone_attachment.setter
    def bone_attachment(self,value):
        self.ui.soft_contact_bone_attachment_sp.setValue(value)
        
        
    @property
    def stiffness(self):
        return self.ui.soft_contact_stiffness_sp.value()
    @stiffness.setter
    def stiffness(self,value):
        self.ui.soft_contact_stiffness_sp.setValue(value)
        
    @property
    def damping(self):
        return self.ui.soft_body_damping_sp.value()
    @damping.setter
    def damping(self,value):
        self.ui.soft_body_damping_sp.setValue(value)
        
    @property
    def flesh_mass_fraction(self):
        return self.ui.soft_contact_flesh_mass_fraction_sp.value()
    @flesh_mass_fraction.setter
    def flesh_mass_fraction(self,value):
        self.ui.soft_contact_flesh_mass_fraction_sp.setValue(value)
        
#=========================================
#_cb
#============================================
    #control checkboxes 
#friction 
    @property
    def surface_ode_mu_cb(self):
        return self.ui.surface_ode_mu_cb.isChecked()
        
    @property
    def surface_ode_mu2_cb(self):
        return self.ui.surface_ode_mu2_cb.isChecked()
        
    @property
    def surface_ode_slip1_cb(self):
        return self.ui.surface_ode_slip1_cb.isChecked()
        
    @property
    def surface_ode_slip2_cb(self):
        return self.ui.surface_ode_slip2_cb.isChecked()
    
    @property
    def surface_bullet_friction_cb(self):
        return  self.ui.surface_bullet_friction_cb.isChecked()
    
    @property
    def surface_bullet_friction2_cb(self):
        return self.ui.surface_bullet_friction2_cb.isChecked()
    
    @property
    def surface_bullet_rolling_friction_cb(self):
        return self.ui.surface_bullet_rolling_friction_cb.isChecked()
    
    @property
    def ode_frdir1_groupbox(self):
        return self.ui.ode_frdir1_groupbox.isChecked()
    @property
    def bullet_frdir1_groupbox(self):
        return self.ui.bullet_frdir1_groupbox.isChecked()
    
    
#contact 
    @property
    def contact_collide_without_contact_bitmask_cb(self):
        return self.ui.contact_collide_without_contact_bitmask_cb.isChecked()
    
    @property
    def contact_collide_bitmask_cb(self):
        return self.ui.contact_collide_bitmask_cb.isChecked()
    
    @property
    def contact_category_bitmask_cb(self):
        return self.ui.contact_category_bitmask_cb.isChecked()
    
    @property
    def contact_poissons_ratio_cb(self):
        return self.ui.contact_poissons_ratio_cb.isChecked()
    
    @property
    def contact_ode_soft_cfm_cb(self):
        return self.ui.contact_ode_soft_cfm_cb.isChecked()
    
    @property
    def contact_ode_soft_erp_cb(self):
        return self.ui.contact_ode_soft_erp_cb.isChecked()
    
    @property
    def contact_ode_kp_cb(self):
        return self.ui.contact_ode_kp_cb.isChecked()
    
    @property
    def contact_ode_kd_cb(self):
        return self.ui.contact_ode_kd_cb.isChecked()
    
    @property
    def contact_ode_max_vel_cb(self):
        return self.ui.contact_ode_max_vel_cb.isChecked()
    
    @property
    def contact_ode_min_depth_cb(self):
        return self.ui.contact_ode_min_depth_cb.isChecked()
    
    @property
    def contact_bullet_soft_cfm_cb(self):
        return self.ui.contact_bullet_soft_cfm_cb.isChecked()
    
    @property
    def contact_bullet_soft_erp_cb(self):
        return self.ui.contact_bullet_soft_erp_cb.isChecked()
    
    @property
    def contact_bullet_kp_cb(self):
        return self.ui.contact_bullet_kp_cb.isChecked()
    
    @property
    def contact_bullet_kd_cb(self):
        return self.ui.contact_bullet_kd_cb.isChecked()

    
#=======================================
#=======surface ===================
#================================  

class surface:
    def __init__(self,ui) -> None:
        self.ui=ui
        self.properties=surface_properties(self.ui)
        self.file_name="surface.sdf"
        self.tag="surface"
        self.surface_element=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.configUI()
        self.updateUI()
        
    
    def configUI(self):
        #bounce 
        # bounce=self.surface_element.find('bounce')
        self.ui.collision_restitution_coefficient_sp.valueChanged.connect(lambda val,bounce=self.surface_element.find('bounce'): 
            common.set_xml_data(bounce,"restitution_coefficient",False,self.properties.restitution_coefficient))
        
        self.ui.collision_bounce_threshold_sp.valueChanged.connect(lambda val,bounce=self.surface_element.find('bounce'): 
            common.set_xml_data(bounce,"threshold",False,self.properties.threshold))
        
        #torsional
        # torsional=self.surface_element.find(".//friction/torsional")
        self.ui.torsional_coeff_sp.valueChanged.connect(lambda val: 
            common.set_xml_data(self.surface_element.find(".//friction/torsional"),"coefficient",False,self.properties.coefficient))
        self.ui.use_patch_radius_cb.stateChanged.connect(lambda  val:
            common.set_xml_data(self.surface_element.find(".//friction/torsional"),"use_patch_radius",False,self.properties.use_patch_radius))
        
        self.ui.torsional_patch_radius_sp.valueChanged.connect(lambda val:
            common.set_xml_data(self.surface_element.find(".//friction/torsional"),"patch_radius",False,self.properties.patch_radius))
        
        self.ui.torsional_surface_radius_sp.valueChanged.connect(lambda val: 
            common.set_xml_data(self.surface_element.find(".//friction/torsional"),"surface_radius",False,self.properties.surface_radius))
        
        self.ui.torsional_ode_slip_sp.valueChanged.connect(lambda val:
            common.set_xml_data(self.surface_element.find(".//friction/torsional"),"slip",False,self.properties.torsional_slip))
        
        #frictional_ode
        # frictional_ode=self.surface_element.find(".//friction/ode")
        
        self.ui.surface_ode_mu_sp.valueChanged.connect(lambda val:
            common.set_xml_data(self.surface_element.find(".//friction/ode"),"mu",False,self.properties.friction_ode_mu))
        
        self.ui.surface_ode_mu2_sp.valueChanged.connect(
            lambda val: 
                common.set_xml_data(self.surface_element.find(".//friction/ode"),"mu2",False,self.properties.friction_ode_mu2)
        )
        
        self.ui.surface_ode_slip1_sp.valueChanged.connect(
            lambda val: 
                common.set_xml_data(self.surface_element.find(".//friction/ode"),"slip1",False,self.properties.friction_ode_slip1)
        )
        
        self.ui.surface_ode_slip2_sp.valueChanged.connect(
            lambda val: 
                common.set_xml_data(self.surface_element.find(".//friction/ode"),"slip2",False,self.properties.friction_ode_slip2)
        )
        
        self.ui.surface_ode_fdir1_x_sp.valueChanged.connect(self.ode_fdir1)
        self.ui.surface_ode_fdir1_y_sp.valueChanged.connect(self.ode_fdir1)
        self.ui.surface_ode_fdir1_z_sp.valueChanged.connect(self.ode_fdir1)
        
        #frictional_bullet
        # frictional_bullet=self.surface_element.find(".//fiction/bullet")
        self.ui.surface_bullet_friction_sp.valueChanged.connect(
            lambda val: 
                common.set_xml_data(self.surface_element.find(".//friction/bullet"),"friction",False,self.properties.friction_bullet_friction))
        self.ui.surface_bullet_friction2_sp.valueChanged.connect(
            lambda val:
                common.set_xml_data(self.surface_element.find(".//friction/bullet"),"friction2",False,self.properties.friction_bullet_friction2)
        )
        
        self.ui.surface_bullet_rolling_friction_sp.valueChanged.connect(
            lambda val: 
                common.set_xml_data(self.surface_element.find(".//friction/bullet"),"rolling_friction",False,self.properties.friction_bullet_rolling_friction)
        )
        

        self.ui.surface_bullet_fdir1_x_sp.valueChanged.connect(self.bullet_fdir1)
        self.ui.surface_bullet_fdir1_y_sp.valueChanged.connect(self.bullet_fdir1)
        self.ui.surface_bullet_fdir1_z_sp.valueChanged.connect(self.bullet_fdir1)
        
    #contact 
        # contact=self.surface_element.find(".//contact")
        self.ui.contact_collide_without_contact_cb.stateChanged.connect(self.on_contact_collide_without_contact)
        
        self.ui.contact_collide_without_contact_bitmask_sp.valueChanged.connect(self.on_contact_collide_without_contact_bitmask)
        
        self.ui.contact_collide_bitmask_sp.valueChanged.connect(self.on_contact_collide_bitmask)
        
        self.ui.contact_category_bitmask_sp.valueChanged.connect(self.on_contact_category_bitmask)
        self.ui.contact_poissons_ratio_sp.valueChanged.connect(self.on_contact_poissons_ratio)
        self.ui.contact_elastic_modulus_sp.valueChanged.connect(self.on_contact_elastic_modulus)
        
        #ode
        
        self.ui.contact_ode_soft_cfm_sp.valueChanged.connect(self.on_contact_ode_soft_cfm)
        self.ui.contact_ode_soft_erp_sp.valueChanged.connect(self.on_contact_ode_soft_erp)
        self.ui.contact_ode_kp_sp.valueChanged.connect(self.on_contact_ode_kp)
        self.ui.contact_ode_kd_sp.valueChanged.connect(self.on_contact_ode_kd)
        self.ui.contact_ode_max_vel_sp.valueChanged.connect(self.on_contact_ode_max_vel)
        self.ui.contact_ode_min_depth_sp.valueChanged.connect(self.on_contact_ode_min_depth)
        
        #bullet
        # contact_bullet=self.surface_element.find(".//contact/bullet")
        self.ui.contact_bullet_soft_cfm_sp.valueChanged.connect(self.on_contact_bullet_soft_cfm)
        self.ui.contact_bullet_soft_erp_sp.valueChanged.connect(self.on_contact_bullet_soft_erp)
        self.ui.contact_bullet_kp_sp.valueChanged.connect(self.on_contact_bullet_kp)
        self.ui.split_impulse_penetration_threshold_sp.valueChanged.connect(self.on_split_impulse_penetration_threshold)
        self.ui.contact_bullet_kd_sp.valueChanged.connect(self.on_contact_bullet_kd)
        self.ui.contact_bullet_split_impulse_cb.stateChanged.connect(self.on_contact_bullet_split_impulse)
        
        #soft contact 
        # soft_contact=self.surface_element.find(".//surface/soft_contact")
        self.ui.soft_contact_bone_attachment_sp.valueChanged.connect(self.on_soft_contact_bone_attachment)
        self.ui.soft_contact_stiffness_sp.valueChanged.connect(self.on_soft_contact_stiffness)
        self.ui.soft_body_damping_sp.valueChanged.connect(self.on_soft_body_damping)
        self.ui.soft_contact_flesh_mass_fraction_sp.valueChanged.connect(self.on_soft_contact_flesh_mass_fraction)
        
    #contact  
    #bullet
    def on_contact_bullet_soft_cfm(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"soft_cfm",False,self.properties.contact_bullet_soft_cfm)
        
    def on_contact_bullet_soft_erp(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"soft_erp",False,self.properties.contact_bullet_soft_erp)
        
    def on_contact_bullet_kp(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"kp",False,self.properties.contact_bullet_kp)
        
    def on_split_impulse_penetration_threshold(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"split_impulse_penetration_threshold",False,self.properties.split_impulse_penetration_threshold)
        
    def on_contact_bullet_kd(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"kd",False,self.properties.contact_bullet_kd)
        
    def on_contact_bullet_split_impulse(self):
        contact_bullet=self.surface_element.find(".//contact/bullet")
        common.set_xml_data(contact_bullet,"split_impulse",False,self.properties.contact_bullet_split_impulse)
        
    #soft contact
    def on_soft_contact_bone_attachment(self):
        soft_contact=self.surface_element.find(".//soft_contact")
        common.set_xml_data(soft_contact,"bone_attachment",False,self.properties.bone_attachment)
        
    def on_soft_contact_stiffness(self):
        soft_contact=self.surface_element.find(".//soft_contact")
        common.set_xml_data(soft_contact,"stiffness",False,self.properties.stiffness)
        
    def on_soft_body_damping(self):
        soft_contact=self.surface_element.find(".//soft_contact")
        common.set_xml_data(soft_contact,"damping",False,self.properties.damping)
        
    def on_soft_contact_flesh_mass_fraction(self):
        soft_contact=self.surface_element.find(".//soft_contact")
        common.set_xml_data(soft_contact,"flesh_mass_fraction",False,self.properties.flesh_mass_fraction)
        
    #ode
    
    def on_contact_ode_soft_cfm(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"soft_cfm",False,self.properties.contact_ode_soft_cfm)
        
    def on_contact_ode_soft_erp(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"soft_erp",False,self.properties.contact_ode_soft_erp)
        
    def on_contact_ode_kp(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"kp",False,self.properties.contact_ode_kp)
        
    def on_contact_ode_kd(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"kd",False,self.properties.contact_ode_kd)
        
    def on_contact_ode_max_vel(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"max_vel",False,self.properties.contact_ode_max_vel)
        
    def on_contact_ode_min_depth(self):
        contact_ode=self.surface_element.find(".//contact/ode")
        common.set_xml_data(contact_ode,"min_depth",False,self.properties.contact_ode_min_depth)
    
    #friction
    #ode
    def ode_fdir1(self):
        frictional_ode=self.surface_element.find(".//friction/ode")
        common.set_xml_data(frictional_ode,"fdir1",False,self.properties.friction_ode_fdir1)
    #bullet
    
    def bullet_fdir1(self):
        frictional_bullet=self.surface_element.find(".//friction/bullet")
        common.set_xml_data(frictional_bullet,"fdir1",False,self.properties.friction_bullet_fdir1)
    
    #contact 
    def on_contact_collide_without_contact(self):
        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"collide_without_contact",False,self.properties.collide_without_contact)
        
    def on_contact_collide_without_contact_bitmask(self):
        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"collide_without_contact_bitmask",False,self.properties.collide_without_contact_bitmask)
        
    def on_contact_collide_bitmask(self):

        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"collide_bitmask",False,self.properties.collide_bitmask)
        
    def on_contact_category_bitmask(self):
        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"category_bitmask",False,self.properties.category_bitmask)
    def on_contact_poissons_ratio(self):
        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"poissons_ratio",False,self.properties.poissons_ratio)
        
    def on_contact_elastic_modulus(self):
        contact=self.surface_element.find(".//contact")
        common.set_xml_data(contact,"elastic_modulus",False,self.properties.elastic_modulus)
    
    
    def updateUI(self):
        #bounce 
        bounce=self.surface_element.find('bounce')
        #{tag : property}
        bounce_pairs={"restitution_coefficient":"restitution_coefficient",
                      "threshold":"threshold"}
        for tag in bounce_pairs.keys():
            setattr(self.properties,bounce_pairs[tag],common.get_xml_data(bounce,tag,False))
            
        #torsional
        torsional=self.surface_element.find(".//friction/torsional")
        #{tag property}
        torsional_pairs={"coefficient":"coefficient","use_patch_radius":"use_patch_radius",
                         "patch_radius":"patch_radius","surface_radius":"surface_radius","slip":"torsional_slip"}
        for tag in torsional_pairs.keys():
            setattr(self.properties,torsional_pairs[tag],common.get_xml_data(torsional,tag,False))
        
        #friction 
        #ode 
        frictional_ode=self.surface_element.find(".//friction/ode")
        friction_ode_pairs={"mu":"friction_ode_mu","mu2":"friction_ode_mu2","slip1":"friction_ode_slip1",
                            "slip2":"friction_ode_slip2","fdir1":"friction_ode_fdir1"}
        for tag in friction_ode_pairs.keys():
            setattr(self.properties,friction_ode_pairs[tag],common.get_xml_data(frictional_ode,tag,False))
            
        #bullet 
        frictional_bullet=self.surface_element.find(".//friction/bullet")
        friction_bullet_pairs={"friction":"friction_bullet_friction","friction2":"friction_bullet_friction2",
                               "rolling_friction":"friction_bullet_rolling_friction","fdir1":"friction_bullet_fdir1"}
        for tag in friction_bullet_pairs.keys():
            setattr(self.properties,friction_bullet_pairs[tag],common.get_xml_data(frictional_bullet,tag,False))
        
        #contact 
        #contact
        contact=self.surface_element.find(".//contact")
        contact_pairs={"collide_without_contact":"collide_without_contact","collide_without_contact_bitmask":"collide_without_contact_bitmask",
                       "category_bitmask":"category_bitmask","poissons_ratio":"poissons_ratio","collide_bitmask":"collide_bitmask",
                       "elastic_modulus":"elastic_modulus"}
        for tag in contact_pairs.keys():
            setattr(self.properties,contact_pairs[tag],common.get_xml_data(contact,tag,False))
            
        
        #ode 
        contact_ode=self.surface_element.find(".//contact/ode")
        contact_ode_pairs={"soft_cfm":"contact_ode_soft_cfm","soft_erp":"contact_ode_soft_erp",
                           "kp":"contact_ode_kp","kd":"contact_ode_kd","max_vel":"contact_ode_max_vel",
                           "min_depth":"contact_ode_min_depth"}
        for tag in contact_ode_pairs.keys():
            setattr(self.properties,contact_ode_pairs[tag],common.get_xml_data(contact_ode,tag,False))
            
        #bullet 
        contact_bullet=self.surface_element.find(".//contact/bullet")
        contact_bullet_pairs={"soft_cfm":"contact_bullet_soft_cfm","soft_erp":"contact_bullet_soft_erp",
                              "kp":"contact_bullet_kp","kd":"contact_bullet_kd","split_impulse":"contact_bullet_split_impulse",
                              "split_impulse_penetration_threshold":"split_impulse_penetration_threshold"}
        for tag in contact_bullet_pairs.keys():
            setattr(self.properties,contact_bullet_pairs[tag],common.get_xml_data(contact_bullet,tag,False))
            
        #soft contact 
        soft_contact=self.surface_element.find(".//soft_contact")
        #since properties have the same name as the pairs no need for pairs 
        soft_contact_tags=["bone_attachment","stiffness","damping","flesh_mass_fraction"]
        for tag in  soft_contact_tags:
            setattr(self.properties,tag,common.get_xml_data(soft_contact,tag,False))
    
    def reset(self):
        pass 
    
    def update_element(self,item):
        self.surface_element=item.surface_element
        self.updateUI()
        
    #return  element 
    @property
    def element(self):
        t_surface_elem=copy.deepcopy(self.surface_element)
        #modify bounce 
        if not self.ui.collision_bounce_groupbox.isChecked():
            t_surface_elem.remove(t_surface_elem.find("bounce"))
        
        #friction
        friction=t_surface_elem.find(".//friction")
        if self.ui.surface_friction_groupBox.isChecked():
            #tor countrysion
            torsion=friction.find("torsional")
            if self.ui.friction_torsional_groupBox.isChecked():
                if not self.ui.torsional_ode_groupbox.isChecked():
                    torsion.remove(torsion.find("ode"))
            else:
                friction.remove(friction.find(torsion))
            #end torsion 
            
            #ode
            friction_ode=friction.find("ode")
            if self.ui.friction_ode_groupbox.isChecked():
                
                elems_attrb_pair={"mu":"surface_ode_mu_cb","mu2":"surface_ode_mu2_cb","slip1":"surface_ode_slip1_cb","slip2":"surface_ode_slip2_cb"
                                  ,"fdir1":"ode_frdir1_groupbox"}
                for tag in elems_attrb_pair.keys():
                    #remove element if its not enabled 
                    if not getattr(self.properties,elems_attrb_pair[tag]):
                        friction_ode.remove(friction_ode.find(tag))
            else:
                friction.remove(friction.find(friction_ode))
            #end ode 
            
            #bullet 
            friction_bullet=friction.find("bullet")
            if self.ui.surface_friction_bullet_groupbox.ischecked():
                bullet_pairs={"friction":"surface_bullet_friction_cb","friction2":"surface_bullet_friction2_cb","rolling_friction":"surface_bullet_rolling_friction_cb"
                              ,"fdir1":"bullet_frdir1_groupbox"}
                for tag in bullet_pairs.keys():
                    if not getattr(self.properties,bullet_pairs[tag]):
                        friction_bullet.remove(friction_bullet.find(tag))
            else:
                friction.remove(friction_bullet)
            #end bullet 
        else:
             #remove friction if its not enabled 
            t_surface_elem.remove(t_surface_elem.find(friction))
            
        #end friction 
        
        #contact 
        contact=t_surface_elem.find("contact")
        if self.ui.surface_contact_groupbox.isChecked():
                contact_pairs={"collide_without_contact_bitmask":"contact_collide_without_contact_bitmask_cb","collide_bitmask":"contact_collide_bitmask_cb",
                               "category_bitmask":"contact_category_bitmask_cb","poissons_ratio":"contact_poissons_ratio_cb","elastic_modulus":"contact_elastic_modulus_cb"}
                for tag in contact_pairs.keys():
                    if not getattr(self.properties,contact_pairs[tag]):
                        contact.remove(contact.find(tag))
                #ode 
                contact_ode=contact.find("ode")
                if self.ui.contact_ode_groupbox.isChecked():
                    ode_pairs={"soft_cfm":"contact_ode_soft_cfm_cb","soft_erp":"contact_ode_soft_erp_cb","kp":"contact_ode_kp_cb","kd":"contact_ode_kd_cb",
                               "max_vel":"contact_ode_max_vel_cb","min_depth":"contact_ode_min_depth_cb"}
                    for tag in ode_pairs.keys():
                        if not getattr(self.properties,ode_pairs[tag]):
                            contact_ode.remove(contact_ode.find(tag))
                else:
                    contact.remove(contact.find(contact_ode))
                #end ode 
                
                #bullet 
                contact_bullet=contact.find("bullet")
                if self.ui.contact_bullet_groupbox.isChecked():
                    bullet_pairs={"soft_cfm":"contact_bullet_soft_cfm_cb","soft_erp":"contact_bullet_soft_erp_cb","kp":"contact_bullet_kp_cb","kd":"contact_bullet_kd_cb"}
                    for tag in bullet_pairs.keys():
                        if not getattr(self.properties,bullet_pairs[tag]):
                            contact_bullet.remove(tag)
                else:
                    contact.remove(contact.find(contact_bullet))
                #end bullet       
        else:
            t_surface_elem.remove(t_surface_elem.find(contact))
        #end contact 
        
        #soft contact 
        if not self.ui.soft_contact_dart_groupbox.isChecked():
            t_surface_elem.remove(t_surface_elem.find("soft_contact"))
            
        return t_surface_elem