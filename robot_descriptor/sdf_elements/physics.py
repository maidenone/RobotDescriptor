
import xml.etree.ElementTree as ET
from ..RD_parser import initialize_element_tree
from .. import RD_globals

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
        return self.ui.ode_iters.Value()
    @iters.setter
    def iters(self,value):
        self.ui.ode_iters.setValue(value)
#min step size
    @property
    def min_step_size(self):
        return self.ui.ode_minstep_size.Value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.ode_minstep_size.setValue(value)
#precon iters
    @property
    def precon_iters(self):
        return self.ui.ode_precon_iters.Value()
    @precon_iters.setter
    def precon_iters(self,value):
        self.ui.ode_precon_iters.setValue(value)
#island threads
    @property
    def island_threads(self):
        return self.ui.ode_island_threads.Value()
    @island_threads.setter
    def island_threads(self,value):
        self.ui.ode_island_threads.setValue(value)
#sor 
    @property 
    def sor(self):
        return self.ui.ode_sor.Value()
    @sor.setter
    def sor(self,value):
        self.ui.ode_sor.setValue(value)
    
#friction model 
    @property
    def friction_model(self):
        return self.ui.ode_friction_model.currentText()
    @friction_model.setter
    def friction_model(self,text):
        self.ui.ode_friction_model.setCurentText(text)
        
#use dynamic moi scaling
    @property
    def use_dynameic_moi_rescaling(self):
        state=self.ui.dynamic_moi_rescaling_checkb.checkState()
        if state==True:
            return 1
        else:
            return 0
    
    @use_dynameic_moi_rescaling.setter
    def use_dynamic_moi_rescaling(self,state:bool):
        self.ui.dynamic_moi_rescaling_checkb.setCheckState(state)
#thread position correction 
    @property
    def thread_positon_correction(self):
        state=self.ui.Thread_positon_correction_checkb.checkState()
        if state==True:
            return 1
        else:
            return 0
    @thread_positon_correction.setter
    def thread_position_correction(self,state:bool):
        self.ui.Thread_positon_correction_checkb.setCheckState(state)
#constraints 
class ode_constraints_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
#cfm
    @property
    def cfm(self):
        return self.ui.ode_cfm.Value()
    @cfm.setter
    def cfm(self,value):
        self.ui.ode_cfm.setValue(value)
#erp
    @property
    def erp(self):
        return self.ui.ode_erp.Value()
    @erp.setter
    def erp(self,value):
        self.ui.ode_erp.setValue(value)
#contact_max_correcting_vel
    @property 
    def contact_max_correcting_vel(self):
        return self.ui.contact_max_correcting_vel()
    @contact_max_correcting_vel.setter
    def contact_max_correcting_vel(self,value):
        self.ui.contact_max_correcting_vel.setValue(value)
        
#contact_surface_layer
    @property
    def contact_surface_layer(self):
        return self.ui.contact_surface_layer.Value()
    @contact_surface_layer.setter
    def contact_surface_layer(self,value):
        self.uicontact_surface_layer.setValue(value)
 

#bullet properties
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
        return self.ui.bullet_iters.Value()
    @iters.setter
    def iters(self,value):
        self.ui.bullet_iters.setValue(value)
        
#min step size
    @property
    def min_step_size(self):
        return self.ui.bullet_minstep_size.Value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.bullet_minstep_size.setValue(value)
    
#sor 
    @property
    def sor(self):
        return self.ui.bullet_sor.Value()
    @sor.setter
    def sor(self,value):
        self.ui.bullet_sor.setValue(value)
    
class bullet_constraint_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
    
#cfm 
    @property
    def cfm(self):
        return self.ui.bullet_cfm.Value()
    @cfm.setter
    def cfm(self,value):
        self.ui.bullet_cfm.setValue(value)
#contact surface layer
    @property
    def contact_surface_layer(self):
        return self.ui.bullet_contact_surface_layer.Value()
    @contact_surface_layer.setter
    def contact_surface_layer(self,value):
        self.ui.bullet_contact_surface_layer.setValue(value)
#erp 
    @property
    def erp(self):
        return self.ui.bullet_erp.Value()
    @erp.setter
    def erp(self,value):
        self.ui.bullet_erp.setValue(value)
# split impulse  penetration threshold
    @property
    def split_impulse_penetration_threshold(self):
        return self.ui.bullet_split_impulse_penetration_threshold.Value()
    @split_impulse_penetration_threshold.setter
    def split_impulse_penetration_threshold(self,value):
        self.ui.bullet_split_impulse_penetration_threshold.setValue(value)
#split impulse
    @property
    def split_impulse(self):
        return self.ui.bullet_split_impulse.checkState()
    @split_impulse.setter
    def split_impulse(self,state:bool):
        self.ui.bullet_split_impulse.setCheckState(state)


class simbody_contact_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
   
#stiffness
    @property
    def stiffness(self):
        return self.ui.simbody_stiffness.Value()
    @stiffness.setter
    def stiffness(self,value):
        self.ui.simbody_stiffness.setValue(value)
        
#plastic coefficient restitution
    @property
    def plastic_coef_restitution(self):
        return self.ui.simbody_plastic_coef_restitution.Value()
    @plastic_coef_restitution.setter
    def plastic_coef_restitution(self,value):
        self.ui.simbody_plastic_coef_restitution.setValue()
    
#plastic impact velocity 
    @property
    def plastic_impact_velocity(self):
        return self.ui.simbody_plastic_impact_velocity.Value()
    @plastic_impact_velocity.setter
    def plastic_impact_velocity(self,value):
        self.ui.simbody_plastic_impact_velocity.setValue(value)
    
