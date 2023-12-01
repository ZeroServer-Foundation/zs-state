import os

from typing import Self,Any 

from dataclasses import dataclass, field

from shiny import ui, App, Inputs, Outputs, Session
from shiny import render, reactive, render

import shinyswatch

from .point import *

from zstate.ext.starlette import Mountable

from zstate.debug import *

from pprint import pformat as pf


class ShinyMountable(Mountable):
    

    def server_entrypoint(self,input,output,session,owner,*args,**kwargs): 
        """
        in addition to having the constructs that match the miffleware and route parameters of a StarletteRouter's Mountable, Shiny Mountables produce widgets 
    
        """
        pass


    def build_uikey_list(self,navarea_key,*args,**kwargs): 
        """
        produce a list fo the uikeys that this Mountable can produce for a given navarea_key:
        top/left/0..n 
        top/right/0..m
        widget/nowkast?
        """
        pass
    
    def build_ui(self,uikey,*args,**kwargs) -> Any:
        pass

@dataclass
class ShinyAppBuilder:
    """
    
    for each host:
      build app from routes


    """
    theme = shinyswatch.theme.darkly()
    default_help_nav = ui.nav(
        "Help",
        ui.div("help nav")
    )

    def build_topnav(self, sm: ShinyMountable): 
        r_args = []
       
        for i in sm.build_topnav_keylist("left"):
            r_args.append(sm.build_ui_nav(i))

        r_args.append(ui.nav_spacer())

        for i in sm.build_topnav_keylist("right"):
            r_args.append(sm.build_ui_nav(i))

        r = ui.navset_tab( *r_args )
        return r 



    def build_footer(self, sm: ShinyMountable):
        r = ui.div( ui.tags.hr(),
                    ui.span( f"copyright 2023 - {org.full_name}" ), 
                   # ui.span( ui.a("Privacy Policy", {"href":"/"} ),
                   #          " --- ",
                   #          ui.a("Terms of Use", {"href":"/"} ) 
                   #        )
                  )
        return r

    def build_main_page(self, sm: ShinyMountable):
        args = [ #{"style": "background-color: rgba(1, 1, 1, 0.1)"},
                 self.theme,
                 self.build_topnav(sm),
                 self.build_footer(sm)
        ]

        # breakpoint()
        r = ui.page_fluid( *args )
        return r


    def server_entrypoint(self, 
                          input: Inputs, output: Outputs, session: Session,
                          sm: ShinyMountable):
        """
        oabr.module_dict has the registered modules from initialiaztion

        server entrypoint is called on each connection
          input, output, and session is created

        org is set for the connection at hand, which is defined by the route that was matched in the router

        """
        for k,v in self.oabr.module_dict.items():
            v.server_entrypoint(input, output, session, sm)

    def build_app_for_org(self, sm: ShinyMountable):
        mp = self.build_main_page(sm)

        from functools import partial
        fn = partial(self.server_entrypoint, sm=sm)
        r = App(mp,fn)

        return r


