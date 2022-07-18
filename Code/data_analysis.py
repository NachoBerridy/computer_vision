from data_collector import Data_collector
from graphic_analysis import Graphic_Analysis

data = Data_collector()
graphics = Graphic_Analysis(data)

for i in data.canny_df:
    i.to_csv('data.csv')

graphics.images_filtered()

'''graphics.slenderness_plot(graphics.data.canny_df)
graphics.roundness_plot(graphics.data.canny_df)
for i in range(1,8):
    graphics.hu_plot(i, graphics.data.canny_df)'''