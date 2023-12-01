from collections import OrderedDict

from zstate import Runtime
from . import *

from zstate.ext.starlette.auth import AuthMountablePlugin
from zstate.ext.sqlmodel import SqlModelPlugin

pod = OrderedDict()
pod["sqlmodel"] = SqlModelPlugin()
pod["auth"] = AuthMountablePlugin()
pod["starlette"] = StarletteRouter(
    mountable_list=[
        TestMountable("/dev"),
        TestMountable("/authtest"),
        pod["auth"].as_mountable("/auth")
    ]
)

rt = Runtime(plugin_ordereddict=pod)
s = rt.plugin_ordereddict["starlette"]
s.run()

import uvicorn
if __name__ == "__main__":
    breakpoint()
    uvicorn.run(s.app, host="0.0.0.0", port=8300, log_level="debug")



