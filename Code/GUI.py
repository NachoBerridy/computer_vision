from tkinter import *
from tkinter import filedialog
from data_collector import Data_collector
from graphic_analysis import Graphic_Analysis
from knn import Knn
from kmeans import Kmeans
import cv2
import copy

class GUI:

    def __init__(self):
        

        self.data = Data_collector()
        self.graphics = Graphic_Analysis(self.data)
        self.kmeans = Kmeans(self.data, self.graphics)
        self.knn = Knn(self.data, self.graphics)

        self.new_path = ''
        self.new_image = []

        self.root = Tk()
        self.root.title('Vision Artificial 1.0 - Ignacio Berridy 2022')       

        Button(self.root, text = 'Seleccionar nueva imagen', command = self.select_file , activebackground = 'SeaGreen1' ).grid(row = 1, column = 1)
        Button(self.root, text = 'Kmeans', command = self.execute_kmeans).grid(row = 2, column = 1)
        Button(self.root, text = 'Knn', command = self.execute_knn).grid(row = 3, column = 1) 
    
    def select_file(self):
        
        file = filedialog.askopenfilename()
        self.new_path = file
        self.new_image = cv2.imread(self.new_path)

    def execute_kmeans(self):
        self.kmeans.kmeans_method(100)
        img = copy.deepcopy(self.new_image)
        self.kmeans.new_image(img)
        self.kmeans.graphic()

    def execute_knn(self):
        img = copy.deepcopy(self.new_image)
        self.knn.knn_method(img,7)
       


    