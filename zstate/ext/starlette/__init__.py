# from .app import *

import os,abc

from typing import Self,Any 

from dataclasses import dataclass, field

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




class Mountable:
    """
    the point is to on initialization, 

    add to the routes, middleware, etc.

    so each Mountable should be called in order and have a chance to modify those 
    
    ---

    org should have
    /point.banner

    orggroup:
    /orgkey/navkey

    dev mount:
    /orggroup/orgkey/navkey

    prod mount
    host = orggroup/orgkey / navkey
    """

    def process_setup(self,
                      route_list: list,
                      middleware_list: list,
                      data: dict) -> None:
        modL = [ 
            ("/basic_auth",  self.init_auth_basic,), 
            ("/authlib1",    self.init_auth_authlib1,), 
        ]
        for m in modL:
            prefix, target_fn = m 
            rL, m_args, m_kwargs = target_fn(prefix)

            mnt = Mount( prefix, routes=rL )
            route_list.append( mnt )
            middleware_list.append( Middleware( *m_args, **m_kwargs ) )

            # breakpoint()





@dataclass
class StarletteRouter(Plugin):
    """

    mainatin a mapping between:
    - Oab pages
    - TextStack keys { used for LangChain integration }
    - and http|shiny routing 


    typing needs to be improved, then
    metaclass entries define sections
    then field key tokens can be raken from metaclass processing for entries
    then TextStack can map that


    """
    mapping: dict = None
    module_dict: dict = None

    def run(self):
        rL = []
        rL.append( Mount("/dev", routes=self.orggroup.build_routes() ) )
        
        for k,v in self.orggroup.items():
            app = self.oab.build_app_for_org(v) 
            rL.append( Mount(f"/{k}", app=app) )

        complete = False
        dev_tagcode("COMPLETE IS FALSE")
        if complete:
            rL.append( Route("/", lambda req: RedirectResponse(url='/home') ) )
            rL.append( Mount('/static', app=StaticFiles(directory='__static__'), name="static") )
        
        mL = []
        # mL.append( Middleware(TrustedHostMiddleware,allowed_hosts=['example.com', '*.example.com'],) )
        # mL.append( Middleware(HTTPSRedirectMiddleware) )
       
        pData = {}
        for p in self.plugin_list:
            p.oabr = self
            p.process_setup(rL,mL,pData)

        self.app = Starlette( routes=rL, middleware=mL, debug=True )

    def build_host_route(self, org):
        app = self.build_app_router(org)
        r = Host(org.host_regex, name=org.name, app=app)
        
        return r



