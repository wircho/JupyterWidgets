from ipywidgets import *
from IPython.display import display, HTML
import json

def print_title(string):
    middle = "|   " + string + "   |"
    l = len(middle)
    top = "-" * l
    print(top)
    print(middle)
    print(top)

class WidgetInfo:
    def __init__(self, data):
        if isinstance(data, DOMWidget):
            self.widget = data
            self.default_name = None
            self.default_value = None
            return
        self.widget = None
        self.default_name = None
        self.default_value = data
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], DOMWidget):
                    self.widget = data[key]
                    self.default_name = key
                    self.default_value = None
                else:
                    self.widget = None
                    self.default_name = key
                    self.default_value = data[key]

    def value(self):
        if not(self.default_value is None):
            return self.default_value
        if not(self.widget is None):
            return self.widget.value
        return None

    def name(self):
        if not(self.default_name is None): return self.default_name
        if not(self.default_value is None): return "Some " + type(self.default_value).__name__
        if self.widget is None: return "(Unknown)"
        if isinstance(self.widget, IntSlider): return "Some Int"
        if isinstance(self.widget, FloatSlider): return "Some Float"
        if isinstance(self.widget, ToggleButton): return "Some Bool"
        if isinstance(self.widget, Text): return "Some String"
        return "(Widget)"
    

def bind(widgets, function):
    infos = [WidgetInfo(widget) for widget in widgets]

    for info in infos:
        if info.widget is None:
            display(HBox([Label(value = info.name() + ": ", align="right"), Label(value = json.dumps(info.value()))]))
        else:
            display(HBox([Label(value = info.name() + ": ", align="right"), info.widget]))

    button = Button(description = "Run " + function.__name__)
    display(button)

    def press(button):
        print_title("Running " +  function.__name__ + " with parameters: (" + ", ".join(json.dumps(info.value()) for info in infos) + ")")

        for info in infos:
            if not(info.widget is None): info.widget.disabled = True

        function(*[info.value() for info in infos])

        for info in infos:
            if not(info.widget is None): info.widget.disabled = False

    button.on_click(press)