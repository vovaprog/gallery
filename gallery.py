from flask import Flask
from flask import render_template

from storage import gallery_page_data, album_page_data, image_page_data
from settings import settings

if __name__ == "__main__":
    app = Flask(__name__, static_folder='data', static_url_path='/data')
    #app = Flask(__name__, static_folder='C:\\Share\\foto_test', static_url_path='/data')
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
    return render_template('album.html', 
        data=album_page_data(album_name,page_number),        
        settings=settings)


@app.route("/image/<album_name>/<image_name>")
def image_page(album_name,image_name):     
    return render_template('image.html',
        data=image_page_data(album_name,image_name),
        settings=settings)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

