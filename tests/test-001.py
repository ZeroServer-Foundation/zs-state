import asyncio

import pytest

from nowkast import *

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def create_nkr(): 
    r = Runtime.get_instance()

    return r

@pytest.mark.asyncio
async def test_rank_001(create_nkr):
    """create a simple rank, populate, and run a sample
  
    """
    nkr = create_nkr


    if True:
        await nkr.init_db()
        s = nkr.get_sm_session()

        for j in [ nkr.gen_users(), nkr.gen_realms() ]:
            for i in j:
                # breakpoint()
                s.add(i)

        breakpoint()
        await s.commit()



@pytest.mark.asyncio
async def test_simple():
        await asyncio.sleep(0.5)
