from . import *

from zstate.ext.sqlmodel import SqlModelPlugin
from zstate.ext.starlette import StarletteRouter,Mountable
from zstate.ext.starlette.auth import AuthPlugin

pod = OrderedDict()
pod["sqlmodel"] = SqlModelPlugin()
pod["auth"] = AuthPlugin()
pod["starlette"] = StarletteRouter(
    mountable_list=[
        Mountable("/dev", None),
        Mountable("/authtest", None),
    ]
)

rt = Runtime(plugin_ordereddict=pod)
