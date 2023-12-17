from zstate import Plugin

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession



def dc(cls):
    return cls



class Storable:
    """

    something that represents a set of classes that are to be stored in tables

    sort of like a subplugin, similar to the Mountable construct for StarletteRouter

    !! we should be able to parse the __annotations__ and grab all of the schema info from there

    """
    pass


@dc 
class StorablePlugin(Plugin):

    sqlmodel_plugin_key: str
    sqlmodel_storable_class_list: list

    sqlmodel_table_prefix: str = ""

    def classname_to_tablename(self,classname):
        return f"{self.sqlmodel_table_predix}{classname}"

    def tablename_to_classname(self,tablename):
        r = tablename[len(self.sqlmodel_table_prefix):]
        return r


    def _on_registered_with_runtime(self,runtime,*args,**kwargs):
        Plugin._on_registered_with_runtime(self,runtime,*args,**kwargs)
        self.sqlmodel = self.registered_runtime.plugin_ordereddict["sqlmodel_plugin_key"]
        dbp(1,pf(self.sqlmodel))      


@dc
class SqlModelPlugin(Plugin):

    sql_url: str = "sqlite+aiosqlite:///database.db"

    def __post_init__(self):
        self.engine = create_async_engine(self.sql_url, echo=True) 

    def get_sm_session(self):
        r = AsyncSession(self.engine)
        self.last_session = r
        return r

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session() -> AsyncSession:
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session

@dc
class SqlModelSyncPlugin(Plugin):
    """

    since SqlAlchemy is available in Pyodide, it makes sense to think about having the underlying backend proxied over ZeroServer Data Mesh, 
    
    but in a way that allows SqlLite to be replaced by proxied, layered, copy-on-wriite, distribution, sync, and other tricks to be used on the underlying binary file

    and then to allow that to be transparently replaced by a real DB backend like PostgreSQL

    perhaps something that listens triggers at the SQL layer and then sends them to a Pubsub?

    """
    pass

