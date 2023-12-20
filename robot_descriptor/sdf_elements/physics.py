
import xml.etree.ElementTree as ET
from ..RD_parser import initialize_element_tree
from .. import RD_globals
import copy
from PySide import QtCore

import FreeCAD

#==============================================
#ode solver properties 
#========================================
class ode_solver_properties:
    def __init__(self,ui):
        self.ui=ui
#type 
    @property
    def type(self):
        return self.ui.ode_solver_type_cb.currentText()
    @type.setter
    def type(self,text):
        self.ui.ode_solver_type_cb.setCurrentText(text)
#iters
    @property
    def iters(self):
        return self.ui.ode_iters.value()
    @iters.setter
    def iters(self,value):
        self.ui.ode_iters.setValue(value)
#min step size
    @property
    def min_step_size(self):
        return self.ui.ode_minstep_size.value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.ode_minstep_size.setValue(value)
#precon iters
    @property
    def precon_iters(self):
        return self.ui.ode_precon_iters.value()
    @precon_iters.setter
    def precon_iters(self,value):
        self.ui.ode_precon_iters.setValue(value)
#island threads
    @property
    def island_threads(self):
        return self.ui.ode_island_threads.value()
    @island_threads.setter
    def island_threads(self,value):
        self.ui.ode_island_threads.setValue(value)
#sor 
    @property 
    def sor(self):
        return self.ui.ode_sor.value()
    @sor.setter
    def sor(self,value):
        self.ui.ode_sor.setValue(value)
    
#friction model 
    @property
    def friction_model(self):
        return self.ui.ode_friction_model.currentText()
    @friction_model.setter
    def friction_model(self,text):
        self.ui.ode_friction_model.setCurrentText(text)
        
#use dynamic moi scaling
    @property
    def use_dynamic_moi_rescaling(self):
        state=self.ui.dynamic_moi_rescaling_checkb.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
    
    @use_dynamic_moi_rescaling.setter
    def use_dynamic_moi_rescaling(self,state:bool):
        if state is True:
            self.ui.dynamic_moi_rescaling_checkb.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.dynamic_moi_rescaling_checkb.setCheckState(QtCore.Qt.Unchecked)
#thread position correction 
    @property
    def thread_position_correction(self):
        state=self.ui.thread_position_correction_checkb.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
    @thread_position_correction.setter
    def thread_position_correction(self,state:bool):
        if state is True:
            self.ui.thread_position_correction_checkb.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.thread_position_correction_checkb.setCheckState(QtCore.Qt.Unchecked)
            
#=========================================================        
#ode constraints
#=========================================================
class ode_constraints_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#cfm
    @property
    def cfm(self):
        return self.ui.ode_cfm.value()
    @cfm.setter
    def cfm(self,value):
        self.ui.ode_cfm.setValue(value)
#erp
    @property
    def erp(self):
        return self.ui.ode_erp.value()
    @erp.setter
    def erp(self,value):
        self.ui.ode_erp.setValue(value)
#contact_max_correcting_vel
    @property 
    def contact_max_correcting_vel(self):
        return self.ui.contact_max_correcting_vel.value()
    @contact_max_correcting_vel.setter
    def contact_max_correcting_vel(self,value):
        self.ui.contact_max_correcting_vel.setValue(value)
        
#contact_surface_layer
    @property
    def contact_surface_layer(self):
        return self.ui.contact_surface_layer.value()
    @contact_surface_layer.setter
    def contact_surface_layer(self,value):
        self.ui.contact_surface_layer.setValue(value)
 
#============================================================
#bullet properties
#==============================================================
class bullet_solver_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
    @property
#type 
    @property
    def type(self):
        return self.ui.bullet_solver_type.currentText()
    @type.setter
    def type(self,text):
        self.ui.bullet_solver_type.setCurrentText(text)
#iters 
    @property
    def iters(self):
        return self.ui.bullet_iters.value()
    @iters.setter
    def iters(self,value):
        self.ui.bullet_iters.setValue(value)
        
#min step size
    @property
    def min_step_size(self):
        return self.ui.bullet_minstep_size.value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.bullet_minstep_size.setValue(value)
    
#sor 
    @property
    def sor(self):
        return self.ui.bullet_sor.value()
    @sor.setter
    def sor(self,value):
        self.ui.bullet_sor.setValue(value)
