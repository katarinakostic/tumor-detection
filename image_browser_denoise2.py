# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 22:04:40 2021

@author: Katarina
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from skimage import color
from skimage import img_as_ubyte, img_as_float, io
from skimage.restoration import denoise_nl_means, estimate_sigma
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage as nd
import napkin


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        self.button()


    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)


    def fileDialog(self):

        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)

        img = Image.open(self.filename)
        photo = ImageTk.PhotoImage(img)
        img_flt = img_as_float(io.imread(self.filename))
        
        
        sigma_est = np.mean(estimate_sigma(img_flt, multichannel=True))
        denoise = denoise_nl_means(img_flt, h=1.15 * sigma_est, fast_mode=True,
                             patch_size=5, patch_distance=3, multichannel=True)
        
        denoise_ubyte1 = img_as_ubyte(denoise)
        # print(denoise_ubyte1.shape[0])
        # print(denoise_ubyte1.shape[1])
        # print(denoise_ubyte1.shape[2])
        denoise_ubyte = denoise_ubyte1[:,:,0]
        # plt.hist(denoise_ubyte.flat, bins=100, range=(0,255))
        
        #segm1 = (denoise_ubyte <= 25)
        # all_segments = np.zeros((denoise_ubyte.shape[0], denoise_ubyte.shape[1], 3))
        # all_segments[segm1] = (1,1,1)

        s=(denoise_ubyte.shape[0], denoise_ubyte.shape[1], 3)
        all_segments_cleaned = np.zeros(s)
        
        segm1 = (denoise_ubyte <= 25)
        
        segm1_opened = nd.binary_opening(segm1, np.ones((3, 3))) # 3x3
        segm1_closed = nd.binary_closing(segm1_opened, np.ones((3, 3)))
        
        all_segments_cleaned[segm1_closed] = (1,1,1)
        
        start = self.filename.rfind("/")
        end = len(self.filename)
        m="denoised"+self.filename[start:end]
        print(m)
        
        plt.imsave(m, all_segments_cleaned)

        self.label2 = Label(image=photo)
        self.label2.image = photo 
        self.label2.grid(column=1, row=4)
        
        
        img_denoised = Image.open(m)
        
        
        photo_denoised = ImageTk.PhotoImage(img_denoised)
        self.label3 = Label (image =  photo_denoised)
        self.label3.image = photo_denoised
        self.label3.grid(column=1, row=5)
        


    # def button2(self):
    #      self.button2 = ttk.Button(self.labelFrame, text = "Detect")
    #      self.button2.grid(column = 2, row = 1)
        
    
root = Root()
root.mainloop()

# from scipy import ndimage as nd

# #binary opening and binary closing
# #opening takes care of straight pixels
# #closing takes care of voids -> ako imamo piksel koji je blank a okruzen je drugim pikselima, popunjava ga
# segm1_opened = nd.binary_opening(segm1, np.ones((3, 3))) # 3x3
# segm1_closed = nd.binary_closing(segm1_opened, np.ones((3, 3)))

# segm2_opened = nd.binary_opening(segm2, np.ones((3, 3))) # 3x3
# segm2_closed = nd.binary_closing(segm2_opened, np.ones((3, 3)))

# segm3_opened = nd.binary_opening(segm3, np.ones((3, 3))) # 3x3
# segm3_closed = nd.binary_closing(segm3_opened, np.ones((3, 3)))

# segm4_opened = nd.binary_opening(segm4, np.ones((3, 3))) # 3x3
# segm4_closed = nd.binary_closing(segm4_opened, np.ones((3, 3)))

# all_segments_cleaned = np.zeros((denoise_ubyte.shape[0], denoise_ubyte.shape[1], 3))

# # svi segm1 pikseli su boje 1,0,0
# all_segments_cleaned[segm1_closed] = (1,0,0)
# all_segments_cleaned[segm2_closed] = (0,1,0)
# all_segments_cleaned[segm3_closed] = (0,0,1)
# all_segments_cleaned[segm4_closed] = (1,1,0)

# plt.imshow(all_segments_cleaned)
# plt.imsave("images/segmented_2.jpg", all_segments_cleaned)