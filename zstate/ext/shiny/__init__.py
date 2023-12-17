import os,abc

from typing import Self,Type,Any 

from dataclasses import \
    field, \
    dataclass as dc

from shiny import ui, App, Inputs, Outputs, Session
from shiny import render, reactive, render

import shinyswatch

from .point import *

from starlette.routing import Mount

from zstate.ext.starlette import MountablePlugin,BaseMountable

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
    def build_uikey_child_list(self,parent_uikey,context_dict: dict): 
        """
        produce a list fo the uikeys that this Mountable can produce for a given navarea_key:
        top/left/0..n 
        top/right/0..m
        widget/nowkast?
        """
        pass
    
    @abc.abstractmethod
    def build_ui(self,uikey,context_dict: dict) -> Any:
        pass


@dc
class PointShinyApp(ShinyAppMountable):
    """

    a mountable that takes its content in the form of points

    """
    root: Point 

    def build_uikey_child_list(self,parent_uikey,context_dict=None):
        r = None
        if self.root != None and type(self.root) != Point:
            breakpoint()

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

    def build_ui(self,uikey,context_dict=None):
        r = None
        p = self.root.search_decendents(uikey)
        
        # breakpoint()
        if p != None and type(p) == Point:
            return p.render_to_ui_content(context_dict=context_dict,
                                          stack=None)
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

    def build_ui_topnav(self,context_dict): 
        r_args = []
       
        for i in self.build_uikey_child_list("topnav/left"):
            r_args.append( ui.nav( i, self.build_ui(i,context_dict) ) )

        r_args.append(ui.nav_spacer())

        for i in self.build_uikey_child_list("topnav/right"):
            r_args.append( ui.nav( i, self.build_ui(i,context_dict) ) )

        r = ui.navset_tab( *r_args )
        return r 

    def build_ui_footer(self,context_dict):
        r = ui.div( ui.tags.hr(),
                    ui.span( f"copyright 2023 - ZeroServer Foundation" ), 
                    # ui.span( ui.a("Privacy Policy", {"href":"/"} ),
                    #          " --- ",
                    #          ui.a("Terms of Use", {"href":"/"} ) 
                    #        )
                  )
        return r

    def build_ui_root(self,context_dict):
        r_args = [ #{"style": "background-color: rgba(1, 1, 1, 0.1)"},
                 self.theme,
                 self.build_ui_topnav(context_dict),
                 self.build_ui_footer(context_dict)
        ]

        breakpoint()
        r = ui.page_fluid( *r_args )
        return r


    def server_entrypoint(self,input,output,session,*args,**kwargs): 
        if False:
            session_connection = session._conn.conn.session
            user = session_connection.get("user")
            dlog(f"new session for user={user}","info")        
            # breakpoint()

            @output
            @render.text
            def r1():
                return f"r1 output[{ session.http_conn.session.get('user') }] { pf( [input, output, session, args, kwargs] ) }"

        elif False:
            from nowkast.shiny import nk_chat_server
            [ nk_chat_server(f"chat{i}") for i in range(10) ]
            breakpoint()

        elif True:
            WidgetTest.server_for(id="test1")

    def _on_pre_run_build_subroute_list(self,
                                starletterouter,
                                route_list,
                                middleware_list,
                                sr_data):
        context_dict = {
            "starletterouter": starletterouter,
            "route_list": route_list,
            "middleware_list": middleware_list,
            "sr_data": sr_data
        }
        app = App( 
            self.build_ui_root(context_dict),
            self.server_entrypoint
        ) 
        r = []
        r.append( Mount("/", app) )
        
        breakpoint()
        return r
   

@dc
class BaseShinyMountablePlugin(MountablePlugin):
    """

    i understand this is overly complicated but this provides a MountablePlugin who is mountable as a BaseShiny, which is what I want for nowkast

    hopefully this at least shields dev users form the confusion of the underlying multi-inheritance of BaseShiny and Mountable Plugin

    i imagine this will be cleanewd up when the documentation is writeen because te documentation process will draw out that the design doesn't make much sense


    """
    root: Point = None

    def as_mountable(self,prefix):
        """ return a mountable presentation which will be a BaseShiny
        """
        outer_self = self
        
        @dc
        class MpBaseShiny(BaseShiny):
            outer_self: MountablePlugin = None

        return MpBaseShiny(prefix=prefix,
                           root=outer_self.root,
                           outer_self=outer_self)



@dc
class WidgetField: 
    """
    
    this is the fields that are defined in a Widget class


    """
    name: str
    field_type: type
    




class WidgetMeta(type):
    """



    """
    widget_class_dict = {}
    
    def __new__(mcls, name, bases, attrs):
        attrs["_instance_list"] = []

        """ this below is a placeholder for alternatively wrapping init instead of using __new__ in widget for registration

        helpful links:
https://stackoverflow.com/questions/56918764/using-metaclass-to-keep-track-of-instances-in-python
https://stackoverflow.com/questions/392160/what-are-some-concrete-use-cases-for-metaclasses
                    
        """
        if False:
            def wrapped_init(self,*args,**kwargs):
                breakpoint()
            attrs["__init__"] = wrapped_init

        mcls.widget_class_dict[name] = r = type.__new__(mcls, name, bases, attrs)
        return r

    @classmethod
    def get_widgetclass_for_dataclass(mcls, id: str, dataclass_cls: Type): 
        """

        this parses a given dataclass to produce a list of WidgetFileds, which is used to create a Widget class

        perhaps this should be static on the widget class, but since we want to be able to subclass the widget class to perform different formatting and storage, it seems like the generations of field data which is populated into a class (as a stati-to-the-class datastructure) should be produced at the meta level.  

        """
        fields = []
        for k,v in dataclass_cls.__annotations__.items():
            breakpoint()

        widgetfield_list = []
        for f in fields:
            wf = WidgetField(name=n,field_type=t)
            widget_field_list.append(wf)

        breakpoint()
        return 
    
    @classmethod
    def get_widgetclass_for_sqlmodelclass(mcls, id: str, sqlmodel_cls: Type): 
        breakpoint()
        return






@dc
class Widget(metaclass=WidgetMeta):
    """

    has a list of fields
    has cacpcity to generate a shiny module for CRUD on those field, and produce a list CRUD too, 
    s

    """

    field_list: list[WidgetField]

    def build_ui(self): pass

    def build_server(self): pass

    def server_for(self,id):
        dlog("this needs to be scoped to the namespace in session i'm pretty sure")
        breakpoint()

    @classmethod
    def __new__(cls,*args,**kwargs):
        r = super().__new__(cls,*args,**kwargs)
        cls.__instance_list__.append(r)
        return r



@dc
class WidgetTestDataclass:

    name: str
    desc: str

    tests: list[str] = field(default_factory=list)
    

