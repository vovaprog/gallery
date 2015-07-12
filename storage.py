import os
import Image
import re

from settings import settings


def gallery_page_data():
    albumns = get_albumns()
    
    output_albumns = []
    
    for albumn in albumns:
        cover = get_cover_name(albumn)
        if cover is not None:
            check_and_create_preview(albumn,cover,settings["gallery_preview_width"])
                
        output_albumns.append({
            'name':albumn,    
            'link':settings['application_url'] +"/albumn/" +albumn,
            'cover_url':get_preview_url(albumn,cover,settings['gallery_preview_width'])
        })
    
    return {
        'albumns' : output_albumns        
    }
    
    
def albumn_page_data(albumn_name, page_number):    
    check_name(albumn_name)
    
    page_size = settings['albumn_page_image_count']
    
    images = get_albumn_images(albumn_name)
    
    #=================================================================
            
    start_index = page_size * page_number
    end_index = start_index + page_size
    
    if start_index >= len(images):
        if len(images) % page_size != 0:
            start_index=len(images) - len(images) % page_size
        else:
            start_index=len(images) - page_size        
    
    if end_index >= len(images):
        end_index = len(images)

    if start_index>0:
        previous_link = get_albumn_url(settings['application_url'],albumn_name,page_number-1)
    else:
        previous_link=None
        
    if end_index< len(images):
        next_link = get_albumn_url(settings['application_url'],albumn_name,page_number+1)
    else:
        next_link=None

    images = images[start_index:end_index]
    
    
    #=================================================================
    
    
    output_images = []
    
    width=settings["albumn_preview_width"]
    for img in images:
        check_and_create_preview(albumn_name,img,width)
        image_link=str.format("{0}/image/{1}/{2}",settings["application_url"],albumn_name,img)
        output_images.append({
            'image_source':get_preview_url(albumn_name,img,width),
            'image_link':image_link,
            'name':img
        })

    if settings["application_url"] == "":
        gallery_link = settings["application_url"] + "/#" + albumn_name
    else:        
        gallery_link = settings["application_url"] + "#" + albumn_name

    return {
        'images' : output_images, 
        'previous_link' : previous_link,
        'next_link' : next_link,
        'gallery_link' : gallery_link
    }        


def image_page_data(albumn_name,image_name):
    check_name(albumn_name)
    check_name(image_name)

    width = settings["image_preview_width"]
    check_and_create_preview(albumn_name,image_name,width)

    #=================================================================

    page_size = settings['albumn_page_image_count']

    images = get_albumn_images(albumn_name)
    
    try:
        image_index = images.index(image_name)
    except:
        image_index = 0

    page_number = image_index / page_size
        
    #=================================================================

    return {
        'preview' : get_preview_url(albumn_name,image_name,width),
        'original' : get_photo_url(albumn_name,image_name),
        'albumn_link' : get_albumn_url(settings['application_url'],albumn_name,page_number,image_name)
    }
        

#=========================================================================
#=========================================================================
#=========================================================================


def get_photo_folder():
    return os.path.join(settings["data_folder"],"photo")


def get_albumns():
    photo_folder = get_photo_folder()
    albumns = os.listdir(photo_folder)    
    albumns = [ albumn for albumn in albumns if os.path.isdir(os.path.join(photo_folder,albumn)) ]    
    return albumns    


def get_albumn_images(albumn_name):
    albumn_folder=os.path.join(get_photo_folder(),albumn_name)
    images = os.listdir(albumn_folder)
    images = [ img for img in images if os.path.isfile(os.path.join(albumn_folder,img)) ]    
    return images    


def check_name(name):    
    if not re.match("^[A-Za-z0-9\\s.\\-_]+$",name) or name.find("..")>=0:                
        raise ValueError("invalid name")


def get_preview_url(albumn,image,width):
    return str.format("{0}/preview_{1}/{2}/{3}",settings['data_url'],width,albumn,image)    


def get_photo_url(albumn,image):
    return str.format("{0}/photo/{1}/{2}",settings['data_url'],albumn,image)


def get_albumn_url(application_url,albumn_name,page_number,image_name=None):
    if image_name is not None:
        return str.format("{0}/albumn/{1}/{2}#{3}",application_url,albumn_name,page_number,image_name)        
    else:    
        return str.format("{0}/albumn/{1}/{2}",application_url,albumn_name,page_number)        


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

    photo_name = os.path.join(get_photo_folder(),albumn_name,image_name) 
    preview_name = os.path.join(preview_albumn_folder,image_name)     
        
    im = Image.open(photo_name)
    im.thumbnail((width,width), Image.ANTIALIAS)
    im.save(preview_name, "JPEG")
    
    
def get_cover_name(albumn_name):        
    files = get_albumn_images(albumn_name)
    
    if len(files) > 0:
        covers = [img for img in files if 'cover' in img]
        if len(covers) > 0:
            cover = covers[0]
        else:
            cover = files[0]
    else:
        cover=None           
    return cover
    
    