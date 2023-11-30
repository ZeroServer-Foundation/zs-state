from typing import Optional,Any

from collections import OrderedDict

from dataclasses import field, dataclass as dc




@dc
class Plugin: pass


@dc
class Runtime:

    runtime_state_dict: Optional[dict[str,Any]] = field(default_factory={})
    plugin_state_dict: Optional[dict[str,dict[str,Any]]] = field(default_factory={})
    plugin_ordereddict: Optional[dict[str,Plugin]] = field(default_factory=OrderedDict)

    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance == None:
            cls.instance = Runtime()
        return cls.instance



