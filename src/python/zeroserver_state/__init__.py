class PubSubEventType(Enum):
    

class NotificationHandler:

    await def handle_pubsub(self,
        pubsub_key: str,
        pubsub_event_type: PubSubEventType,
        pubsub_data: dict) -> None: pass


class StateHandle:
    """

    messaging encryption, underlying backend (Supabase, Ethereum, etc.) and setup (login, auth, password, etc.) should be abstrcated behind this class, such that once an app has an initialized version of this object, it is assumed that everything needed to set that up has already magically happened in the backgroun

    in this system, there is only pubsub.  a messaging setup is just a two party pubsub

    """


    await def block_read(self,position,length) -> byte[]: pass
    await def block_write(self,position,length,data) -> None: pass

    await def pubsub_send(self,pubsub_key,data,callback_fn) -> None: pass
    await def pubsub_subscribe(self,
        pubsub_key: str,
        notification_handler: NotificationHandler) -> None: pass

    await def pubsub_unsubscribe(self,
        pubsub_key: str,
        notification_handler: NotificationHandler) -> None: pass

    await def get_local_kvstore(self) -> dict: 
        """used to get the local version of the key-value store used for things like data that needs to go into the UI
        because the dict does not have a notification mechansim, a Pubsub should be used instead of polling to notify when to process new information
        """
        pass

class RpcOverPubsub: 
    """

    """
    pass


class SqlModelSync:
    """

    since SqlAlchemy is available in Pyodide, it makes sense to think about having the underlying backend proxied over ZeroServer Data Mesh, 
    
    but in a way that allows SqlLite to be replaced by proxied, layered, copy-on-wriite, distribution, sync, and other tricks to be used on the underlying binary file

    and then to allow that to be transparently replaced by a real DB backend like PostgreSQL

    """
    pass
