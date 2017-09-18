require.undef('fileview');

window.inputElement = undefined;

function Size(width, height, maxWidth, maxHeight) {
    var ratio = (width <= maxWidth && height <= maxHeight) ? 1 : Math.min(maxWidth / width, maxHeight / height)
    this.width = Math.round(width * ratio)
    this.height = Math.round(height * ratio)
    
}

define('fileview', ["jupyter-js-widgets"], function(widgets) {

    var FileView = widgets.DOMWidgetView.extend({
        render: function() {
            inputField = document.createElement("input");
            inputField.type = "file";
            canvas = document.createElement("canvas");
            canvasContainer = document.createElement("div");
            canvasContainer.appendChild(canvas)
            context = canvas.getContext("2d");
            this.el.innerHTML = "";
            this.el.appendChild(inputField);
            this.el.appendChild(canvasContainer);
            inputField.onchange = function(evt) {
                var tgt = evt.target || window.event.srcElement
                var files = tgt.files;
                if (!(FileReader && files && files.length > 0)) { return; }
                var fr = new FileReader();
                fr.onload = function() {
                    data_url = fr.result;
                    this.model.set("data_url", data_url)
                    this.touch();
                    var image = new Image;
                    image.src = data_url;
                    image.onload = function() {
                        size = new Size(image.naturalWidth, image.naturalHeight, 200, 200)
                        canvas.width = size.width;
                        canvas.height = size.height;
                        context.drawImage(image, 0, 0, size.width, size.height);
                    }.bind(this);
                }.bind(this);
                fr.readAsDataURL(files[0]);
            }.bind(this);
        }
    });

    return {
        FileView: FileView
    }
});