#===============================================================
#bullet constraints
#===================================================================  
class bullet_constraint_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
    
#cfm 
    @property
    def cfm(self):
        return self.ui.bullet_cfm.value()
    @cfm.setter
    def cfm(self,value):
        self.ui.bullet_cfm.setValue(value)
#contact surface layer
    @property
    def contact_surface_layer(self):
        return self.ui.bullet_contact_surface_layer.value()
    @contact_surface_layer.setter
    def contact_surface_layer(self,value):
        self.ui.bullet_contact_surface_layer.setValue(value)
#erp 
    @property
    def erp(self):
        return self.ui.bullet_erp.value()
    @erp.setter
    def erp(self,value):
        self.ui.bullet_erp.setValue(value)
# split impulse  penetration threshold
    @property
    def split_impulse_penetration_threshold(self):
        return self.ui.bullet_split_impulse_penetration_threshold.value()
    @split_impulse_penetration_threshold.setter
    def split_impulse_penetration_threshold(self,value):
        self.ui.bullet_split_impulse_penetration_threshold.setValue(value)
#split impulse
    @property
    def split_impulse(self):
        state= self.ui.bullet_split_impulse.isChecked()
        if state:
            return str('true')
        else:
            return str('false')
    @split_impulse.setter
    def split_impulse(self,state:bool):
        if state is True:
            self.ui.bullet_split_impulse.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.bullet_split_impulse.setCheckState(QtCore.Qt.Unchecked) 
            
#=============================================================================
#simbody contact 
#=============================================================================
class simbody_contact_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
   
#stiffness
    @property
    def stiffness(self):
        return self.ui.simbody_stiffness.value()
    @stiffness.setter
    def stiffness(self,value):
        self.ui.simbody_stiffness.setValue(value)
        
#plastic coefficient restitution
    @property
    def plastic_coef_restitution(self):
        return self.ui.simbody_plastic_coef_restitution.value()
    @plastic_coef_restitution.setter
    def plastic_coef_restitution(self,value):
        self.ui.simbody_plastic_coef_restitution.setValue(value)
    
#plastic impact velocity 
    @property
    def plastic_impact_velocity(self):
        return self.ui.simbody_plastic_impact_velocity.value()
    @plastic_impact_velocity.setter
    def plastic_impact_velocity(self,value):
        self.ui.simbody_plastic_impact_velocity.setValue(value)
    
#override impact capture velocity 
    @property
    def override_impact_capture_velocity(self):
        return self.ui.simbody_override_impact_capture_velocity.value()
    @override_impact_capture_velocity.setter
    def override_impact_capture_velocity(self,value):
        self.ui.simbody_override_impact_capture_velocity.setValue(value)
        
#dissipation 
    @property 
    def dissipation(self):
        return self.ui.simbody_dissipation.value()
    @dissipation.setter
    def dissipation(self,value):
        self.ui.simbody_dissipation.setValue(value)
    
#static friction 
    @property 
    def static_friction(self):
        return self.ui.simbody_static_friction.value()
    @static_friction.setter
    def static_friction(self,value):
        self.ui.simbody_static_friction.setValue(value)

# dynamic friction 
    @property 
    def dynamic_friction(self):
        return self.ui.simbody_dynamic_friction.value()
    @dynamic_friction.setter
    def dynamic_friction(self,value):
        self.ui.simbody_dynamic_friction.setValue(value)

#viscous friction 
    @property
    def viscous_friction(self):
        return self.ui.simbody_viscous_friction.value()
    @viscous_friction.setter
    def viscous_friction(self,value):
        self.ui.simbody_viscous_friction.setValue(value)
        
# override_stiction_transition_velocity      
    @property
    def override_stiction_transition_velocity(self):
        return self.ui.simbody_override_stiction_transition_velocity.value()

    @override_stiction_transition_velocity.setter
    def override_stiction_transition_velocity(self,value):
        self.ui.simbody_override_stiction_transition_velocity.setValue(value)

#====================================================================================
#simbody properties
#====================================================================================   
class simbody_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
    
# min step size
    @property
    def min_step_size(self):
        return self.ui.simbody_min_step_size.value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.simbody_min_step_size.setValue(value)
    
