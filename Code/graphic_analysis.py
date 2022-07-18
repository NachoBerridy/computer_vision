from cProfile import label
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


class Graphic_Analysis:

    def __init__(self, data):
        
        self.data = data 
        
    def hu_plot(self, n, filter_df):
        hu_names = ['hu1', 'hu2', 'hu3', 'hu4', 'hu5', 'hu6', 'hu7']
        tools = ['Screws', 'Nails', 'Nuts', 'Washers']

        if n == 0:  
            counter = 0 
            for i in filter_df:
                fig , ax = plt.subplots()
                plt.title('Hu moments: ' + tools[counter])
                plt.xlabel('Image') 

                plt.ylabel('hu values')
                counter  = counter +1
                for j in hu_names:
                    ax.plot(i[j], marker = 'o', label = j)
                plt.legend()

        if n != 0:  
            counter = 0 
            fig , ax = plt.subplots()
            for i in self.data.canny_df:
                plt.title(hu_names[n-1])
                plt.xlabel('Image')
                plt.ylabel('hu values')
                ax.plot(i[hu_names[n-1]], marker = 'o', label = tools[counter])
                plt.legend()
                counter  = counter +1
                        
        plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def roundness_plot(self, filter_df):

        tools = ['Screws', 'Nails', 'Nuts', 'Washers']
        counter = 0
        fig, ax = plt.subplots()
        plt.title('Roundness')
        plt.xlabel('Image')
        plt.ylabel('Roundness values') 
        for i in filter_df:
            ax.plot(i['roundness'], marker = 'o', label = tools[counter])
            counter  = counter +1
        plt.legend()
        plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def slenderness_plot(self, filter_df):

        tools = ['Screws', 'Nails', 'Nuts', 'Washers']
        counter = 0
        fig, ax = plt.subplots()
        plt.title('height/width')
        plt.xlabel('Image')
        plt.ylabel('height/width values') 
        for i in filter_df:
            ax.plot(i['slenderness'], marker = 'o', label = tools[counter])
            counter  = counter +1
        plt.legend()
        plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def img_visualization(self, rectangle, img, l, tool):

        (x, y) = rectangle[0]
        (al, an) = rectangle[1] 
        if an >= al:
            al, an = an, al
        rect = cv2.boxPoints(rectangle)
        rect = np.int0(rect)
        cv2.polylines(img, [rect], True, (0, 255, 0), 2)
        cv2.putText(img, tool, (int(x)+10, int(y)-70), cv2.LINE_AA, 0.8, (255, 0, 0), 2)
        if l == True:
            cv2.putText(img, 'Alto: %s cm'%round(al/35.333, 2), (int(x)+10, int(y)-15), cv2.LINE_AA, 0.8, (255, 0, 0), 2)
            cv2.putText(img, 'Ancho: %s cm'%round(an/35.333, 2), (int(x)+10, int(y)+15), cv2.LINE_AA, 0.8, (255, 0, 0), 2) 
        cv2.imshow('Imagen', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
    def k_means_graphic(self, cluster, cen):
        
        def extract_values(cluster):
    
            x = []
            y = []
            z = []
            
            for i in cluster:
                
                x.append(i[0])
                y.append(i[1])
                z.append(i[2])

            return((x, y, z))


        fig = plt.figure()
        (x1, y1, z1) = extract_values(cluster[0])
        (x2, y2, z2) = extract_values(cluster[1])
        (x3, y3, z3) = extract_values(cluster[2])
        (x4, y4, z4) = extract_values(cluster[3])

        ax1 = fig.add_subplot(111,projection='3d')
        ax1.scatter(x1, y1, z1, c = 'b', label = 'Tornillos')
        ax1.scatter(cen[0][0], cen[0][1], cen[0][2], c = 'b', marker = 's')
        ax1.scatter(x2, y2, z2, c = 'y', label = 'Clavos')
        ax1.scatter(cen[1][0], cen[1][1], cen[1][2], c = 'y', marker = 's')
        ax1.scatter(x3, y3, z3, c = 'g', label = 'Tuercas')
        ax1.scatter(cen[2][0], cen[2][1], cen[2][2], c = 'g', marker = 's')
        ax1.scatter(x4, y4, z4, c = 'r', label = 'Arandelas')
        ax1.scatter(cen[3][0], cen[3][1], cen[3][2], c = 'r', marker = 's')

        ax1.set_xlabel('hu2')
        ax1.set_ylabel('slenderness')
        ax1.set_zlabel('roundness')


        plt.legend()
        plt.show()
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        

    def images_filtered(self):

        #fig , ax = plt.subplots()

        cv2.imshow('a', self.data.screws[0])
        cv2.imshow('s', self.data.canny_screws[0])
        cv2.imshow('d', self.data.gaussian_screws[0])
        cv2.imshow('f', self.data.gray_screws[0])
        cv2.imshow('g', self.data.contour_screws[0])

        cv2.waitKey(0)
        cv2.destroyAllWindows()


      