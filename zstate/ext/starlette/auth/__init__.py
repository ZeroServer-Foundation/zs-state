from dataclasses import dataclass

from starlette.routing import Route,Mount
from starlette.middleware import Middleware
from starlette.responses import Response,RedirectResponse,PlainTextResponse

from zstate import Plugin

from pprint import pformat as pf


class Mountable:
    """

    the point is to on initialization, 

    add to the routes, middleware, etc.

    so each plugin should be called in order and have a chance to modify those 

    """

    def process_setup(self,
                      route_list: list,
                      middleware_list: list,
                      data: dict) -> None:
        pass

    def __call__(self,*args,**kwargs):
        pass



@dataclass
class AuthPlugin(Plugin):

    def __post_init__(self):
        pass

    def process_setup(self,
                      route_list: list,
                      middleware_list: list,
                      data: dict) -> None:
       
        modL = [ 
            ("/basic_auth",  self.init_auth_basic,), 
            ("/authlib1",    self.init_auth_authlib1,), 
        ]
        for m in modL:
            prefix, target_fn = m 
            rL, m_args, m_kwargs = target_fn(prefix)

            mnt = Mount( prefix, routes=rL )
            route_list.append( mnt )
            middleware_list.append( Middleware( *m_args, **m_kwargs ) )

            # breakpoint()

    def init_auth_basic(self,prefix):
        from starlette.authentication import (
            AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
        )
        from starlette.middleware.authentication import AuthenticationMiddleware
        import base64
        import binascii

        class BasicAuthBackend(AuthenticationBackend):
            async def authenticate(self, conn):
                if "Authorization" not in conn.headers:
                    return

                auth = conn.headers["Authorization"]
                try:
                    scheme, credentials = auth.split()
                    if scheme.lower() != 'basic':
                        return
                    decoded = base64.b64decode(credentials).decode("ascii")
                except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
                    raise AuthenticationError('Invalid basic auth credentials')

                username, _, password = decoded.partition(":")
                # TODO: You'd want to verify the username and password here.
                return AuthCredentials(["authenticated"]), SimpleUser(username)


        async def homepage(request):
            if request.user.is_authenticated:
                return PlainTextResponse('Hello, ' + request.user.display_name)
            return PlainTextResponse('Hello, you')

        rL = [
            Route("/", endpoint=homepage)
        ]

        return rL, [ AuthenticationMiddleware ], {"backend": BasicAuthBackend()}

    def init_auth_authlib1(self,prefix):
        async def check(request):
            """
            Check if we are in session.
            """
            content = f"""
                <html>
                <title>starlette authlib demo</title>
                <body>
                    your status is: %(status)s, click here to <a href="/%(action)s">%(action)s</a>
                
                <pre>
                { pf(locals()) }
                </pre>
                </body></html>
            """
            if not request.session.get("user"):
                return Response(
                    content % {"status": "logged out", "action": "login"},
                    headers={"content-type": "text/html"},
                    status_code=401,
                )
            # dbp(1)
            return Response(content % {"status": "logged in", "action": "logout"})


        async def login(request):
            """
            A login endpoint that creates a session.
            """
            request.session.update(
                {
                    "iss": "myself",
                    "user": "username",
                }
            )
            # return RedirectResponse(url=request.url_for("check"))
            return RedirectResponse(url=prefix)


        async def logout(request):
            """
            A login endpoint that creates a session.
            """
            request.session.clear()
            return RedirectResponse(url=prefix)


        routes = [  # pylint: disable=invalid-name
            Route("/", endpoint=check, name="check"),
            Route("/login", endpoint=login),
            Route("/logout", endpoint=logout),
        ]


        from starlette.config import Config
        from starlette.datastructures import Secret
        from starlette_authlib.middleware import (
            AuthlibMiddleware as SessionMiddleware,
            SecretKey,
        )

        config = Config(".env") 

        if True or JWT_ALG.startswith("HS"):
            secret_key = config(  # pylint: disable=invalid-name
                "JWT_SECRET", cast=Secret, default="secret"
            )
        else:
            if JWT_ALG.startswith("RS"):
                private_key = open(  # pylint: disable=invalid-name
                    os.path.join(KEYS_DIR, "rsa.key")
                ).read()

                public_key = open(  # pylint: disable=invalid-name
                    os.path.join(KEYS_DIR, "rsa.pub")
                ).read()

            elif JWT_ALG.startswith("ES"):
                private_key = open(  # pylint: disable=invalid-name
                    os.path.join(KEYS_DIR, "ec.key")
                ).read()

                public_key = open(  # pylint: disable=invalid-name
                    os.path.join(KEYS_DIR, "ec.pub")
                ).read()

            ## WIP: can't find a proper way to generate them

            #     elif JWT_ALG.startswith("PS"):
            #
            #         private_key = open(  # pylint: disable=invalid-name
            #             os.path.join(KEYS_DIR, "ps.key")
            #         ).read()
            #
            #         public_key = open(  # pylint: disable=invalid-name
            #             os.path.join(KEYS_DIR, "ps.pub")
            #         ).read()
    
            secret_key = SecretKey(  # pylint: disable=invalid-name
                Secret(private_key), Secret(public_key)
            )

        return routes, [ SessionMiddleware ], {"secret_key": secret_key}


