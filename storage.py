import os
import Image
import re

from settings import settings


def gallery_page_data():
    albums = get_albums()
    
    output_albums = []
    
    for album in albums:
        cover = get_cover_name(album)
        if cover is not None:
            check_and_create_preview(album,cover,settings["gallery_preview_width"])
                
        output_albums.append({
            'name':album,    
            'link':settings['application_url'] +"/album/" +album,
            'cover_url':get_preview_url(album,cover,settings['gallery_preview_width'])
        })
    
    return {
        'albums' : output_albums        
    }
    
    
def album_page_data(album_name, page_number):    
    check_name(album_name)
    
    page_size = settings['album_page_image_count']
    
    images = get_album_images(album_name)
    
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
        previous_link = get_album_url(settings['application_url'],album_name,page_number-1)
    else:
        previous_link=None
        
    if end_index< len(images):
        next_link = get_album_url(settings['application_url'],album_name,page_number+1)
    else:
        next_link=None

    images = images[start_index:end_index]
    
    
    #=================================================================
    
    
    output_images = []
    
    width=settings["album_preview_width"]
    for img in images:
        check_and_create_preview(album_name,img,width)
        image_link=str.format("{0}/image/{1}/{2}",settings["application_url"],album_name,img)
        output_images.append({
            'image_source':get_preview_url(album_name,img,width),
            'image_link':image_link,
            'name':img
        })

    if settings["application_url"] == "":
        gallery_link = settings["application_url"] + "/#" + album_name
    else:        
        gallery_link = settings["application_url"] + "#" + album_name

    return {
        'album_name' : album_name,
        'images' : output_images, 
        'previous_link' : previous_link,
        'next_link' : next_link,
        'gallery_link' : gallery_link
    }        


def image_page_data(album_name,image_name):
    check_name(album_name)
    check_name(image_name)

    width = settings["image_preview_width"]
    check_and_create_preview(album_name,image_name,width)

    #=================================================================

    page_size = settings['album_page_image_count']

    images = get_album_images(album_name)
    
    try:
        image_index = images.index(image_name)
    except:
        image_index = 0

    page_number = image_index / page_size
        
    #=================================================================

    return {
        'album_name' : album_name,
        'preview' : get_preview_url(album_name,image_name,width),
        'original' : get_photo_url(album_name,image_name),
        'album_link' : get_album_url(settings['application_url'],album_name,page_number,image_name)
    }
        

#=========================================================================
#=========================================================================
#=========================================================================


def get_photo_folder():
    return os.path.join(settings["data_folder"],"photo")


def get_albums():
    photo_folder = get_photo_folder()
    albums = os.listdir(photo_folder)    
    albums = [ album for album in albums if os.path.isdir(os.path.join(photo_folder,album)) ]    
    albums.sort()
    return albums    


def get_album_images(album_name):
    album_folder=os.path.join(get_photo_folder(),album_name)
    images = os.listdir(album_folder)
    images = [ img for img in images if os.path.isfile(os.path.join(album_folder,img)) ]    
    images.sort()
    return images    


def check_name(name):    
    if not re.match("^[A-Za-z0-9\\s.\\-_]+$",name) or name.find("..")>=0:                
        raise ValueError("invalid name")


def get_preview_url(album,image,width):
    return str.format("{0}/preview_{1}/{2}/{3}",settings['data_url'],width,album,image)    


def get_photo_url(album,image):
    return str.format("{0}/photo/{1}/{2}",settings['data_url'],album,image)


def get_album_url(application_url,album_name,page_number,image_name=None):
    if image_name is not None:
        return str.format("{0}/album/{1}/{2}#{3}",application_url,album_name,page_number,image_name)        
    else:    
        return str.format("{0}/album/{1}/{2}",application_url,album_name,page_number)        


def check_and_create_preview(album_name,image_name,width):
    if not check_preview_exists(album_name,image_name,width):
        create_preview(album_name,image_name,width)    
    
    
def check_preview_exists(album_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))
    file_name = os.path.join(preview_folder,album_name,image_name)    
    return os.path.isfile(file_name) 
    
    
def create_preview(album_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))

    if not os.path.isdir(preview_folder):
        os.mkdir(preview_folder)    
    
    preview_album_folder = os.path.join(preview_folder,album_name)
    if not os.path.isdir(preview_album_folder):
        os.mkdir(preview_album_folder)

    photo_name = os.path.join(get_photo_folder(),album_name,image_name) 
    preview_name = os.path.join(preview_album_folder,image_name)     
        
    im = Image.open(photo_name)
    im.thumbnail((width,width), Image.ANTIALIAS)
    im.save(preview_name, "JPEG")
    
    
def get_cover_name(album_name):        
    files = get_album_images(album_name)
    
    if len(files) > 0:
        covers = [img for img in files if 'cover' in img]
        if len(covers) > 0:
            cover = covers[0]
        else:
            cover = files[0]
    else:
        cover=None           
    return cover
    
    