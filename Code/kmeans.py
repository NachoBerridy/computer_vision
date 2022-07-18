import cv2

class Kmeans():

    def __init__(self, data, graphics):
        
        self.data = data
        self. graphics = graphics

        self.screws = []
        self.nails = []
        self.nuts = []
        self.washers = [] 
        self.images = []
        

        self.first_centers()
        
        self.cen_1 = (self.screws[5][0], self.screws[5][1], self.screws[5][2])
        self.cen_2 = (self.nails[0][0], self.nails[0][1], self.nails[0][2])
        self.cen_3 = (self.nuts[0][0], self.nuts[0][1], self.nuts[0][2])
        self.cen_4 = (self.washers[0][0], self.washers[0][1], self.washers[0][2])
        self.cen = (self.cen_1, self.cen_2, self.cen_3, self.cen_4)
        
        self.cluster = []

    def first_centers(self):

        for i in self.data.canny_df[0].index:
            self.images.append((self.data.canny_df[0]['hu2'][i], self.data.canny_df[0]['slenderness'][i], self.data.canny_df[0]['roundness'][i]))
            self.screws.append((self.data.canny_df[0]['hu2'][i], self.data.canny_df[0]['slenderness'][i], self.data.canny_df[0]['roundness'][i]))

        for i in self.data.canny_df[1].index:
            self.images.append((self.data.canny_df[1]['hu2'][i], self.data.canny_df[1]['slenderness'][i], self.data.canny_df[1]['roundness'][i]))
            self.nails.append((self.data.canny_df[1]['hu2'][i], self.data.canny_df[1]['slenderness'][i], self.data.canny_df[1]['roundness'][i]))

        for i in self.data.canny_df[2].index:
            self.images.append((self.data.canny_df[2]['hu2'][i], self.data.canny_df[2]['slenderness'][i], self.data.canny_df[2]['roundness'][i]))
            self.nuts.append((self.data.canny_df[2]['hu2'][i], self.data.canny_df[2]['slenderness'][i], self.data.canny_df[2]['roundness'][i]))

        for i in self.data.canny_df[3].index:
            self.images.append((self.data.canny_df[3]['hu2'][i], self.data.canny_df[3]['slenderness'][i], self.data.canny_df[3]['roundness'][i]))
            self.washers.append((self.data.canny_df[3]['hu2'][i], self.data.canny_df[3]['slenderness'][i], self.data.canny_df[3]['roundness'][i]))

    def distance(self, images, cen):
    
        cluster_1 = []
        cluster_2 = []
        cluster_3 = []
        cluster_4 = []
        
        
        for i in images:

            
            distance_1 = (((i[0]-cen[0][0])**2) + ((i[1]-cen[0][1])**2) + ((i[2]-cen[0][2])**2))**(1/2)
            distance_2 = (((i[0]-cen[1][0])**2) + ((i[1]-cen[1][1])**2) + ((i[2]-cen[1][2])**2))**(1/2)
            distance_3 = (((i[0]-cen[2][0])**2) + ((i[1]-cen[2][1])**2) + ((i[2]-cen[2][2])**2))**(1/2)
            distance_4 = (((i[0]-cen[3][0])**2) + ((i[1]-cen[3][1])**2) + ((i[2]-cen[3][2])**2))**(1/2)

            if distance_1 <= distance_2 and distance_1 <= distance_3 and distance_1 <= distance_4:
                cluster_1.append(i[:])
            elif distance_2 <= distance_1 and distance_2 <= distance_3 and distance_2 <= distance_4:
                cluster_2.append(i[:])
            elif distance_3 <= distance_1 and distance_3 <= distance_2 and distance_3 <= distance_4:
                cluster_3.append(i[:])
            elif distance_4 <= distance_1 and distance_4 <= distance_2 and distance_4 <= distance_3:
                cluster_4.append(i[:])


        return(cluster_1, cluster_2, cluster_3, cluster_4)

    def recalculate_centroid(self, cluster_list ,cent):

        cen = []
        cont = 0
        for i in cluster_list:
            n = len(i)
            x = 0
            y = 0
            z = 0 
            for j in i:
                
                x = x + j[0]
                y = y + j[1]
                z = z + j[2]
            try:
                cen.append((x/n, y/n, z/n))
            except:
                cen.append(cent[cont])
            cont = cont+1

        return cen 

    def kmeans_method(self, n):

        it = 0
        centroids_1 = [self.cen_1]
        centroids_2 = [self.cen_2]
        centroids_3 = [self.cen_3]
        centroids_4 = [self.cen_4]

        while it<n:

            
            self.cluster = self.distance(self.images, self.cen)
            self.cen = self.recalculate_centroid(self.cluster, self.cen)
            
            centroids_1.append(self.cen[0])
            centroids_2.append(self.cen[1])
            centroids_3.append(self.cen[2])
            centroids_4.append(self.cen[3])
            
            if it > 10:
                if (centroids_1[it] == centroids_1[it-1] and centroids_2[it] == centroids_2[it-1] and 
                    centroids_3[it] == centroids_3[it-1] and centroids_4[it] == centroids_4[it-1]): 
                    return (centroids_1, centroids_2, centroids_3, centroids_4)
                    
            it = it + 1
            
        return (centroids_1, centroids_2, centroids_3, centroids_4)


    def graphic(self):

        self.graphics.k_means_graphic(self.cluster, self.cen)

    def new_image(self, img):

        r, s, h, al, an, rect= self.data.single_img(img)
        img_filtered = (h[1], s, r)
        img = cv2.resize(img, (400, 400))
        self.images.append(img_filtered)
        self.kmeans_method(100)

        if img_filtered in self.cluster[0]:
            #print('ES UN TORNILLO y su medida es: alto = %s ancho = %s'%(al, an))
            self.graphics.img_visualization(rect, img, True, 'TORNILLO')
        elif img_filtered in self.cluster[1]:
            #print('ES UN CLAVO y su medida es: alto = %s ancho = %s'%(al, an))
            self.graphics.img_visualization(rect, img, True, 'CLAVO')
        elif img_filtered in self.cluster[2]:
            #print('ES UNA TUERCA')
            self.graphics.img_visualization(rect, img, False, 'TUERCA')
        elif img_filtered in self.cluster[3]:
            #print('ES UNA ARANDELA')
            self.graphics.img_visualization(rect, img, False, 'ARANDELA')