# maximum transient velocity 
    @property 
    def maximum_transient_velocity(self):
        return self.ui.simbody_max_transient_velocity.value()
    @maximum_transient_velocity.setter
    def maximum_transient_velocity(self,value):
        self.ui.simbody_max_transient_velocity.setValue(value)
# accuracy 
    @property
    def accuracy(self):
        return self.ui.simbody_accuracy.value()
    @accuracy.setter
    def accuracy(self,value):
        self.ui.simbody_accuracy.setValue(value)
        

#===================================================
#dart properties 
#====================================================

class dart_properties:
    def __init__(self,ui) -> None:
        self.ui=ui

#solver type
    @property
    def solver_type(self):
        return self.ui.dart_solver_type.currentText()
    @solver_type.setter
    def solver_type(self,text):
        self.ui.dart_solver_type.setCurrentText(text)
#collision detector
    @property
    def collison_detector(self):
        return self.ui.dart_collison_detector.currentText()
    @collison_detector.setter
    def collision_detector(self,text):
        self.ui.dart_collison_detector.setCurrentText(text)

#=====================================================================
#ode
#=====================================================================
class ode:
    def __init__(self,ui,element:ET.Element):
        self.ui=ui
        self.solver=ode_solver_properties(ui)
        self.constraints=ode_constraints_properties(ui)
        self._get_ode_elem(element)
        self.configUI()

#define callbacks 
#store own local copy of solver element
    def _get_ode_elem(self,el:ET.Element):
        self._ode_elem= copy.deepcopy(el.iter("ode").__next__())
        #remove and  append the default element so that changes 
        #made to the local copy be reflected  in the main copy 
        #create reference to the local physics element
#this is only needed for the ode sice it is the default radio button 
#and is toggled at initialization of the class 
# thus the  toggled callback function  wont be called which  calls the append method 
#that creates a reference to the local copy of the solver
        el.remove(el.iter("ode").__next__())
#make reference 
        el.append(self._ode_elem)

    def configUI(self):
        self.ui.ode_solver_type_cb.currentTextChanged.connect(self.on_type)
        self.ui.ode_minstep_size.valueChanged.connect(self.on_min_step_size)
        self.ui.ode_island_threads.valueChanged.connect(self.on_island_threads)
        self.ui.ode_friction_model.currentTextChanged.connect(self.on_friction_model)
        self.ui.ode_iters.valueChanged.connect(self.on_iters)
        self.ui.ode_precon_iters.valueChanged.connect(self.on_precon_iters)
        self.ui.ode_sor.valueChanged.connect(self.on_sor)
        self.ui.dynamic_moi_rescaling_checkb.stateChanged.connect(self.on_dynamic_moi_rescaling)
        self.ui.thread_position_correction_checkb.stateChanged.connect(self.on_thread_position_correction)
        self.ui.ode_cfm.valueChanged.connect(self.on_cfm)
        self.ui.ode_erp.valueChanged.connect(self.on_erp)
        self.ui.contact_max_correcting_vel.valueChanged.connect(self.on_contact_max_correction_vel)
        self.ui.contact_surface_layer.valueChanged.connect(self.on_contact_surface_layer)
#callbacks 

    def on_type(self):
        RD_globals.set_xml_data(self._ode_elem,"type",False,self.solver.type)
    
    def on_min_step_size(self):
        RD_globals.set_xml_data(self._ode_elem,"min_step_size",False,self.solver.min_step_size)
    def on_island_threads(self):
        RD_globals.set_xml_data(self._ode_elem,"island_threads",False,self.solver.island_threads)
    def on_friction_model(self):
        RD_globals.set_xml_data(self._ode_elem,"friction_model",False,self.solver.friction_model)
    def on_iters(self):
        RD_globals.set_xml_data(self._ode_elem,"iters",False,self.solver.iters)
    def on_precon_iters(self):
        RD_globals.set_xml_data(self._ode_elem,"precon_iters",False,self.solver.precon_iters)
    
    def on_sor(self):
        RD_globals.set_xml_data(self._ode_elem,"sor",False,self.solver.sor)
 
    def on_dynamic_moi_rescaling(self):
        RD_globals.set_xml_data(self._ode_elem,"use_dynamic_moi_rescaling",False,self.solver.use_dynamic_moi_rescaling)

    def on_thread_position_correction(self):
        RD_globals.set_xml_data(self._ode_elem,"thread_position_correction",False,self.solver.thread_position_correction)
    
    def on_cfm(self):
        RD_globals.set_xml_data(self._ode_elem,"cfm",False,self.constraints.cfm)
    
    def on_erp(self):
        RD_globals.set_xml_data(self._ode_elem,"erp",False,self.constraints.erp)
        
    def on_contact_max_correction_vel(self):
        RD_globals.set_xml_data(self._ode_elem,"contact_max_correcting_vel",False,self.constraints.contact_max_correcting_vel)
    
    def on_contact_surface_layer(self):
        RD_globals.set_xml_data(self._ode_elem,"contact_surface_layer",False,self.constraints.contact_surface_layer)
        
