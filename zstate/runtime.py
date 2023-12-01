from typing import Optional,Any

from collections import OrderedDict

from dataclasses import field, dataclass as dc




@dc
class Plugin: 

    # at the moment of registration with the Runtime, this list will be travsed and called
    # or more accurately this is done in __post_init__ of the Runtime
    notify_registered_with_runtime_callbackfn_list: list = field(default_factory=list)

    def __post_init__(self): pass

    def _on_registered_with_runtime(self,runtime,*args,**kwargs): 
        for i in self.notify_registered_with_runtime_callbackfn_list:
            i(self,runtime,*args,**kwargs)
    


@dc
class Runtime:

    runtime_state_dict: Optional[dict[str,Any]] = field(default_factory=dict)
    plugin_state_dict: Optional[dict[str,dict[str,Any]]] = field(default_factory=dict)
    plugin_ordereddict: Optional[dict[str,Plugin]] = field(default_factory=OrderedDict)

    instance = None

    def __post_init__(self): 
        self.registered_runtime = self
        for k,v in self.plugin_ordereddict.items():
            v._on_registered_with_runtime(runtime=self)

    

    @classmethod
    def get_instance(cls):
        if cls.instance == None:
            cls.instance = Runtime()
        return cls.instance



