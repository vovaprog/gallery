from flask import Flask
from flask import render_template

from storage import gallery_page_data, albumn_page_data, image_page_data
from settings import settings

if __name__ == "__main__":
    #app = Flask(__name__, static_folder='data', static_url_path='/data')
    app = Flask(__name__, static_folder='C:\\Share\\foto_test', static_url_path='/data')
else:    
    app = Flask(__name__)

@app.route("/")
def gallery_page(): 
    return render_template('gallery.html', 
        albumns=gallery_page_data(),
        settings=settings)


@app.route("/albumn/<albumn_name>",defaults={'page_number':0})
@app.route("/albumn/<albumn_name>/<int:page_number>")
def albumn_page(albumn_name,page_number):
    return render_template('albumn.html', 
        data=albumn_page_data(albumn_name,page_number),
        gallery_link=settings["application_url"] + "/",
        settings=settings)


@app.route("/image/<albumn_name>/<image_name>")
def image_page(albumn_name,image_name):
    return render_template('image.html', 
        image=image_page_data(albumn_name,image_name),
        albumn_link=settings['application_url']+"/albumn/"+albumn_name,
        settings=settings)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

