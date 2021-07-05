import cv2
import numpy as np
from PIL import Image



class Merge():
    def __init__(self,abs_dir,root,the_shorter_num):
        #print(abs_dir)
        self.root = root
        # self.pic_name_dic = pic_name_dic
        self.center_img = cv2.imread(abs_dir)
        self.the_shorter_num = the_shorter_num

        NN=abs_dir.split("/")[-1].split(".")[0]
        #print(NN)
        self.r=int(NN.split("x")[0])
        self.c=int(NN.split("x")[1])

    def mergeX(self,circle):


        grid = []
        center_int_row=min(self.the_shorter_num-circle-1,max(circle,self.r))
        center_int_col=min(self.the_shorter_num-circle-1,max(circle,self.c))

        for i in range(center_int_row-circle,center_int_row+circle+1):
            grid_one_row=[]
            for j in range(center_int_col - circle, center_int_col + circle+1):
                if i==self.r and j==self.c:
                    tem_img=self.center_img
                else:
                    tem_img=cv2.imread(self.root+str(i)+"x"+str(j)+".jpg")
                #print(self.root+str(i)+"x"+str(j)+".jpg")
                grid_one_row.append(tem_img)
            grid_one_row_concat= np.concatenate(grid_one_row, axis=1)
            grid.append(grid_one_row_concat)
        all_concat= np.concatenate(grid, axis=0)
        img = cv2.cvtColor(all_concat, cv2.COLOR_BGR2RGB)
        img=Image.fromarray(img.astype(np.uint8))
        img = img.toqpixmap()
        return  img


    def merge3(self):
        return self.mergeX(1)

    def merge5(self):
        return self.mergeX(2)











