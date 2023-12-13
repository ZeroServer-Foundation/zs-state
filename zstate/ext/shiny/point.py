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

    def render_to_ui_content(self,
                             context_dict: dict=None,
                             stack: list=None):
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
                            # breakpoint()
                            if type(stack) == slice: 
                                breakpoint()
                            fn_stack = stack[:]
                            if type(fn_stack) == tuple: 
                                breakpoint()
                            fn_stack.append( self )
                        
                        dev_tagcode(f"{self.banner} this needs some serious verification {stack and len(stack),len(fn_stack)}")

                        # breakpoint()
                        x = i.render_to_ui_content(context_dict=context_dict,
                                                   stack=fn_stack) 
                        r.append( x )

                    elif type(i) == list:
                        dbp(1)
                    
                    elif type(i) == Tag:
                        r.append(i)
                    
                    elif callable(i):
                        r.append( i(context_dict) )

                    elif type(i) == str:
                        r.append( ui.div(i) )

                    else:
                        dbp(1)

                            
        return r

    def normalize(self,
                  context_dict: dict=None,
                  stack: list=None):

        if self.child_list == None:
            self.child_list = []

        if type(self.child_list) != list:
            dbp(1)

        for p in range(len(self.child_list)):
            
            i = self.child_list[p]
            if type(i) == str:
                i = Point(i)   
                self.child_list[p] = i

            if type(i) != Point:
                dbp(1)

            if i.parent == None:
                i.parent = self
                
            if i.parent != self:
                dbp(1)

            if type(i) == Point:
                fn_stack = None
                if stack == None:
                    fn_stack = [ self ]
                else:
                    if type(stack) == slice: 
                        breakpoint()
                    fn_stack = stack[:]
                    if type(fn_stack) == tuple: 
                        breakpoint()
                    fn_stack.append( self )
                    
                i.normalize(context_dict=context_dict,
                            stack=fn_stack) 
            elif type(i) == list:
                dbp(1)
            
            elif type(i) == Tag:
                dbp(1)
                    
            elif callable(i):
                dbp(1)

            else:
                dbp(1)
                            
        return self

    def _dep_me_resolve(self,*args,**kwargs):
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

    def _dep_me_get_value(self,*args,**kwargs):
        """

        has to do with NavSetArg protocol in shiny.ui, which calls this method on args to a navset, looks like to establish which nav to have marked as selected.  if you return None, it assumes the first one is the one selected

        """
        dbp(1)
        return None

    def _dep_me_encode(self,*args,**kwargs):
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



    def search_decendents(self,match_fn):
        if type(match_fn) == str:
            match_str = match_fn
            match_fn = lambda x: x.banner == match_str

        if match_fn(self):
            return self
        else:
            if self.child_list == None:
                breakpoint()

            for i in self.child_list:
                if type(i) == Point:
                    r = i.search_decendents(match_fn)
                    if r != None:
                        return r
            else:
                return None










OptionalPointList = Optional[list[Point]]


def cycle(token_list: list):
    return ",".join(token_list)

