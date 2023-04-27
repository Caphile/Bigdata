# -*- coding: cp949 -*-

from collections import Counter
import pandas as pd
import numpy as np
from tkinter import filedialog, Tk
import ast
import os
import re

def fileOpen(opt):
    root = Tk()
    root.withdraw()

    if opt == 1:    # �������� �Ѱ�
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

def fileCreate(dt, val, fileName):
    #try:
    #    folder = '10000recipeData'  # ���� ���� ������
    #    os.mkdir(folder)
    #except:
    #    pass

    cols = [['Key', '�丮��', '�κ�', '�ҿ�ð�', '���̵�', '���', '������'],
            ['���', '�󵵼�'],
            ['���', '�󵵼�']]
    df = pd.DataFrame(dt, columns = cols[val - 1])

    pattern = r'F\d+_T\d+'
    fName = re.findall(pattern, fileName)[0]

    if val == 3:
        val = '������'
    fName = f'{fName}_{val}.xlsx'

    root = Tk()
    root.withdraw()

    fName = filedialog.asksaveasfilename(initialdir = os.getcwd(), initialfile = fName)
    root.destroy()

    df.to_excel(fName, index = False)

def process1(): # �ѹ��� ���� ���� �е��� ���� ����
    dt, fName = fileOpen(2)

    for c, d in enumerate(dt):
        subDt = []
        for i in d:
            min = i[3].find('��')
            if min != -1 and int(i[3][ : min]) <= 30 and i[4] in ['�ƹ���', '�ʱ�']:
                subDt.append(i)

        #fileCreate(subDt, 1, fName)
        subDt = np.array(subDt)

        ingred = np.transpose(subDt[ : , 5 : 6]).tolist()[0]
        ingred_dict = []
        for i in ingred:
            temp = ast.literal_eval(i)
            ingred_dict.append(temp)

        ingreds = []
        for i in ingred_dict:
            for j in i:
                ingreds.append(list(j.keys())[0].replace(' ', ''))  # ������ ���� ����

        counts = Counter(ingreds)

        counts_key = list(counts.keys())
        counts_val = list(counts.values())

        param = []
        for i in range(len(counts_key)):
            param.append([counts_key[i], counts_val[i]])  
    
        fileCreate(param, 2, fName[c])

def process2():
    dt, fNames = fileOpen(2)

    ingreds = []
    counts = []
    for d in dt:
        d = np.array(d).transpose().tolist()

        # ������ ���� ����
        #for i in range(len(d[0])):
        #    d[0][i] = d[0][i].replace(' ', '')

        for i, c in zip(d[0], d[1]):
            if i in ingreds:
                idx = ingreds.index(i)
                counts[idx] += int(c)
            else:
                ingreds.append(i)
                counts.append(int(c))

    df = []
    for i in range(len(ingreds)):
        df.append([ingreds[i], counts[i]])
    df = sorted(df, key=lambda x: x[1], reverse=True)

    pattern = r'F\d+_T\d+'
    fromMin = float('inf')
    toMax = float('-inf')
    for f in fNames:
        nums = re.findall('\d+', re.findall(pattern, f)[0])
        fromMin = min(fromMin, int(nums[0]))
        toMax = max(toMax, int(nums[1]))

    title = f'F{fromMin}_T{toMax}'

    fileCreate(df, 3, title)

print('1. �ҿ�ð�, ���̵� ���͸� �� ��� �󵵼�')
print('2. ��� �󵵼� ����')
print('���� :', end = ' ')
n = int(input())

while 1:
    if n == 1:
        process1()
    else:
        break
if n == 2:
    process2()