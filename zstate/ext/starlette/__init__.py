# from .app import *

import os,abc

from typing import Self,Any,Union 

from dataclasses import \
    field, \
    dataclass as dc

from functools import partial

from starlette.routing import Mount, Host, Router, Route
from starlette.applications import Starlette

from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from starlette.responses import Response,RedirectResponse,PlainTextResponse
from starlette.staticfiles import StaticFiles

from zstate import Plugin

from zstate.debug import *
from pprint import pformat as pf



@dc
class Mountable:
    """
    the point is to on initialization, 

    add to the routes, middleware, etc.

    so each Mountable should be called in order and have a chance to modify those 
    
    """

    prefix: str

    def _on_pre_run(self,
                    starletterouter,
                    route_list: list,
                    middleware_list: list,
                    sr_data: dict) -> None:
        self.starletterouter = starletterouter


res = Response

@dc
class BaseMountable(Mountable,metaclass=abc.ABCMeta):

    def _on_pre_run(self,
                    starletterouter: Any,
                    route_list: list,
                    middleware_list: list,
                    sr_data: dict) -> None:
        
        Mountable._on_pre_run(self,starletterouter, route_list, middleware_list, sr_data)
        sub_route_list = self._on_pre_run_build_sub_route_list(starletterouter,route_list,middleware_list,sr_data)

        if type(sub_route_list) != list:
            sub_route_list = [ sub_route_list ]

        route_list.append( Mount( self.prefix, routes=sub_route_list ) )

    @abc.abstractmethod
    def _on_pre_run_build_sub_route_list(self,
                    starletterouter: Any,
                    route_list: list,
                    middleware_list: list,
                    sr_data: dict) -> None:
        pass

@dc
class TestMountable(BaseMountable):

    def _on_pre_run_build_sub_route_list(self,
                    starletterouter: Any,
                    route_list: list,
                    middleware_list: list,
                    sr_data: dict) -> None:
        
        r = []
        # r.append( Mount("/test_mount", self.test_mount_fn) )
        r.append( Route("/pf", 
                        partial( self.test_route_fn, 
                                [], 
                                {"build_mount_data": { "starletterouter": starletterouter, "route_list": route_list, "middleware_list": middleware_list, "sr_ata":sr_data }} )) )
        return r

    async def test_mount_fn(self,*args,**kwargs):
        dbp(1,dev_tagcode="this causes a HTTP 500, saying that ASGI callable returned without starting a response")
        return res("test") 

    async def test_route_fn(self,*args,**kwargs):
        return res( pf(locals()) ) 



@dc
class StarletteRouter(Plugin):
    """


    """
    mountable_list: list[Mountable] = field(default_factory=list)

    route_list: list[Union[Mount,Route]] = field(default_factory=list)
    middleware_list: list = field(default_factory=list)

    sr_data: dict = field(default_factory=dict)

    def run(self,*arg,**kwargs):
        for p in self.mountable_list:
            p._on_pre_run(self,
                          self.route_list,
                          self.middleware_list,
                          self.sr_data)

        self.app = Starlette( routes=self.route_list, middleware=self.middleware_list, debug=True )


class MountablePlugin(Plugin,metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _init_mountable_build_sub_route_list(self,
                        prefix: str,
                        starletterouter: StarletteRouter,
                        route_list: list,
                        middleware_list: list,
                        sr_data: dict) -> None:
        pass


    def as_mountable(self,prefix):
        """
        send a mountable adaptor for this plugin
        typically this would be done to create the mountable list for the starlette plugin's constructor
        and in the above case, it will not have been registered
        therefore, the point is to just create the object and return it, and expect all initialization to take place later
        
        expected initialization flow would be:

        - _on_registered_with_runtime to be called by Runtime.__post_init__ 
          - any onotify_registered_with_runtime_callbackfn_list entries are called, as part of the Plugin's base _on_registered_with_runtime method         - _on_pre_run method to be called by StarletteRounter.run
          - the base method implementation of _on_pre_run in BaseMountable calls on _on_pre_run_build_mount to build a starlette.routing.Mount object for this Mountable

        """
        outer_self = self
        
        @dc
        class MpBaseMountable(BaseMountable):
            outer_self: MountablePlugin 

            def _on_pre_run_build_sub_route_list(self,
                                    starletterouter: StarletteRouter,
                                    route_list: list,
                                    middleware_list: list,
                                    sr_data: dict) -> None:
                return self.outer_self._init_mountable_build_sub_route_list(prefix,starletterouter,route_list,middleware_list,sr_data)

        return MpBaseMountable(prefix=prefix,
                               outer_self=outer_self)
                              


