from IPython.display import display, HTML
import ipywidgets as widgets
from traitlets import Unicode, validate
from base64 import decodestring

class FileWidget(widgets.DOMWidget):
    _view_name = Unicode('FileView').tag(sync=True)
    _view_module = Unicode('fileview').tag(sync=True)
    data_url = Unicode('').tag(sync=True)

display(HTML("<script src=\"file_widget.js\"></script>"))

def save_data_url(data_url, path):
	file = open(path, "wb")
	string = data_url.split(",")[1].encode()
	file.write(decodestring(string))
	file.close()

def changed_data(change):
	path = "data_url_image.jpg"
	save_data_url(change.new, path)
	print("Saved image to path: {}".format(path))

file_widget = FileWidget()
display(file_widget)
file_widget.observe(changed_data, names=["data_url"])