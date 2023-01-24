# Workaround script for pause operation on Creality-flavor Marlin firmware
# Original script from DisplayFilenameAndLayerOnLCD.py by Amanda de Castilho (2018)
# Released under the terms of the LGPLv3 or higher.

from ..Script import Script
from UM.Application import Application

class DisplayLayerCR(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Display Layer (CR-Marlin)",
            "key": "DisplayLayerCR",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "scroll":
                {
                    "label": "Scroll enabled/Small layers?",
                    "description": "If SCROLL_LONG_FILENAMES is enabled select this setting however, if the model is small disable this setting!",
                    "type": "bool",
                    "default_value": false
                },
                "name":
                {
                    "label": "Text to display:",
                    "description": "By default the current filename will be displayed on the LCD. Enter text here to override the filename and display something else.",
                    "type": "str",
                    "default_value": ""
                },
                "startNum":
                {
                    "label": "Initial layer number:",
                    "description": "Choose which number you prefer for the initial layer, 0 or 1",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 1                    
                },
                "maxlayer":
                {
                    "label": "Display max layer?:",
                    "description": "Display how many layers are in the entire print on status bar?",
                    "type": "bool",
                    "default_value": true
                }
            }
        }"""

    def execute(self, data):
        max_layer = 0
        if self.getSettingValueByKey("name") != "":
            name = self.getSettingValueByKey("name")
        else:
            name = Application.getInstance().getPrintInformation().jobName
        if not self.getSettingValueByKey("scroll"):
            if self.getSettingValueByKey("maxlayer"):
                lcd_text = "M117 Layer "
            else:
                lcd_text = "M117 Printing Layer "
        else:
            lcd_text = "M117 Printing " + name + " - Layer "
        i = self.getSettingValueByKey("startNum")
        for layer in data:
            display_text = lcd_text + str(i)
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER_COUNT:"):
                    max_layer = line
                    max_layer = max_layer.split(":")[1]
                    if self.getSettingValueByKey("startNum") == 0:
                        max_layer = str(int(max_layer) - 1)
                if line.startswith(";LAYER:"):
                    if self.getSettingValueByKey("maxlayer"):
                        display_text = display_text + " of " + max_layer
                        if not self.getSettingValueByKey("scroll"):
                            display_text = display_text + " " + name
                    else:
                        if not self.getSettingValueByKey("scroll"):
                            display_text = display_text + " " + name + "!"
                        else:
                            display_text = display_text + "!"
                    line_index = lines.index(line)
                    lines.insert(line_index + 1, display_text)
                    i += 1
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines

        return data
