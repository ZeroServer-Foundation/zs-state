from collections import OrderedDict

from zstate import Runtime
from . import *

from zstate.ext.starlette import StarletteRouter,TestMountable
from zstate.ext.starlette.auth import AuthMountablePlugin
from zstate.ext.sqlmodel import SqlModelPlugin

pod = OrderedDict()
pod["sqlmodel"] = SqlModelPlugin()
pod["auth"] = AuthMountablePlugin()

l_nav_list = [
    Point("l1",["content l1"]),
    Point("l2",["content l2"]),
        ]

from shiny import ui
r_nav_list = [
    Point("r1",["content r1",ui.output_text("r1")]),
    Point("r2",["content r2"]),
    ]

pod["starlette"] = StarletteRouter(
    mountable_list=[
        TestMountable("/dev"),
        pod["auth"].as_mountable("/authtest"),
        BaseShiny("/shiny",
            root=Point(None,
                [
                    Point("topnav/left", l_nav_list),
                    Point("topnav/right", r_nav_list)
                ]
            )
        )
    ]
)

rt = Runtime(plugin_ordereddict=pod)
s = rt.plugin_ordereddict["starlette"]
s.run()

import uvicorn
if __name__ == "__main__":
    breakpoint()
    uvicorn.run(s.app, host="0.0.0.0", port=8300, log_level="debug")