#end callbacks 

    def update_ui(self):
#solver 
        self.solver.type=RD_globals.get_xml_data(self._ode_elem,"type",False)
        self.solver.min_step_size=float(RD_globals.get_xml_data(self._ode_elem,"min_step_size",False))
        self.solver.island_threads=int(RD_globals.get_xml_data(self._ode_elem,"island_threads",False))
        self.solver.iters=float(RD_globals.get_xml_data(self._ode_elem,"iters",False))
        self.solver.precon_iters=int(RD_globals.get_xml_data(self._ode_elem,"precon_iters",False))
        self.solver.sor=float(RD_globals.get_xml_data(self._ode_elem,"sor",False))
        self.solver.friction_model=RD_globals.get_xml_data(self._ode_elem,"friction_model",False)
        
        if RD_globals.get_xml_data(self._ode_elem,"use_dynamic_moi_rescaling",False)=='true':
            self.solver.use_dynamic_moi_rescaling=True
        else:
            self.solver.use_dynamic_moi_rescaling=False
        
        
        if RD_globals.get_xml_data(self._ode_elem,"thread_position_correction",False)=='true':
            self.solver.thread_position_correction=True
        else:
            self.solver.thread_position_correction=False
#constraints
        self.constraints.cfm=float(RD_globals.get_xml_data(self._ode_elem,"cfm",False))
        self.constraints.erp=float(RD_globals.get_xml_data(self._ode_elem,"erp"))
        self.constraints.contact_max_correcting_vel=float(RD_globals.get_xml_data(self._ode_elem,"contact_max_correcting_vel"))
        self.constraints.contact_surface_layer=float(RD_globals.get_xml_data(self._ode_elem,"contact_surface_layer"))
#this takes an element  and updates the internal ones 
    def reset(self,new_elem:ET.Element):
        self._get_ode_elem(new_elem)
        self.update_ui()
        
    @property
    def element(self):
        return self._ode_elem
    
    
#======================================================================
#bullet 
#=======================================================================
     
class bullet:
    def __init__(self,ui,element:ET.Element) -> None:
        self.ui=ui
        self.solver=bullet_solver_properties(ui)
        self.constraints=bullet_constraint_properties(ui)
        self._get_bullet_element(element)
        self.configUI()

#will also be used when reset is called
#store local copy of solver 
    def _get_bullet_element(self,el:ET.Element):
        self._bullet_element=copy.deepcopy(el.iter("bullet").__next__())
        
#create callbacks 
    def configUI(self):
        self.ui.bullet_solver_type.currentIndexChanged.connect(self.on_type)
        self.ui.bullet_minstep_size.valueChanged.connect(self.on_min_step_size)
        self.ui.bullet_iters.valueChanged.connect(self.on_iters)
        self.ui.bullet_sor.valueChanged.connect(self.on_sor)
        self.ui.bullet_cfm.valueChanged.connect(self.on_cfm)
        self.ui.bullet_erp.valueChanged.connect(self.on_erp)
        self.ui.bullet_contact_surface_layer.valueChanged.connect(self.on_cont_surf_layer)
        self.ui.bullet_split_impulse.stateChanged.connect(self.on_split_impulse)
        self.ui.bullet_split_impulse_penetration_threshold.valueChanged.connect(self.on_splt_impl_pen_tr)
#solver
    def on_type(self):
        RD_globals.set_xml_data(self._bullet_element,"solver",False,self.solver.type)

    def on_min_step_size(self):
        RD_globals.set_xml_data(self._bullet_element,"min_step_size",False,self.solver.min_step_size)
    
    def on_iters(self):
        RD_globals.set_xml_data(self._bullet_element,"iters",False,self.solver.iters)
        
    def on_sor(self):
        RD_globals.set_xml_data(self._bullet_element,"sor",False,self.solver.sor)
