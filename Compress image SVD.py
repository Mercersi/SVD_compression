import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image
import time

from ipywidgets import interact, interactive, interact_manual
import ipywidgets as widgets
from IPython.display import display

images = {
    "Final": np.asarray(Image.open('edir.jpg'))
}

def show_images(img_name):
    'It will show image in widgets'
    print("Loading...")
    plt.title("Close this plot to open compressed image...")
    plt.imshow(images[img_name])
    plt.axis('off')
    plt.show()

show_images('Final')

compressed_image = None

def compress_image(img_name, k):

    start_time = time.time()
    
    global compressed_image
    img = images[img_name]
    
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    
    
    ur,sr,vr = svd(r, full_matrices=False)
    ug,sg,vg = svd(g, full_matrices=False)
    ub,sb,vb = svd(b, full_matrices=False)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sb[:k]), vb[:k,:]))
    
    
    rimg = np.zeros(img.shape)
    rimg[:,:,0] = rr
    rimg[:,:,1] = rg
    rimg[:,:,2] = rb
    
    for ind1, row in enumerate(rimg):
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value)
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255

    compressed_image = rimg.astype(np.uint8)
    plt.title("Image Name: "+img_name+"\n")
    plt.imshow(compressed_image)
    plt.axis('off')
    plt.show()
    compressed_image = Image.fromarray(compressed_image)
    
    enlapsed_time = time.time()- start_time

    print('thoi gian thuc thi', enlapsed_time)    
compress_image("Final", 20)

compressed_image.save("compressedios.jpg")
