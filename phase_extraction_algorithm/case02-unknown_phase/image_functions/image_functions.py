from PIL import Image
from numpy import array, zeros
from itertools import product

def import_image(filename):
    img = Image.open(filename).convert('L')
    return array(img)

#def cut_black(image):

def show_image(image, image_type='L'):
    Image.fromarray(image).convert(image_type).show()

def subtract_background(image, bg):
    return sub_arr(image, bg)

def sub_arr(img1, img2):
    dimensions = img1.shape
    diff = zeros(dimensions)
    
    for i, j in product(range(dimensions[0]), range(dimensions[1])):
        diff[i][j] = sub_pixel(img1[i][j], img2[i][j])

    return diff

def sub_pixel(pixel1, pixel2):
    if pixel2 >= pixel1: return 0
    return pixel1 - pixel2

def save_image(img, name, image_type='L'):
    Image.fromarray(img).convert(image_type).save(name)