#constraints 
    def on_cfm(self):
        RD_globals.set_xml_data(self._bullet_element,"cfm",False,self.constraints.cfm)
    
    def on_erp(self):
        RD_globals.set_xml_data(self._bullet_element,"erp",False,self.constraints.erp)
        
    def on_cont_surf_layer(self):
        RD_globals.set_xml_data(self._bullet_element,"contact_surface_layer",False,self.constraints.contact_surface_layer)
        
    def on_split_impulse(self):
        RD_globals.set_xml_data(self._bullet_element,"split_impulse",False,self.constraints.split_impulse)
    
    def on_splt_impl_pen_tr(self):
        RD_globals.set_xml_data(self._bullet_element,"split_impulse_penetration_threshold",False,self.constraints.split_impulse_penetration_threshold)
    
    def update_ui(self):
#solver ui
        self.solver.type=RD_globals.get_xml_data(self._bullet_element,"type",False)
        self.solver.min_step_size=float(RD_globals.get_xml_data(self._bullet_element,"min_step_size",False))
        self.solver.iters=int(RD_globals.get_xml_data(self._bullet_element,"iters",False))
        self.solver.sor=float(RD_globals.get_xml_data(self._bullet_element,"sor",False))
#constrains ui 
        self.constraints.cfm=float(RD_globals.get_xml_data(self._bullet_element,"cfm",False))
        self.constraints.erp=float(RD_globals.get_xml_data(self._bullet_element,"erp",False))
        self.constraints.contact_surface_layer=float(RD_globals.get_xml_data(self._bullet_element,"contact_surface_layer"))
        self.constraints.split_impulse_penetration_threshold=float(RD_globals.get_xml_data(self._bullet_element,
                                                                                           "split_impulse_penetration_threshold"))
        if RD_globals.get_xml_data(self._bullet_element,"split_impulse")=='true':
            self.constraints.split_impulse=True
        else:
            self.constraints.split_impulse=False
    @property
    def element(self):
        return self._bullet_element
    
    def reset(self,new_element:ET.Element):
        self._get_bullet_element(new_element)
        self.update_ui()

#=====================================================================
#simbody
#======================================================================
class simbody:
    def __init__(self,ui,element:ET.Element) -> None:
        self.ui=ui
        self.properties=simbody_properties(ui)
        self.contact=simbody_contact_properties(ui)
        self._get_simbody_element(element)
        self.configUI()
        
#keep local copy of element
    def _get_simbody_element(self,el:ET.Element):
        self._simbody_element=copy.deepcopy(el.iter("simbody").__next__())

    
    def configUI(self):      
#properties 
        self.ui.simbody_min_step_size.valueChanged.connect(self.on_min_step_size)
        self.ui.simbody_accuracy.valueChanged.connect(self.on_accuracy)
        self.ui.simbody_max_transient_velocity.valueChanged.connect(self.on_max_trans_vel)
#contact
        self.ui.simbody_stiffness.valueChanged.connect(self.on_stiffness)
        self.ui.simbody_plastic_coef_restitution.valueChanged.connect(self.on_plst_coef_rest)
        self.ui.simbody_plastic_impact_velocity.valueChanged.connect(self.on_plst_imp_vel)
        self.ui.simbody_override_impact_capture_velocity.valueChanged.connect(self.on_ovr_imp_cpt_vel)
        self.ui.simbody_dissipation.valueChanged.connect(self.on_dissipation)
        self.ui.simbody_static_friction.valueChanged.connect(self.on_static_fric)
        self.ui.simbody_dynamic_friction.valueChanged.connect(self.on_dyn_fric)
        self.ui.simbody_viscous_friction.valueChanged.connect(self.on_vsc_fric)
        self.ui.simbody_override_stiction_transition_velocity.valueChanged.connect(self.on_ovr_st_tr_vel)
