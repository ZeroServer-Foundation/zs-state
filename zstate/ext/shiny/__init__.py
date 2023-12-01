import os,abc

from typing import Self,Any 

from dataclasses import \
    field, \
    dataclass as dc


from shiny import ui, App, Inputs, Outputs, Session
from shiny import render, reactive, render

import shinyswatch

from .point import *

from starlette.routing import Mount

from zstate.ext.starlette import BaseMountable

from zstate.debug import *

from pprint import pformat as pf


@dc
class ShinyAppMountable(BaseMountable,metaclass=abc.ABCMeta):
    """

    a ShinyMountable extends the zstate.ext.starlette.Mountable to add a server and ui generation capacity

    """
    @abc.abstractmethod
    def server_entrypoint(self,input,output,session,*args,**kwargs): 
        """
        in addition to having the constructs that match the miffleware and route parameters of a StarletteRouter's Mountable, Shiny Mountables produce widgets 
    
        """
        pass

    @abc.abstractmethod
    def build_uikey_child_list(self,parent_uikey,*args,**kwargs): 
        """
        produce a list fo the uikeys that this Mountable can produce for a given navarea_key:
        top/left/0..n 
        top/right/0..m
        widget/nowkast?
        """
        pass
    
    @abc.abstractmethod
    def build_ui(self,uikey,*args,**kwargs) -> Any:
        pass


@dc
class PointShinyApp(ShinyAppMountable):
    """

    a mountable that takes its content in the form of points

    """
    root: Point 

    def build_uikey_child_list(self,parent_uikey,*args,**kwargs):
        r = None
        p = self.root.search_decendents(parent_uikey)
        if p != None and type(p) == Point:
            def str_for(x):
                if type(x) == Point:
                    return x.banner
                elif type(x) == str:
                    return x
                else:
                    breakpoint()
            r = [ str_for(i) for i in p.child_list ] 
        return r 

    def build_ui(self,uikey,*args,**kwargs):
        r = None
        p = self.root.search_decendents(uikey)
        
        # breakpoint()
        if p != None and type(p) == Point:
            return p.render_to_ui_content()
        else:
            return ui.pre( pf(locals()) )
                      



@dc
class BaseShiny(PointShinyApp):
    """

    a specific shiny app mountable that has a main page, nav, and footer

    if these are going to have different routes / different single page apps, then they should be different instances of this object

    root 
      topnav: left + space + right
        content
      footer

    """
    theme = shinyswatch.theme.darkly()

    default_help_nav = ui.nav(
        "Help",
        ui.div("help nav")
    )

    def build_ui_topnav(self,*args,**kwargs): 
        r_args = []
       
        for i in self.build_uikey_child_list("topnav/left"):
            r_args.append( ui.nav( i, self.build_ui(i,*args,**kwargs) ) )

        r_args.append(ui.nav_spacer())

        for i in self.build_uikey_child_list("topnav/right"):
            r_args.append( ui.nav( i, self.build_ui(i,*args,**kwargs) ) )

        r = ui.navset_tab( *r_args )
        return r 

    def build_ui_footer(self,*args,**kwargs):
        r = ui.div( ui.tags.hr(),
                    ui.span( f"copyright 2023 - ZeroServer Foundation" ), 
                    # ui.span( ui.a("Privacy Policy", {"href":"/"} ),
                    #          " --- ",
                    #          ui.a("Terms of Use", {"href":"/"} ) 
                    #        )
                  )
        return r

    def build_ui_root(self,*args,**kwargs):
        r_args = [ #{"style": "background-color: rgba(1, 1, 1, 0.1)"},
                 self.theme,
                 self.build_ui_topnav(*args,**kwargs),
                 self.build_ui_footer(*args,**kwargs)
        ]

        # breakpoint()
        r = ui.page_fluid( *r_args )
        return r


    def server_entrypoint(self,input,output,session,*args,**kwargs): 
        @output
        @render.text
        def r1():
            return f"r1 output{ pf( [input, output, session, args, kwargs] ) }"

    def _on_pre_run_build_mount(self,
                                starletterouter,
                                route_list,
                                middleware_list,
                                sr_data):
        args = []
        kwargs = {
            "starletterouter": starletterouter,
            "route_list": route_list,
            "middleware_list": middleware_list,
            "sr_data": sr_data
        }
        r = Mount("/",
                  App(self.build_ui_root(*args,**kwargs),self.server_entrypoint) )
        return r
    
