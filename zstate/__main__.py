from . import *

from .ext.sqlmodel import SqlModelPlugin
from .ext.starlette import StarletteRouter,Mountable
from .ext.starlette.auth import AuthPlugin

pod = OrderedDict()
pod["sqlmodel"] = SqlModelPlugin()
pod["auth"] = AuthPlugin()
pod["starlette"] = StarletteRouter(
    mountable_list=[
        Mountable("/dev", None),
        Mountable("/authtest", None),
        Mountable("/das", og.build_app_for_org(das)),
        Mountable("/mdam", og.build_app_for_org(mdam)),
    ]
)


rt = Runtime(plugin_ordereddict=pod)
