import os
import Image
import re

from settings import settings

photo_folder = os.path.join(settings["data_folder"],"photo")

def gallery_page_data():
    albumns = os.listdir(photo_folder)
    
    output = []
    
    for albumn in albumns:
        cover = get_cover_name(albumn)
        if cover is not None:
            check_and_create_preview(albumn,cover,settings["gallery_preview_width"])
                
        output.append({
            'name':albumn,    
            'link':settings['application_url'] +"/albumn/" +albumn,
            'cover_url':get_preview_url(albumn,cover,settings['gallery_preview_width'])
        })
    
    return output
    
    
def albumn_page_data(albumn_name, page_number):    
    check_name(albumn_name)
    
    albumn_folder=os.path.join(photo_folder,albumn_name)
    images = os.listdir(albumn_folder)
    images = [ img for img in images if os.path.isfile(os.path.join(albumn_folder,img)) ]
    
    page_size = settings['albumn_page_image_count']
    
    max_pages = len(images) / page_size
    if len(images) % page_size !=0:
        max_pages += 1
    
    #=================================================================
            
    start_index = page_size * page_number
    end_index = start_index + page_size
    
    if start_index >= len(images):
        start_index=len(images) - len(images) % page_size 
    
    if end_index >= len(images):
        end_index = len(images)

    if start_index>0:
        previous_link = str.format("{0}/albumn/{1}/{2}",settings['application_url'],albumn_name,page_number-1)
    else:
        previous_link=None
        
    if end_index< len(images):
        next_link = str.format("{0}/albumn/{1}/{2}",settings['application_url'],albumn_name,page_number+1)
    else:
        next_link=None

    images = images[start_index:end_index]
    
    #=================================================================
    
    pages = []
    
    for i in range(max(0,page_number-2),min(page_number+3,max_pages)):
        if i != page_number:
            link = str.format("{0}/albumn/{1}/{2}",settings['application_url'],albumn_name,i)
        else:
            link = None
        
        pages.append({'number':i, 'link':link})
        
    #=================================================================
    
    
    output_images = []
    
    width=settings["albumn_preview_width"]
    for img in images:
        check_and_create_preview(albumn_name,img,width)
        image_link=str.format("{0}/image/{1}/{2}",settings["application_url"],albumn_name,img)
        output_images.append({'image_source':get_preview_url(albumn_name,img,width),'image_link':image_link})
        
    output = {
        'images':output_images, 
        'pages':pages,
        'previous_link':previous_link,
        'next_link':next_link
    }        
        
    return output


def image_page_data(albumn_name,image_name):
    check_name(albumn_name)
    check_name(image_name)

    width = settings["image_preview_width"]
    check_and_create_preview(albumn_name,image_name,width)

    output = {}

    return {'preview' : get_preview_url(albumn_name,image_name,width),
        'original' : get_photo_url(albumn_name,image_name) }
        

#=========================================================================
#=========================================================================
#=========================================================================

def check_name(name):    
    if not re.match("^[A-Za-z0-9\\s.\\-_]+$",name) or name.find("..")>=0:                
        raise ValueError("invalid name")


def get_preview_url(albumn,image,width):
    return str.format("{0}/preview_{1}/{2}/{3}",settings['data_url'],width,albumn,image)    

def get_photo_url(albumn,image):
    return str.format("{0}/photo/{1}/{2}",settings['data_url'],albumn,image)

def check_and_create_preview(albumn_name,image_name,width):
    if not check_preview_exists(albumn_name,image_name,width):
        create_preview(albumn_name,image_name,width)    
    
    
def check_preview_exists(albumn_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))
    file_name = os.path.join(preview_folder,albumn_name,image_name)    
    return os.path.isfile(file_name) 
    
    
def create_preview(albumn_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))

    if not os.path.isdir(preview_folder):
        os.mkdir(preview_folder)    
    
    preview_albumn_folder = os.path.join(preview_folder,albumn_name)
    if not os.path.isdir(preview_albumn_folder):
        os.mkdir(preview_albumn_folder)

    photo_name = os.path.join(photo_folder,albumn_name,image_name) 
    preview_name = os.path.join(preview_albumn_folder,image_name)     
        
    im = Image.open(photo_name)
    im.thumbnail((width,width), Image.ANTIALIAS)
    im.save(preview_name, "JPEG")
    
    
def get_cover_name(albumn_name):
    print albumn_name
    files = os.listdir(os.path.join(photo_folder,albumn_name))    
    if len(files) > 0:
        covers = [img for img in files if img.startswith('cover')]
        if len(covers) > 0:
            cover = covers[0]
        else:
            cover = files[0]
    else:
        cover=None           
    return cover
    