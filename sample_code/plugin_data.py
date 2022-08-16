import figmapy.datatypes
import pprint

plugin_key = '102354890500261289'  # fake plugin key
plugin_name = 'FakePluginName'
file_key = 'REDACTED'
auth_key = 'REDACTED'

figmaPy = figmapy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key, plugin_data=plugin_key)
page1 = file.document.children[0]

for child in page1.children:  # -> FigmaPy.datatypes.nodes.Node
    pprint.pprint(child.sharedPluginData, width=1)
    # None

    pprint.pprint(child.pluginData, width=1)
    # {
    #   '102354890500261289':
    #   {
    #     'FakePluginName':
    #     '{
    #       "export_location":"C:\\\\downloads\\\\",
    #       "ignore":false,
    #       "scale_to_power_of_2":false
    #     }'
    #   }
    # }

    # access the plugin data:
    child.pluginData[plugin_key][plugin_name]
    # '{"export_location":"C:\\\\downloads\\\\",
    #   "ignore":false,
    #   "scale_to_power_of_2":false
    #  }'
