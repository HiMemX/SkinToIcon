import PIL
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import helpers
import math
from multiprocessing import Pool
import scipy.ndimage

def png_to_rgb(path):
    image = plt.imread(path)[:,:,:4]
    new_image = []
    for y in image:
        new_image.append([])
        for x in y:
            new_image[-1].append((int(x[0]*255), int(x[1]*255), int(x[2]*255), int(x[3]*255)))
            
    return new_image

def rgb_to_png(rgb, path, name, mode):
    rgbarray = []
    rgbarray = np.array([np.array([x for x in i], np.uint8) for i in rgb], np.uint8)
    rgbimage = PIL.Image.fromarray(rgbarray, "RGBA")
        
    rgbimage.save(path+f"/{name}.{mode}")
    
def scale_rgb(rgb, factorx, factory):
    return [[rgb[math.floor(array)][math.floor(element)] for element in helpers.floatrange(0, len(rgb[math.floor(array)]), 1/factorx)] for array in helpers.floatrange(0, len(rgb), 1/factory)]

def clamp_rgb_size(rgb, pixelx, pixely):
    side_padding_len = int((pixelx-len(rgb[0]))/2)
    top_padding_len = int((pixely-len(rgb))/2)
    new_rgb = []
    
    rgb = [[(0, 0, 0, 0) for i in range(len(rgb[0]))] for padd in range(top_padding_len)] + rgb + [[(0, 0, 0, 0) for i in range(len(rgb[0]))] for padd in range(top_padding_len)]
    
    for array in range(len(rgb)):
        new_rgb.append([(0, 0, 0, 0) for i in range(side_padding_len)] + rgb[array] + [(0, 0, 0, 0) for i in range(side_padding_len)])
        
    return new_rgb
    
def rgb_to_ba(rgb, alpha):
    return [[[0,0,0,math.ceil(pixel[3]/255)*alpha] for pixel in array] for array in rgb]

def filter_channel(rgb, channel):
    output = []
    for row in rgb:
        output.append([])
        for pixel in row:
            output[-1].append(pixel[channel])
    return output

def blur_rgb(rgb, pixels):
    r = filter_channel(rgb, 0)
    g = filter_channel(rgb, 1)
    b = filter_channel(rgb, 2)
    a = filter_channel(rgb, 3)
    
    r = scipy.ndimage.gaussian_filter(r, sigma=pixels)
    g = scipy.ndimage.gaussian_filter(g, sigma=pixels)
    b = scipy.ndimage.gaussian_filter(b, sigma=pixels)
    a = scipy.ndimage.gaussian_filter(a, sigma=pixels)
    
    return [[[r[y][x], g[y][x], b[y][x], a[y][x]] for x in range(len(rgb[0]))] for y in range(len(rgb))]

def alpha_blend(final, rgb):
    for y in range(len(final)):
        for x in range(len(final[y])):
            combined_alpha = rgb[y][x][3]/255 + (1-rgb[y][x][3]/255)*final[y][x][3]/255
            final[y][x] = helpers.listadd(helpers.listmul(rgb[y][x][:3], rgb[y][x][3]/255), helpers.listmul(final[y][x][:3], 1-rgb[y][x][3]/255)) + [combined_alpha*255]

    return final
    
def combine_rgb(rgbs):
    final = rgbs[0]
    
    for rgb in rgbs[1:]:
        final = alpha_blend(final, rgb)
                
    return final