#callbacks 
    #properties 
    def on_min_step_size(self):
        RD_globals.set_xml_data(self._simbody_element,"min_step_size",False,self.properties.min_step_size)
    
    def on_accuracy(self):
        RD_globals.set_xml_data(self._simbody_element,"accuracy",False,self.properties.accuracy)
    
    def on_max_trans_vel(self):
        RD_globals.set_xml_data(self._simbody_element,"max_transient_velocity",False,self.properties.maximum_transient_velocity)
    
    #contact 
    def on_stiffness(self):
        RD_globals.set_xml_data(self._simbody_element,"stiffness",False,self.contact.stiffness)
        
    def on_plst_coef_rest(self):
        RD_globals.set_xml_data(self._simbody_element,"plastic_coef_restitution",False,self.contact.plastic_coef_restitution)
        
    def on_plst_imp_vel(self):
        RD_globals.set_xml_data(self._simbody_element,"plastic_impact_velocity",False,self.contact.plastic_impact_velocity)
        
    def on_ovr_imp_cpt_vel(self):
        RD_globals.set_xml_data(self._simbody_element,"override_impact_capture_velocity",False,self.contact.override_impact_capture_velocity)
        
    def on_dissipation(self):
        RD_globals.set_xml_data(self._simbody_element,"dissipation",False,self.contact.dissipation)
        
    def on_static_fric(self):
        RD_globals.set_xml_data(self._simbody_element,"static_friction",False,self.contact.static_friction)
        
    def on_dyn_fric(self):
        RD_globals.set_xml_data(self._simbody_element,"dynamic_friction",False,self.contact.dynamic_friction)
    
    def on_vsc_fric(self):
        RD_globals.set_xml_data(self._simbody_element,"viscous_friction",False,self.contact.viscous_friction)
        
    def on_ovr_st_tr_vel(self):
        RD_globals.set_xml_data(self._simbody_element,"override_stiction_transition_velocity",False,self.contact.override_stiction_transition_velocity)
    
#update ui 
    def update_ui(self):
#properties 
        self.properties.min_step_size=float(RD_globals.get_xml_data(self._simbody_element,"min_step_size",False))
        self.properties.accuracy=float(RD_globals.get_xml_data(self._simbody_element,"accuracy",False))
        self.properties.maximum_transient_velocity=float(RD_globals.get_xml_data(self._simbody_element,"max_transient_velocity",False))
#contact 
        self.contact.stiffness=float(RD_globals.get_xml_data(self._simbody_element,"stiffness",False))
        self.contact.plastic_coef_restitution=float(RD_globals.get_xml_data(self._simbody_element,"plastic_coef_restitution",False))
        self.contact.plastic_impact_velocity=float(RD_globals.get_xml_data(self._simbody_element,"plastic_impact_velocity",False))
        self.contact.override_impact_capture_velocity=float(RD_globals.get_xml_data(self._simbody_element,"override_impact_capture_velocity",False))
        self.contact.dissipation=float(RD_globals.get_xml_data(self._simbody_element,"dissipation",False))
        self.contact.static_friction=float(RD_globals.get_xml_data(self._simbody_element,"static_friction",False))
        self.contact.dynamic_friction=float(RD_globals.get_xml_data(self._simbody_element,"dynamic_friction",False))
        self.contact.viscous_friction=float(RD_globals.get_xml_data(self._simbody_element,"viscous_friction",False))
        self.contact.override_stiction_transition_velocity=float(RD_globals.get_xml_data(self._simbody_element,"override_stiction_transition_velocity",False))
    
    @property
    def element(self):
        return self._simbody_element
    def reset(self,el:ET.Element):
        self._get_simbody_element(el)
        self.update_ui()

#===========================================================
#dart
#=======================================================self._dart_element=copy.deepcopy(el.iter("dart").__next__())====
class dart:
    def __init__(self,ui,element:ET.Element) -> None:
        self.ui=ui
        self.properties=dart_properties(self.ui)
        self._get_dart_element(element)
        self.configUI()
#keep local copy       
    def _get_dart_element(self,el:ET.Element):
        self._dart_element=copy.deepcopy(el.iter("dart").__next__())
        
    def configUI(self):
        self.ui.dart_solver_type.currentTextChanged.connect(self.on_type)
        self.ui.dart_collison_detector.currentTextChanged.connect(self.on_collision)
