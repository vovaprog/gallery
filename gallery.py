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


gallery_route = settings["application_route_url"]
if gallery_route == "":
    gallery_route = "/"


@app.route(gallery_route)
def gallery_page(): 
    return render_template('gallery.html', 
        data=gallery_page_data(request.args.copy()),
        settings=settings)


@app.route(settings["application_route_url"] + "/album/<album_name>",defaults={'page_number':0})
@app.route(settings["application_route_url"] + "/album/<album_name>/<page_number>")
def album_page(album_name,page_number):
    album_name = urllib.unquote(album_name)
    page_number = int(page_number)

    return render_template('album.html', 
        data=album_page_data(album_name,page_number,request.args.copy()),        
        settings=settings)


@app.route(settings["application_route_url"] + "/image/<album_name>/<image_name>")
def image_page(album_name,image_name):
    album_name = urllib.unquote(album_name)
    image_name = urllib.unquote(image_name)
    
    return render_template('image.html',
        data=image_page_data(album_name,image_name,request.args.copy()),
        settings=settings)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')    
    

