import abc

from enum import Enum

from typing import Union, Optional, Self, TypeVar

from dataclasses import dataclass,field,KW_ONLY

from htmltools import Tag

from zstate.debug import *

rich_str = str

@dataclass
class Point:
    """
    content: 

    """
    banner: str = None
    child_list: list[Self] = None 

    _: KW_ONLY

    summary: str = None
    details: rich_str = None
    
    # these can be done using children
    # bullet_list: list[str] = None
    # def_list: list[tuple[str,str]] = None
    parent: Self = None

    @classmethod
    def _normalize(cls,
                   p: Union[Self,Tag,
                            list[Union[Self,Tag]],
                            str],
                   parent=None):
        r = None
        
        if type(p) == Point:
            r = p
            assert r.child_list == None or type(r.child_list) == list
            if p.child_list != None and len(p.child_list):
                r.child_list = cls._normalize(p.child_list,parent=p)
        
        elif type(p) == list:
            r = []
            for i in p:
                r.append(cls._normalize(i,parent=parent))
        elif type(p) == str:
            r = Point(banner=p,parent=parent)
            # dbp()
        elif type(p) == Tag:
            r = p
        else:
            dbp(1) 
        
        if False and type(r) == list:
            dbp(1)

        return r

    @classmethod
    def prepare(cls, 
                plist: Union[list[Self]|Self],
                key_prefix: str = None, 
        ):
        """
        take a Point, or a list thereof, and prefix the keys of that point with the given str param
    
        """
        if type(plist) != list:
            plist = [plist]
        
        r = []
        for i in plist:
            if len([ x for x in i.child_list if x == None ]):
                dbp(1)
            r.append( cls._normalize(i) )

        return r

    def render_to_ui_content(self,stack=None):
        from shiny import ui
        
        r = []
        
        if False:
            r.append( ui.pre(pf(self)) )
        
        else:

            l = 0
            if stack != None:
                l = len(stack) 
                
            t = [
                    ui.tags.h1,
                    ui.tags.h2,
                    ui.tags.h3,
                    ui.tags.h4,
                    ui.tags.h5,
                    ui.tags.h6,
                    ui.tags.p
                 ]
            
            if self.banner:
                if l > 6:
                    dbp(1)

                r.append( t[l](self.banner) )  

            if self.summary:
                r.extend(self.summary)
            
            if self.details:
                dbp(1)

            if self.child_list:
                for i in self.child_list:
                    if i == None:
                        dbp(1)
                    
                    elif type(i) == Point:
                        fn_stack = None
                        if stack == None:
                            fn_stack = [ self ]
                        else:
                            fn_stack = stack[:]
                            fn_stack.append( self )
                        
                        dev_tagcode(f"{self.banner} this needs some serious verification {stack and len(stack),len(fn_stack)}")
                        # breakpoint()

                        r.extend( i.render_to_ui_content(fn_stack) )

                    elif type(i) == list:
                        dbp(1)
                    
                    elif type(i) == Tag:
                        r.append(i)
                    
                    else:
                        dbp(1)

                            
        return r

    def resolve(self,*args,**kwargs):
        """
        this is called in the tagify process, which decends down the DOM like assembly that happens in py-htmltools, turning the TagList object that represents the children of a Tag, i believe to render further child/ascestor elements into that structure

        because this Point object got stuck into the nav argument, it needs to duck type itself to allow for these calls in the rendering process

        nov20 04e: i think basically this is going to swap a TagList, so this is where we can convert a Point into a ui.* structures and swap it out?

        """
        dbp(1)
        from shiny import ui

        nav = self.banner
        contents = None
        if self.child_list:
            contents = []
            for c in self.child_list:
                if False:
                    contents.append(pf(c))
                else:
                    x = c.resolve()
                    print(self,type(x),x)
                    breakpoint()
                    contents.append(x)
        return nav,contents

    def get_value(self,*args,**kwargs):
        """

        has to do with NavSetArg protocol in shiny.ui, which calls this method on args to a navset, looks like to establish which nav to have marked as selected.  if you return None, it assumes the first one is the one selected

        """
        dbp(1)
        return None

    def encode(self,*args,**kwargs):
        """

        has to do with NavSetArg protocol in shiny.ui, which calls this method on args to a navset, looks like to establish which nav to have marked as selected.  if you return None, it assumes the first one is the one selected

        """
        msg = """
        - this should be replaced by a navset render 
        - but you need to check into shiny.App, because this route need to be handled there
        - shiny.App is a single page app
        https://asgi.readthedocs.io/en/latest/introduction.html
        """
        dbp(level=1,start_here=1,dev_tagcode=msg)
        return None

OptionalPointList = Optional[list[Point]]


def cycle(token_list: list):
    return ",".join(token_list)