#callbacks       
    def on_type(self):
        RD_globals.set_xml_data(self._dart_element,"solver_type",False,self.properties.solver_type)
        
    def on_collision(self):
        RD_globals.set_xml_data(self._dart_element,"collision_detector",False,self.properties.collision_detector)
    
    def update_ui(self):
        self.properties.solver_type=RD_globals.get_xml_data(self._dart_element,"solver_type",False)
        self.properties.collision_detector=RD_globals.get_xml_data(self._dart_element,"collision_detector",False)
    @property  
    def element(self):
        return self._dart_element
    def reset(self,el:ET.Element):
        self._get_dart_element(el)
        self.update_ui() 
        

#=============================================================
#physics configurations 
#==============================================================
class physics_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
        
#max contacts 
    @property
    def max_contacts(self):
        return self.ui.physics_max_contacts.value()
    @max_contacts.setter
    def max_contacts(self,value):
        self.ui.physics_max_contacts.setValue(value)
         
# max step size
    @property
    def max_step_size(self):
        return self.ui.physics_max_step_size.value()
    @max_step_size.setter
    def max_step_size(self,value):
        self.ui.physics_max_step_size.setValue(value)
    
# real time factor
    @property
    def real_time_factor(self):
        return self.ui.physics_real_time_factor.value()
    @real_time_factor.setter
    def real_time_factor(self,value):
        self.ui.physics_real_time_factor.setValue(value)

#real time update rate
    @property
    def real_time_update_rate(self):
        return self.ui.physics_real_time_update_rate.value()
    @real_time_update_rate.setter
    def real_time_update_rate(self,value):
        self.ui.physics_real_time_update_rate.setValue(value)
 
    
#====================================================================
#main physics class 
#====================================================================

class physics:
    def __init__(self,ui) -> None:
        self.parent_path=["sdf","world"]
        self.tag='physics'
        self.ui=ui
        self.file_name="physics.sdf"
#initialize physics element
        self._physics_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element

#delete the name and default attributes    
#they  are not currently required
        del self._physics_elem.attrib["name"]
        del self._physics_elem.attrib["default"]

#initialize     properties before reset 
        self.properties=physics_properties(ui)
        self.make_local_copies()
#set the default solver type 
        self.set_default()  
        # config ui 
        self.configUI()
 #update ui with previously configured values if available
 #call reset before configui because the variable current_type_tag sset by 
 #set type is required by configui 
        self.reset(default=False)
        
    def make_local_copies(self):
        self._ode=ode(self.ui,self._physics_elem)
        self._bullet=bullet(self.ui,self._physics_elem)
        self._dart=dart(self.ui,self._physics_elem)
        self._simbody=simbody(self.ui,self._physics_elem)
            
# set the default element 
    def set_default(self):
        self.current_type_tag='ode'
#remove  solver type elements
        types=["bullet","simbody","dart"]
        for type in types:
            el=self._physics_elem.iter(type).__next__()
            self._physics_elem.remove(el)
#set the current stacked widget to the ode one 
        self.ui.physics_type_stack.setCurrentIndex(0)
        self.ui.ode_radio_btn.toggle()
        
        
 #confifure the ui        
    def configUI(self):
        self.ui.physics_max_step_size.valueChanged.connect(self.on_step_sz)
        self.ui.physics_real_time_factor.valueChanged.connect(self.on_real_time_fct)
        self.ui.physics_real_time_update_rate.valueChanged.connect(self.on_update_rt)
        self.ui.physics_max_contacts.valueChanged.connect(self.on_max_cnt)
#radio buttons
        self.ui.bullet_radio_btn.toggled.connect(self.on_bullet_radio_button)
        self.ui.ode_radio_btn.toggled.connect(self.on_ode_radio_button)
        self.ui.simbody_radio_btn.toggled.connect(self.on_simbody_radio_button)
        self.ui.dart_radio_btn.toggled.connect(self.on_dart_radio_button)
        self.ui.physics_reset_btn.clicked.connect(self.on_reset)

#reset btn pressed      
    def on_reset(self):
        self.reset(default=True)
        print("physics resets applied \n")
        
    def on_step_sz(self):
        RD_globals.set_xml_data(self._physics_elem,"max_step_size",False,self.properties.max_step_size)
        
    def on_real_time_fct(self):
        RD_globals.set_xml_data(self._physics_elem,"real_time_factor",False,self.properties.real_time_factor)
        
    def on_update_rt(self):
        RD_globals.set_xml_data(self._physics_elem,"real_time_update_rate",False,self.properties.real_time_update_rate)
        
    def on_max_cnt(self):
        RD_globals.set_xml_data(self._physics_elem,"max_contacts",False,self.properties.max_contacts)
  
