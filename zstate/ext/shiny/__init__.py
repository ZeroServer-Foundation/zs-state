import os

from typing import Self,Any 

from dataclasses import \
    field,
    dataclass as dc


from shiny import ui, App, Inputs, Outputs, Session
from shiny import render, reactive, render

import shinyswatch

from .point import *

from zstate.ext.starlette import Mountable

from zstate.debug import *

from pprint import pformat as pf


@dc
class ShinyAppMountable(Mountable):
    """

    a ShinyMountable extends the zstate.ext.starlette.Mountable to add a server and ui generation capacity

    """
    def server_entrypoint(self,input,output,session,owner,*args,**kwargs): 
        """
        in addition to having the constructs that match the miffleware and route parameters of a StarletteRouter's Mountable, Shiny Mountables produce widgets 
    
        """
        pass

    def build_uikey_child_list(self,parent_uikey,*args,**kwargs): 
        """
        produce a list fo the uikeys that this Mountable can produce for a given navarea_key:
        top/left/0..n 
        top/right/0..m
        widget/nowkast?
        """
        pass
    
    def build_ui(self,uikey,*args,**kwargs) -> Any:
        pass


@dc
class PointShinyApp(ShinyAppMountable):
    """

    a mountable that takes its content in the form of points

    """
    root: Point 


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

    def build_topnav(self): 
        r_args = []
       
        for i in sm.build_topnav_keylist("left"):
            r_args.append(sm.build_ui_nav(i))

        r_args.append(ui.nav_spacer())

        for i in sm.build_topnav_keylist("right"):
            r_args.append(sm.build_ui_nav(i))

        r = ui.navset_tab( *r_args )
        return r 



    def build_footer(self):
        r = ui.div( ui.tags.hr(),
                    ui.span( f"copyright 2023 - {org.full_name}" ), 
                    # ui.span( ui.a("Privacy Policy", {"href":"/"} ),
                    #          " --- ",
                    #          ui.a("Terms of Use", {"href":"/"} ) 
                    #        )
                  )
        return r

    def build_root(self):
        args = [ #{"style": "background-color: rgba(1, 1, 1, 0.1)"},
                 self.theme,
                 self.build_topnav(),
                 self.build_footer()
        ]

        # breakpoint()
        r = ui.page_fluid( *args )
        return r

