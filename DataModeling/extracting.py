# -*- encoding= cp949 -*-

import pandas as pd
from tkinter import filedialog, Tk
import os
import re

def fileOpen(opt):
    root = Tk()
    root.withdraw()

    if opt == 1:    # ���� �Ѱ�
        fileName = filedialog.askopenfilename(title ='Select Excel File', initialdir = os.getcwd(), filetypes = (('Excel Files', '*.xlsx'), ('All Files', '*.*')))
        df = pd.read_excel(fileName)
        dt = df.values.tolist()
    if opt == 2:    # ���� ���� ����
        dt = []
        fileName = filedialog.askopenfilenames(title ='Select Excel Files', initialdir = os.getcwd(), filetypes = (('Excel Files', '*.xlsx'), ('All Files', '*.*')))
        for f in fileName:
            df = pd.read_excel(f)
            dt.append(df.values.tolist())
    
    root.destroy()
    return dt, fileName


def dishNameExtract(dishNames, ingreds):
    dishNameList = []
    for ingred in ingreds:
        for dishName in dishNames:
            dishName = re.sub('[^a-zA-Z0-9\s\uAC00-\uD7AF]', '', dishName)  # Ư������ ����
            if ingred in dishName:
                dishNameList.append(dishName)
    dishNameList = list(set(dishNameList))
    return dishNameList

def process():
    ingreds, notUse = fileOpen(1)   # �丮���� ���� �б�
    dishFiles, fn = fileOpen(2)     # �丮���� ������ �������� ����

    ingreds = [ingreds[i][0] for i in range(len(ingreds))]
    
    for c, dishes in enumerate(dishFiles):
        for dish in dishes:
            dishName = dish[1].split()
                
            a = dishNameExtract(dishName, ingreds)
            if a == []:
               a = [None]

            print(a)



process()