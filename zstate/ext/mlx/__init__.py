from typing import Generator

from zstate import Plugin




class Gnode:

    id: int
    data: dict

class Gedge:

    id: int
    a: Gnode
    b: Gnode

class Ggraph:

    node_list: list[Gnode]

    def build_gedge_list(self, Gnode): pass

class Fsm:

    details: p
    ggraph: Ggraph
    current_gnode: Gnode

    def set_current(self, Gnode): pass

    def get_current(self): pass

class Timeseries(Ggraph):

    pass




class CallableWidget:
    """

    has:
    - typing for args,k2args, and return type
    - has a BaseShiny UI presentation for in,output,call argument
    - executions {args,kwargs,result,exception/throwable} are storable
  

    """
    def __init__(self,Callable,CallableWodgetArgList,CallableWidgetKwargsDict):
        pass



class LoraMlxFineTuning(CallableWidget):
    
    pass


class LoraMlxGeneration(CallableWidget):

    def __call__(self) -> Generator:
        """
        
        each yield is a token

        """
        def r():
            i = 0
            while True:
                yield i
                i += 1
        return r

@dc
class MlxQueueJob:

    id: int
    details: p
    
    status_fsm: Fsm[int]
    call: Callable

class MlxQueue(Plugin):









