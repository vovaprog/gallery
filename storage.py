import os
import Image
import re
import urllib

from settings import settings


def gallery_page_data(parameters):
    albums = get_albums()
    
    output_albums = []
    
    for album in albums:
        cover = get_cover_name(album)
        if cover is not None:
            check_and_create_preview(album,cover,settings["gallery_preview_width"])
                
        output_albums.append({
            'name':album,
            'link': get_album_url(album,parameters=parameters),
            'cover_url':get_preview_url(album,cover,settings['gallery_preview_width'])
        })
    
    return {
        'albums' : output_albums        
    }
    
    
def album_page_data(album_name, page_number, parameters):    
    check_name(album_name)
    
    view = get_parameter(parameters,'album-view')    
    
    page_image_count = settings['album_'+view+'_page_image_count']
    
    images = get_album_images(album_name)
    
    #=================================================================
            
    start_index = page_image_count * page_number
    end_index = start_index + page_image_count
    
    if start_index >= len(images):
        if len(images) % page_image_count != 0:
            start_index=len(images) - len(images) % page_image_count
        else:
            start_index=len(images) - page_image_count        
    
    if end_index >= len(images):
        end_index = len(images)

    if start_index>0:
        previous_link = get_album_url(album_name,page_number-1,parameters=parameters)
    else:
        previous_link=None
        
    if end_index< len(images):
        next_link = get_album_url(album_name,page_number+1,parameters=parameters)
    else:
        next_link=None

    images = images[start_index:end_index]
        
    #=================================================================    
    
    output_images = []
    
    width=settings["album_"+view+"_preview_width"]
    for img in images:
        check_and_create_preview(album_name,img,width)
        
        image_link= get_image_url(album_name=album_name,image_name=img,parameters=parameters)
        
        output_images.append({
            'image_source':get_preview_url(album_name,img,width),
            'image_link':image_link,
            'name':img
        })

    gallery_link = get_gallery_url(parameters = parameters,album_name = album_name)

    parameters['album-view']="1"
    album_view_1cols_link=get_album_url(album_name,page_number,parameters=parameters)
    parameters['album-view']="2"
    album_view_2cols_link=get_album_url(album_name,page_number,parameters=parameters)
    parameters['album-view']="3"
    album_view_3cols_link=get_album_url(album_name,page_number,parameters=parameters)

    return {
        'album_name' : album_name,
        'images' : output_images, 
        'previous_link' : previous_link,
        'next_link' : next_link,
        'gallery_link' : gallery_link,
        'columns' : int(view),
        'album_view_1cols_link' : album_view_1cols_link,
        'album_view_2cols_link' : album_view_2cols_link,
        'album_view_3cols_link' : album_view_3cols_link,
    }        


def image_page_data(album_name,image_name,parameters):
    check_name(album_name)
    check_name(image_name)

    width = settings["image_preview_width"]
    check_and_create_preview(album_name,image_name,width)

    #=================================================================

    album_view = get_parameter(parameters,"album-view")    
    album_page_image_count = settings['album_'+album_view+'_page_image_count']

    images = get_album_images(album_name)
    
    try:
        image_index = images.index(image_name)
    except:
        image_index = 0

    page_number = image_index / album_page_image_count

    #=================================================================

    if image_index > 0:
        previous_image_link = get_image_url(album_name,images[image_index-1],parameters=parameters)
    else:
        previous_image_link = None
        
    if image_index < len(images) - 1:
        next_image_link = get_image_url(album_name,images[image_index+1],parameters=parameters)
    else:
        next_image_link = None

    #=================================================================

    return {
        'album_name' : album_name,
        'preview' : get_preview_url(album_name,image_name,width),
        'original' : get_photo_url(album_name,image_name),
        'album_link' : get_album_url(album_name,page_number,image_name,parameters=parameters),
        'previous_image_link' : previous_image_link,
        'next_image_link' : next_image_link
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


#=========================================================================
#=========================================================================
#=========================================================================

def get_gallery_url(parameters,album_name):
    gallery_url = settings["application_url"]
    if settings["application_url"] == "":
        gallery_url = gallery_url + "/"
    gallery_url = append_url_parameters(gallery_url,parameters)
    if album_name:
        gallery_url = gallery_url + "#" + urllib.quote(album_name)
    return gallery_url


def get_preview_url(album,image,width):
    image = replace_extension(image,".png")
    return str.format("{0}/preview_{1}/{2}/{3}",settings['data_url'],width,urllib.quote(album),urllib.quote(image))


def get_photo_url(album,image):
    return str.format("{0}/photo/{1}/{2}",settings['data_url'],urllib.quote(album),urllib.quote(image))


def append_url_parameters(url,parameters):
    if not parameters is None:
        param_string = urllib.urlencode(parameters)
        if param_string:
            url = url+"?"+urllib.urlencode(parameters)         
    return url
    

def get_album_url(album_name,page_number=0,image_name=None,parameters=None):
    album_name = str.format("{0}/album/{1}/{2}",settings["application_url"],urllib.quote(album_name),page_number)

    album_name=append_url_parameters(album_name,parameters)

    if image_name:
        album_name += "#" + urllib.quote(image_name) 

    return album_name


def get_image_url(album_name,image_name,parameters):
    url = str.format("{0}/image/{1}/{2}",settings["application_url"],urllib.quote(album_name),urllib.quote(image_name))
    url = append_url_parameters(url,parameters)
    return url


#=========================================================================
#=========================================================================
#=========================================================================


def replace_extension(file_name,new_extension):
    (root, ext) = os.path.splitext(file_name)
    return root + new_extension
    

def get_preview_file_name(album_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))
    image_name=replace_extension(image_name,".png")
    return os.path.join(preview_folder,album_name,image_name)     
    

def check_and_create_preview(album_name,image_name,width):
    if not check_preview_exists(album_name,image_name,width):
        create_preview(album_name,image_name,width)    
    
    
def check_preview_exists(album_name,image_name,width):
    return os.path.isfile(get_preview_file_name(album_name,image_name,width)) 
    
    
def create_preview(album_name,image_name,width):
    preview_folder = os.path.join(settings["data_folder"],"preview_"+str(width))

    if not os.path.isdir(preview_folder):
        os.mkdir(preview_folder)    
    
    preview_album_folder = os.path.join(preview_folder,album_name)
    if not os.path.isdir(preview_album_folder):
        os.mkdir(preview_album_folder)

    photo_name = os.path.join(get_photo_folder(),album_name,image_name)     
    preview_name=get_preview_file_name(album_name,image_name,width)
        
    im = Image.open(photo_name)
    img_width = im.size[0]    
    img_height = im.size[1]
    
    if img_height > img_width:
        width = width * settings["image_height_ratio"] / settings["image_width_ratio"]
    
    im.thumbnail((width,width), Image.ANTIALIAS)
    im.save(preview_name, "PNG")    
    
    
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
    
    
def get_parameter(parameters,parameter_name):
    value = parameters.get(parameter_name)
    if not value is None:
        return value
    else:
        value = settings.get(parameter_name+"-default")
        if not value is None:
            parameters[parameter_name]=value
        return value
    
    