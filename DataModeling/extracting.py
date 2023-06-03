# -*- encoding= cp949 -*-

from konlpy.tag import Komoran
from ckonlpy.tag import Twitter
import os, re
import utils
import ner
#import recipe_spell as rs

model = ner.loadModel()

def dishNameExtract(dishNames, ingreds):
    dishNameList = []
    for ingred in ingreds:
        for dishName in dishNames:
            dishName = re.sub('[^a-zA-Z0-9\s\uAC00-\uD7AF]', '', dishName)  # Ư������ ����
            if ingred in dishName and tagging.pos(dishName)[0][1] == 'NNP':
                dishNameList.append(dishName)
    dishNameList = list(set(dishNameList))
    return dishNameList

def process():
    os.system('cls')
    print('������ ����')
    ingreds_ds = []
    fp, fn = utils.filePaths(2) # ������ ���� �б�
    for p, n in zip(fp, fn): 
        ingreds_df = utils.readFile(p, n, 2)
        ingreds_ds += ingreds_df.values.tolist()[1 : ]

    opt = 2     # ����, �ڵ�
    if opt == 1:
        print('\n�󵵼� ���� : ', end = '')
        limit = int(input())
    else:
        limit = 20
    ingreds_ds = [ingreds_ds[i][0] for i in range(len(ingreds_ds)) if ingreds_ds[i][1] >= limit]
    ingreds_ds += utils.readFile(os.getcwd(), '3. Ingreds.txt')


    print('\n�������� ����(������ ���� ����)')
    print('���͸��� ������ ����\n')
    fp, fn = utils.filePaths(2) # �丮���� ������ �������� ����
    for p, n in zip(fp, fn): 
        df = utils.readFile(p, n, 2)
        ds = df.values.tolist()[1 : ]

        newDt = []
        for d in ds:
            # �丮��
            dish = d[2]

            tempDish = []
            doc = model(dish)
            for entity in doc.ents:
                if entity.label_ == 'DISH':
                    tempDish.append(entity.text)

            dish = ' '.join(tempDish)

            # ���
            ingreds = d[6]



            # ������
            recipe = d[7]
            recipe = rs.process(recipe)
            
            # ��� �����Ͱ� ������ ��츸 ����
            newDt.append([d[0], d[1], dish, d[3], d[4], d[5], ingreds, recipe, d[8]])

        name = n[2 : ]
        utils.saveFile(os.getcwd(), f'3_{name}', newDt, 2, df.columns)

def addDict():
    words = utils.readFile(os.getcwd(), '2. Dictionary.txt')
    for word in words:
        twitter.add_dictionary(word, 'Noun')

twitter = Twitter()
addDict()
tagging = Komoran()
process()