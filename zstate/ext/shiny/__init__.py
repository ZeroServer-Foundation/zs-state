import os

from typing import Self,Any 

from dataclasses import dataclass, field

from shiny import ui, App, Inputs, Outputs, Session
from shiny import render, reactive, render

import shinyswatch

from datasetstack import fake

from .debug import *

from pprint import pformat as pf


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

    oabr: Any

    def __post_init__(self):
        pass

    def build_offering_nav(self, org: Org): 
        return self.gen_nav("Offering",menu=True)

    def build_technology_nav(self, org: Org): 
        return self.gen_nav("Technology",menu=True)

    def build_company_nav(self, org: Org): 
        return self.gen_nav("Company",menu=True)

    def build_account_nav(self, org: Org):
        """
        register / login
          by OIDC
             SMS
             EMAIL
             ETH
             QR code

        """
        return self.gen_nav("Account",menu=True)



    def build_topnav(self, org: Org): 
        r_args = []
       
        for i in org.topnav_left_keylist:
            r_args.append(org.build_ui_nav(i))

        r_args.append(ui.nav_spacer())

        for i in org.topnav_right_keylist:
            r_args.append(org.build_ui_nav(i))

        r = ui.navset_tab( *r_args )
        return r 



    def build_footer(self, org: Org):
        r = ui.div( ui.tags.hr(),
                    ui.span( f"copyright 2023 - {org.full_name}" ), 
                   # ui.span( ui.a("Privacy Policy", {"href":"/"} ),
                   #          " --- ",
                   #          ui.a("Terms of Use", {"href":"/"} ) 
                   #        )
                  )
        return r

    def build_main_page(self, org: Org):
        args = [ #{"style": "background-color: rgba(1, 1, 1, 0.1)"},
                 self.theme,
                 self.build_topnav(org),
                 self.build_footer(org)
        ]

        # breakpoint()
        r = ui.page_fluid( *args )
        return r


    def server_entrypoint(self, 
                          input: Inputs, output: Outputs, session: Session,
                          org: Org):
        """
        oabr.module_dict has the registered modules from initialiaztion

        server entrypoint is called on each connection
          input, output, and session is created

        org is set for the connection at hand, which is defined by the route that was matched in the router

        """
        for k,v in self.oabr.module_dict.items():
            v.server_entrypoint(input, output, session, org)

    def build_app_for_org(self, org: Org):
        mp = self.build_main_page(org)

        from functools import partial
        fn = partial(self.server_entrypoint, org=org)
        r = App(mp,fn)

        return r


