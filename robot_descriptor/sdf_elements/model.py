from ..RD_utils import initialize_element_tree


class model:
    def __intit__(self,root_d):
        self.file_name='model.sdf'
        self.parent_path=['sdf']
        self._root_dict=root_d
        self.model_element=initialize_element_tree.convdict_2_tree(self.file_name)