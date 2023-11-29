from . import dc

@dc
class Plugin: pass


@dc
class Runtime:

    runtime_state_dict: dict = None
    plugin_state_dict: dict = None
    plugin_ordereddict: dict = None


    instance = None

    @classmethod
    def get_instance(cls):
        
        if cls.instance == None:
            cls.instance = Runtime()
        return cls.instance