#override impact capture velocity 
    @property
    def override_impact_capture_velocity(self):
        return self.ui.simbody_override_impact_capture_velocity.Value()
    @override_impact_capture_velocity.setter
    def override_impact_capture_velocity(self,value):
        self.ui.simbody_override_impact_capture_velocity.setValue(value)
        
#dissipation 
    @property 
    def dissipation(self):
        return self.ui.simbody_dissipation.Value()
    @dissipation.setter
    def dissipation(self,value):
        self.ui.simbody_dissipation.setValue(value)
    
#static friction 
    @property 
    def static_friction(self):
        return self.ui.simbody_static_friction.Value()
    @static_friction.setter
    def static_friction(self,value):
        self.ui.simbody_static_friction.setValue(value)

# dynamic friction 
    @property 
    def dynamic_friction(self):
        return self.ui.simbody_dynamic_friction.Value()
    @dynamic_friction.setter
    def dynamic_friction(self,value):
        self.ui.simbody_dynamic_friction.setValue(value)

#viscous friction 
    @property
    def viscous_friction(self):
        return self.ui.simbody_viscous_friction.Value()
    @viscous_friction.setter
    def viscous_friction(self,value):
        self.ui.simbody_viscous_friction.setValue(value)
        
# override_stiction_transition_velocity      
    @property
    def override_stiction_transition_velocity(self):
        return self.ui.simbody_override_stiction_transition_velocity.Value()
    @override_impact_capture_velocity.setter
    def override_impact_capture_velocity(self,value):
        self.ui.simbody_override_stiction_transition_velocity.setValue(value)

      
class simbody_properties:
    def __init__(self,ui) -> None:
        self.ui=ui
    
# min step size
    @property
    def min_step_size(self):
        return self.ui.simbody_min_step_size.Value()
    @min_step_size.setter
    def min_step_size(self,value):
        self.ui.simbody_min_step_size.setValue(value)
    
# maximum transient velocity 
    @property 
    def maximum_transient_velocity(self):
        return self.ui.simbody_max_transient_velocity.Value()
    @maximum_transient_velocity.setter
    def max_transient_velocity(self,value):
        self.ui.simbody_max_transient_velocity.setValue(value)
# accuracy 
    @property
    def accuracy(self):
        return self.ui.simbody_accuracy.Value()
    @accuracy.setter
    def accuracy(self,value):
        self.ui.simbody_accuracy.setValue(value)

class dart_properties:
    def __init__(self,ui) -> None:
        self.ui=ui

class ode:
    def __init__(self,ui,element:ET.Element):
        self.ui=ui
        self.solver=ode_solver_properties(ui)
        self.constraints=ode_constraints_properties(ui)
        self._ode_elem=element
        self.configUI()

#define callbacks       
    def configUI(self):
        self.ui.ode_solver_type_cb.currentIndexChanged.connect(self.on_type)
        self.ui.ode_minstep_size.valueChanged.connect(self.on_min_step_size)
        self.ui.ode_island_threads.valueChanged.connect(self.on_island_threads)
        self.ui.ode_friction_model.currentIndexChanged.connect(self.on_friction_model)
        self.ui.ode_iters.valueChanged.connect(self.on_iters)
        self.ui.ode_precon_iters.valueChanged.connect(self.on_precon_iters)
        self.ui.ode_sor.valueChanged.connect(self.on_sor)
        self.ui.dynamic_moi_rescaling_checkb.stateChanged.connect(self.on_dynamic_moi_rrescaling)
        self.ui.ode_cfm.valueChanged.connect(self.on_cfm)
        self.ui.ode_erp.valueChanged.connect(self.on_erp)
        self.ui.contact_max_correcting_vel.valueChanged.connect(self.on_contact_max_correction_vel)
        self.ui.contact_surface_layer.valueChanged.connect(self.on_contact_surface_layer)
#callbcks 
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
        RD_globals.set_xml_data(self._ode_elem,"use_dynamic_moi_rescaling",False,self.solver.use_dynameic_moi_rescaling)
    
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
        pass
#this takes an element  and updates the internal ones 
    def reset(self,new_elem:ET.Element):
        self._ode_elem=new_elem

     
class bullet:
    def __init__(self,ui) -> None:
        self.ui=ui
        self.solver=bullet_solver_properties(ui)
        self.constraints=bullet_constraint_properties(ui)
        
class simbody:
    def __init__(self,ui) -> None:
        self.ui=ui
        self.properties=simbody_properties(ui)
        self.contact=simbody_contact_properties(ui)
        
#physics configurations 
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
        return self.ui.physics_max_step_size.Value()
    @max_step_size.setter
    def max_step_size(self,value):
        self.ui.physics_max_step_size.setValue(value)
    
# real time factor
    @property
    def real_time_factor(self):
        return self.ui.physics_real_time_factor.Value()
    @real_time_factor.setter
    def real_time_factor(self,value):
        self.ui.physics_real_time_factor.setValue(value)

#real time update rate
    @property
    def real_time_update_rate(self):
        return self.ui.physics_real_time_update_rate.Value()
    @real_time_update_rate.setter
    def real_time_update_rate(self,value):
        self.ui.physics_real_time_update_rate.setValue(value)


    
    
class physics:
    def __init__(self,ui) -> None:
        self.parent_PATH=["sdf","world"]
        self.tag='physics'
        self.ui=ui
        self.file_name="physics.sdf"
        self.physics_elem=initialize_element_tree.convdict_2_tree(self.file_name).get_element
        self.properties=physics_properties()
    
    
    