from pprint import pprint as pp


D = True
DL = 3

dev_tagcode = print

def dmsg(*args,**kwargs):
    if D:
        print(args,kwargs)

def dmark(msg=None):
    if D:
        if msg:
            dmsg(msg)
        import traceback
        traceback.print_stack()

def dpp(o):
    if D:
        pp(o)

def dbp(level=5,dev_tagcode=None,start_here=False,do_dmark=False):
    if dev_tagcode:
        print(dev_tagcode)              # notice the double naming

    if start_here:
        print("START_HERE")
        breakpoint()

    if D:
        if do_dmark:
            dmark("dbp")
        if level < DL:
            breakpoint()



dlog = dmsg