#ode radio button   
    def on_ode_radio_button(self):
        self._physics_elem.remove(self._physics_elem.iter(self.current_type_tag).__next__())
        self.current_type_tag="ode"
        RD_globals.set_xml_data(self._physics_elem,self.tag,True,{"type":self.current_type_tag})
        self._physics_elem.append(self._ode.element)
#ode  is at index 0 
        self.ui.physics_type_stack.setCurrentIndex(0)
        
#bullet radio button
    def on_bullet_radio_button(self):
        self._physics_elem.remove(self._physics_elem.iter(self.current_type_tag).__next__())
        self.current_type_tag="bullet"
        RD_globals.set_xml_data(self._physics_elem,self.tag,True,{"type":self.current_type_tag})
        self._physics_elem.append(self._bullet.element)
#bullet is at index 1 
        self.ui.physics_type_stack.setCurrentIndex(1)

#simbody radio button     
    def on_simbody_radio_button(self):
    #remove current element
        self._physics_elem.remove(self._physics_elem.iter(self.current_type_tag).__next__())
        self.current_type_tag="simbody"
        RD_globals.set_xml_data(self._physics_elem,self.tag,True,{"type":self.current_type_tag})
        self._physics_elem.append(self._simbody.element)
#simbody is at index 2
        self.ui.physics_type_stack.setCurrentIndex(2)

#dart radio button 
    def on_dart_radio_button(self):
    #remove current element
        self._physics_elem.remove(self._physics_elem.iter(self.current_type_tag).__next__())
        self.current_type_tag="dart"
        RD_globals.set_xml_data(self._physics_elem,self.tag,True,{"type":self.current_type_tag})
        self._physics_elem.append(self._dart.element)
#dart is at index 3
        self.ui.physics_type_stack.setCurrentIndex(3)


    def update_ui(self):
        self.properties.max_contacts=int(RD_globals.get_xml_data(self._physics_elem,"max_contacts",False))
        self.properties.real_time_update_rate=float(RD_globals.get_xml_data(self._physics_elem,"real_time_update_rate",False))
        self.properties.real_time_factor=float(RD_globals.get_xml_data(self._physics_elem,"real_time_factor",False))
        self.properties.max_step_size=float(RD_globals.get_xml_data(self._physics_elem,"max_step_size"))
       
       
    def reset(self,default:bool=True):
        if default:
            self._physics_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
            self._ode.reset(self._physics_elem)
            self._bullet.reset(self._physics_elem)
            self._simbody.reset(self._physics_elem)
            self._dart.reset(self._physics_elem)
            self.set_default()
            del self._physics_elem.attrib["name"]
            del self._physics_elem.attrib["default"]
#update the solver elements
            
        else:
            doc=FreeCAD.ActiveDocument
            _root_dict=doc.Robot_Description.Proxy.element_dict
            el_dict=RD_globals.parse_dict(_root_dict,self.parent_path+[self.tag])

            if el_dict is not None:
                el_str=el_dict['elem_str']
                self.merge(el_str)
                self.current_type_tag=self._physics_elem.attrib['type']

            #reset individual elements since only one of them will exist in the retrieved element 
            #update ode
                if self.current_type_tag=='ode':
                    self._ode.reset(self._physics_elem)
                    self.ui.physics_type_stack.setCurrentIndex(0)
                    self.ui.ode_radio_btn.toggle()
                #update simbody 
                elif self.current_type_tag=="simbody":
                    self._simbody.reset(self._physics_elem)
                    self.ui.physics_type_stack.setCurrentIndex(2)
                    self.ui.simbody_radio_btn.toggle()
                    
                #update bullet
                elif self.current_type_tag=="bullet":
                    self._bullet.reset(self._physics_elem)
                    self.ui.physics_type_stack.setCurrentIndex(1)
                    self.ui.bullet_radio_btn.toggle()
                #update dart
                else:
                    self._dart.reset(self._physics_elem)
                    self.ui.physics_type_stack.setCurrentIndex(3)
                    self.ui.dart_radio_btn.toggle()

            else:
                pass     
        self.update_ui()

    def merge(self, el_str):
        self._physics_elem=copy.deepcopy(ET.fromstring(el_str))
            
    @property
    def element(self):
        return self._physics_elem