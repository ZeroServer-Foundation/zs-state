from typing import Optional,Any

from collections import OrderedDict

from dataclasses import field, dataclass as dc




@dc
class Plugin: 

    registered_with_runtime_completed_callback_list: list = field(default_factory=list)

    def __post_init__(self): pass

    def handle_registered_with_runtime(self,runtime,*args,**kwargs): 
        self.registered_runtime = runtime
        for i in self.registered_with_runtime_completed_callback_list:
            i(self,runtime,*args,**kwargs)
    


@dc
class Runtime:

    runtime_state_dict: Optional[dict[str,Any]] = field(default_factory=dict)
    plugin_state_dict: Optional[dict[str,dict[str,Any]]] = field(default_factory=dict)
    plugin_ordereddict: Optional[dict[str,Plugin]] = field(default_factory=OrderedDict)

    instance = None

    def __post_init__(self): 
        for k,v in self.plugin_ordereddict.items():
            v.handle_registered_with_runtime(runtime=self)

    @classmethod
    def get_instance(cls):
        if cls.instance == None:
            cls.instance = Runtime()
        return cls.instance



