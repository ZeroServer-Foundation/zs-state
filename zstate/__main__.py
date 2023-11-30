from . import *

from .ext.sqlmodel import SqlModelPlugin
from .ext.starlette import StarletteRouter
from .ext.starlette.auth import AuthPlugin

pod = OrderedDict()
pod["sqlmodel"] = SqlModelPlugin()
pod["auth"] = AuthPlugin()
pod["starlette"] = StarletteRouter()

rt = Runtime(plugin_ordereddict=pod)
