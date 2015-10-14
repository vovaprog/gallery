from flask import Flask
from flask import render_template
from flask import request
import urllib

from storage import gallery_page_data, album_page_data, image_page_data
from settings import settings

if __name__ == "__main__":
    app = Flask(__name__, static_folder='data', static_url_path='/data')
else:    
    app = Flask(__name__)

@app.route("/")
def gallery_page(): 
    return render_template('gallery.html', 
        data=gallery_page_data(),
        settings=settings)


@app.route("/album/<album_name>",defaults={'page_number':0})
@app.route("/album/<album_name>/<int:page_number>")
def album_page(album_name,page_number):
    album_name = urllib.unquote(album_name)
    view = request.args.get('album-view')

    template_name=None
    if view == "2" or view == "3":
        template_name='album_column_view.html'
    else:
        view = "1"
        template_name='album.html'

    return render_template(template_name, 
        data=album_page_data(album_name,view,page_number),        
        settings=settings)


@app.route("/image/<album_name>/<image_name>")
def image_page(album_name,image_name):
    album_name = urllib.unquote(album_name)
    image_name = urllib.unquote(image_name)
    
    return render_template('image.html',
        data=image_page_data(album_name,image_name),
        settings=settings)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

