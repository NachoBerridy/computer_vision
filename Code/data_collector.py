import cv2
import os
import math
import numpy as np
import pandas as pd
from pathlib import Path


class Data_collector:

    def __init__(self, image_path = str(Path.cwd())):
        

        #Imagenes
        self.screws = self.load_images(image_path + '\\Images\\screw')
        self.nails = self.load_images(image_path + '\\Images\\nail')
        self.nuts = self.load_images(image_path + '\\Images\\nut')
        self.washers = self.load_images(image_path + '\\Images\\washer')

        #Imagenes en escala de grises
        self.gray_screws = self.gray_scale_list(self.screws)
        self.gray_nails = self.gray_scale_list(self.nails)
        self.gray_nuts = self.gray_scale_list(self.nuts)
        self.gray_washers = self.gray_scale_list(self.washers)

        #Imagenes con filtro gaussiano
        self.gaussian_screws = self.gaussianblur_list(self.gray_screws) 
        self.gaussian_nails = self.gaussianblur_list(self.gray_nails) 
        self.gaussian_nuts = self.gaussianblur_list(self.gray_nuts)
        self.gaussian_washers = self.gaussianblur_list(self.gray_washers)

        #Imagenes con filtro canny
        self.canny_screws = self.canny_list(self.gaussian_screws)
        self.canny_nails = self.canny_list(self.gaussian_nails)
        self.canny_nuts = self.canny_list(self.gaussian_nuts)
        self.canny_washers = self.canny_list(self.gaussian_washers)
        self.canny = [self.canny_screws, self.canny_nails, self.canny_nuts, self.canny_washers] 
        

        #Imagenes con filtro binario
        self.binary_screws = self.binary_filter_list(self.gray_screws)
        self.binary_nails = self.binary_filter_list(self.gray_nails)
        self.binary_nuts = self.binary_filter_list(self.gray_nuts)
        self.binary_washers = self.binary_filter_list(self.gray_washers) 
        self.binary = [self.binary_screws, self.binary_nails, self.binary_nuts, self.binary_washers]

        #Imagenes solo con contorno

        self.contour_screws = self.contour_images(self.canny_screws)
        self.contour_nails = self.contour_images(self.canny_nails)
        self.contour_nuts = self.contour_images(self.canny_nuts)
        self.contour_washers = self.contour_images(self.canny_washers)
        self.cont = [self.contour_screws, self.contour_nails, self.contour_nuts, self.contour_washers] 

        #Variables con informacion de las imagenes     
         
        self.canny_hu = []
        self.canny_contour = []
        self.canny_roundness = []
        self.canny_slenderness = []
        self.binary_hu = []
        self.binary_contour = []
        self.binary_roundness = []
        self.binary_slenderness = []
        self.fill_information()

        #Data frame con la informacion de cada grupo de imagenes
        self.binary_screw_df = pd.DataFrame()
        self.canny_screw_df = pd.DataFrame()    
        self.binary_nail_df = pd.DataFrame()
        self.canny_nail_df = pd.DataFrame()
        self.binary_nut_df = pd.DataFrame()
        self.canny_nut_df = pd.DataFrame()
        self.binary_washer_df = pd.DataFrame()
        self.canny_washer_df = pd.DataFrame()
        self.organize_information()
        self.canny_screw_df.to_csv('screws.csv')
        self.canny_nail_df.to_csv('nails.csv')
        self.canny_nut_df.to_csv('nuts.csv')
        self.canny_washer_df.to_csv('washers.csv')
        self.canny_df = [self.canny_screw_df, self.canny_nail_df, self.canny_nut_df, self.canny_washer_df]
        self.binary_df = [self.binary_screw_df, self.binary_nail_df, self.binary_nut_df, self.binary_washer_df]

    #Funciones de tratamiento de imagen

    def load_images(self, dir):
        '''
        Recibe un directorio y devuelve una lista con las imagenes
        '''
        paths = os.listdir(dir)
        images = []

        for i in paths:
            path = dir+'\\'+i
            images.append(cv2.resize(cv2.imread(path), (400, 400)))

        return images

    def gray_scale_list(self, img_list):
    
        '''
        Recibe una lista de imagenes y las devuelve en escala de grises
        '''
        gray_images = []

        for i in img_list:
            gray_images.append(cv2.cvtColor(i,cv2.COLOR_BGR2GRAY))

        return gray_images

    def gaussianblur_list(self, img_list):

        '''
        Recibe una lista de imagenes y devuelve otra lista con
        las imagenes luego de aplicarles el filtro gaussiano
        '''
        filtered_images = []
        
        for i in img_list:
            filtered_images.append(cv2.GaussianBlur(i, (5, 5), 0))

        return filtered_images

    def canny_list(self, img_list):

        '''
        Recibe una lista de imagenes y devuelve otra lista con
        las imagenes luego de aplicarles el filtro Canny
        '''
        filtered_images = []
        for i in img_list:
            i = cv2.Canny(i, 40, 160)
            i = cv2.dilate(i, None, iterations = 1)
            i = cv2.erode(i, None, iterations = 1)
            filtered_images.append(i)

        return filtered_images

    def binary_filter_list(self, img_list):
    
        '''
        Recibe una lista de imagenes y las devuelve filtradas con un filtro
        binario
        '''

        filtered_images = []

        for i in img_list:
            a, inv_binary = cv2.threshold(i,100,255,cv2.THRESH_BINARY_INV)
            filtered_images.append(inv_binary)

        return filtered_images

    def contour_images(self, img_list):

        images = []

        for i in img_list:
            contours, hierarchy = cv2.findContours(i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            draw = np.zeros((i.shape[0], i.shape[1], 3), dtype=np.uint8) 
            i = cv2.drawContours(draw, contours, -1, (0, 255, 0), 2)
            i = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)  
            #i = cv2.dilate(i, None, iterations = 1)
            #i = cv2.erode(i, None, iterations = 1)  
            images.append(i)
        return images

    #Funciones de extraccion de datos de la imagen

    def fill_information(self):

        for i in self.cont:
            self.canny_hu.append(self.hu_moments(i))
        for i in self.canny:
            self.canny_contour.append(self.contour_list(i)) 
        for i in self.canny_contour:
            self.canny_roundness.append(self.roundness_list(i))
            self.canny_slenderness.append(self.slenderness_list(i)) 
        
        for i in self.binary:
            self.binary_hu.append(self.hu_moments(i))
            self.binary_contour.append(self.contour_list(i))
        for i in self.binary_contour:
            self.binary_roundness.append(self.roundness_list(i))
            self.binary_slenderness.append(self.slenderness_list(i))

    def organize_information(self):

        hu_names = ['hu1', 'hu2', 'hu3', 'hu4', 'hu5', 'hu6', 'hu7']

        canny_screw_dict = {'roundness':self.canny_roundness[0], 
                            'slenderness':self.canny_slenderness[0]}
        binary_screw_dict = {'roundness':self.binary_roundness[0], 
                             'slenderness':self.binary_slenderness[0]}
        hu_counter = 0 
        for i in hu_names:
            canny_screw_dict[i] = []
            binary_screw_dict[i] = []
            for j in self.canny_hu[0]:
                canny_screw_dict[i].append(j[hu_counter])
            for l in self.binary_hu[0]:
                binary_screw_dict[i].append(l[hu_counter])
            hu_counter = hu_counter + 1


        canny_nail_dict = {'roundness':self.canny_roundness[1], 
                           'slenderness':self.canny_slenderness[1]}
        binary_nail_dict = {'roundness':self.binary_roundness[1], 
                            'slenderness':self.binary_slenderness[1]}
        hu_counter = 0 
        for i in hu_names:
            canny_nail_dict[i] = []
            binary_nail_dict[i] = []
            for j in self.canny_hu[1]:
                canny_nail_dict[i].append(j[hu_counter])
            for l in self.binary_hu[1]:
                binary_nail_dict[i].append(l[hu_counter])
            hu_counter = hu_counter +1


        canny_nut_dict = {'roundness':self.canny_roundness[2], 
                          'slenderness':self.canny_slenderness[2]}
        binary_nut_dict = {'roundness':self.binary_roundness[2], 
                           'slenderness':self.binary_slenderness[2]}
        hu_counter = 0 
        for i in hu_names:
            canny_nut_dict[i] = []
            binary_nut_dict[i] = []
            for j in self.canny_hu[2]:
                canny_nut_dict[i].append(j[hu_counter])
            for l in self.binary_hu[2]:
                binary_nut_dict[i].append(l[hu_counter])
            hu_counter = hu_counter +1


        canny_washer_dict = {'roundness':self.canny_roundness[3], 
                             'slenderness':self.canny_slenderness[3]}
        binary_washer_dict = {'roundness':self.binary_roundness[3], 
                              'slenderness':self.binary_slenderness[3]}
        hu_counter = 0 
        for i in hu_names:
            canny_washer_dict[i] = []
            binary_washer_dict[i] = []
            for j in self.canny_hu[3]:
                canny_washer_dict[i].append(j[hu_counter])
            for l in self.binary_hu[3]:
                binary_washer_dict[i].append(l[hu_counter])
            hu_counter = hu_counter +1


        self.binary_screw_df = pd.DataFrame(binary_screw_dict)
        self.canny_screw_df = pd.DataFrame(canny_screw_dict)

        self.binary_nail_df = pd.DataFrame(binary_nail_dict)
        self.canny_nail_df = pd.DataFrame(canny_nail_dict)

        self.binary_nut_df = pd.DataFrame(binary_nut_dict)
        self.canny_nut_df = pd.DataFrame(canny_nut_dict)

        self.binary_washer_df = pd.DataFrame(binary_washer_dict)
        self.canny_washer_df = pd.DataFrame(canny_washer_dict)

    def contour_list(self, img_list):

        '''
        Recibe una lista de imagenes y devuelve una matriz con los
        contornos de cada imagen
        '''

        contours_list = []

        for i in img_list:
            contours = []
            hierarchy = []
            contours,hierarchy = cv2.findContours(i,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            contours_list.append(contours)

        return contours_list

    def hu_moments(self, img_list):

        '''
        Recibe una lista de imagenes  y devuelve una lista con sus momentos de hu escalados
        '''
        Hu = []
        for i in img_list:
            hu_list = []
            moment = cv2.moments(i)
            hu_moments = (cv2.HuMoments(moment))
            for j in range(len(hu_moments)):
                hu_list.append(float(-1* math.copysign(1.0, hu_moments[j])* math.log10(abs(hu_moments[j]))))
            Hu.append(hu_list)
        return Hu

    def roundness_list(self, con_list):

        '''
        Recibe una matriz con contornos de una lista de imagen y devuelve una lista
        con ru redondez
        '''
        roundness = []
        p = math.pi

        for i in con_list:
            r = 0
            area = 0
            arc_length = 0
            
            for j in i:
                area = area + cv2.contourArea(j)
                arc_length = arc_length + cv2.arcLength(j, True)
                coef = 0.03 * cv2.arcLength(j, True)
                n = cv2.approxPolyDP(j, coef, True)
            try:
                r = (4*p*area)/(arc_length**2)
                #round(r, 2)*
            except:
                roundness.append('Error')
            roundness.append(round(len(n)*r, 5))
        return roundness

    def slenderness_list(self, con_list):

        '''
        Recibe una matriz con los contornos de una lista de imagenes
        y devuelve un valor de esbeltez para cada una de las mismas
        '''
        slenderness = []
        for i in con_list:
            height = 0
            width = 0
            for j in i:
                (x, y), (current_width, current_height), angle = cv2.minAreaRect(j)
                if current_height<current_width:
                    current_width, current_height = current_height, current_width
                if current_width>width:
                    width = current_width
                if current_height>height:
                    height = current_height
            try:
                slenderness.append(round(height/width, 2))
            except:
                slenderness.append('Error')
        return slenderness

    def single_img(self, img):

        img = cv2.resize(img, (400, 400))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_canny = cv2.GaussianBlur(img, (5, 5), 0)
        img_canny = cv2.Canny(img_canny, 50, 150)
        img_canny = cv2.dilate(img_canny, None, iterations = 1)
        img_canny = cv2.erode(img_canny, None, iterations = 1)

        contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        draw = np.zeros((img_canny.shape[0], img_canny.shape[1], 3), dtype=np.uint8) 
        img_contour = cv2.drawContours(draw, contours, -1, (0, 255, 0), 5)
        img_contour = cv2.cvtColor(img_contour,cv2.COLOR_BGR2GRAY)  

        moments = cv2.moments(img_contour)
        hu = cv2.HuMoments(moments)
        HU = []
        for j in range(len(hu)):
                HU.append(float(-1* math.copysign(1.0, hu[j])* math.log10(abs(hu[j]))))
        
        
        p = math.pi
        r = 0
        area = 0
        arc_length = 0

        height = 0
        width = 0

        for i in contours:
            area = area + cv2.contourArea(i)
            arc_length = arc_length + cv2.arcLength(i, True)
            coef = 0.03 * cv2.arcLength(i, True)
            n = cv2.approxPolyDP(i, coef, True)
            r = (4*p*area)/(arc_length**2)

            rect = cv2.minAreaRect(i)
            (x, y), (current_width, current_height), angle = rect
            if current_height<current_width:
                current_width, current_height = current_height, current_width
            if current_width>width:
                width = current_width
            if current_height>height:
                height = current_height
            try:
                slenderness = (round(height/width, 2))
            except:
                pass
        
        roundness = (round(len(n)*r, 5))   
        return(roundness, slenderness, HU, height, width, rect)
