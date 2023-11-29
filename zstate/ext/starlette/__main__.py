import fire

from orgstar import OrgGroup,OabRouter,AuthPlugin

og = OrgGroup.get_instance()

mapping = {
        'dev1.dataasset.store': og['mdam']
        }

from nowkast.shiny import ShinyWrapper
module_dict = { 'nk': ShinyWrapper.get_instance()
              }

plugin_list = [ AuthPlugin() ]

oabr = OabRouter(orggroup=og,
                 mapping=mapping,
                 module_dict=module_dict,
                 plugin_list=plugin_list)
oabr.run()                                    # oabr.app is only set after run is called

app = oabr.app


if __name__ == '__main__':
      fire.Fire()


