import cv2

class Knn:

    def __init__(self, data, graphic):
        
        self.data = data
        self.graphic = graphic
        self.screws = []
        self.nails = []
        self.nuts = []
        self.washers = [] 
        self.data_split()

    def data_split(self):

        for i in self.data.canny_df[0].index:
            self.screws.append((self.data.canny_df[0]['hu2'][i], self.data.canny_df[0]['slenderness'][i], self.data.canny_df[0]['roundness'][i]))

        for i in self.data.canny_df[1].index:
            self.nails.append((self.data.canny_df[1]['hu2'][i], self.data.canny_df[1]['slenderness'][i], self.data.canny_df[1]['roundness'][i]))

        for i in self.data.canny_df[2].index:
            self.nuts.append((self.data.canny_df[2]['hu2'][i], self.data.canny_df[2]['slenderness'][i], self.data.canny_df[2]['roundness'][i]))

        for i in self.data.canny_df[3].index:
            self.washers.append((self.data.canny_df[3]['hu2'][i], self.data.canny_df[3]['slenderness'][i], self.data.canny_df[3]['roundness'][i]))

    def distance(self, img):

        distance = []
        for i in self.screws:
            distance.append(((((img[0]-i[0])**2) + ((img[1]-i[1])**2) + ((img[2]-i[2])**2))**(1/2), 'screw'))
        for i in self.nails:
            distance.append(((((img[0]-i[0])**2) + ((img[1]-i[1])**2) + ((img[2]-i[2])**2))**(1/2), 'nail'))
        for i in self.nuts:
            distance.append(((((img[0]-i[0])**2) + ((img[1]-i[1])**2) + ((img[2]-i[2])**2))**(1/2), 'nuts'))
        for i in self.washers:
            distance.append(((((img[0]-i[0])**2) + ((img[1]-i[1])**2) + ((img[2]-i[2])**2))**(1/2), 'washer'))

        return(distance)
        

    def knn_method(self, img, n):
        
        r, s, h, al, an , rect = self.data.single_img(img)
        img_filtered = (h[1], s, r)
        distances = self.distance(img_filtered)
        distances.sort()
        neighbours = distances[0:n]
        print(neighbours)
        img = cv2.resize(img, (400, 400))
        s = 0
        na = 0
        nu = 0
        w = 0
        for i in neighbours:
            if i[1] == 'screw':
                s = s + 1
            elif i[1] == 'nail':
                na = na + 1
            elif i[1] == 'nuts':
                nu = nu + 1
            elif i[1] == 'washer':
                w = w + 1
        print('s:%s na:%s nu:%s w:%s'%(s, na, nu, w))
        if s >= na and s >= nu and s >= w:
            print('ES UN TORNILLO y su medida es: alto = %s ancho = %s'%(al, an))
            self.graphic.img_visualization(rect, img, True, 'TORNILLO')
        if na >= s and na >= nu and na >= w:
            print('ES UN CLAVO y su medida es: alto = %s ancho = %s'%(al, an))
            self.graphic.img_visualization(rect, img, True, 'CLAVO')
        if nu >= s and nu >= na and nu >= w:
            print('ES UNA TUERCA')
            self.graphic.img_visualization(rect, img, False, 'TUERCA')
        if w >= s and w >= na and w >= nu:
            print('ES UNA ARANDELA')
            self.graphic.img_visualization(rect, img, False, 'ARANDELA')

            

                        
                    