# -*- encoding= cp949 -*-

from konlpy.tag import Komoran
import os, re
import utils

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
    print('������ ����')
    ingreds_ds = []
    fp, fn = utils.filePaths(2) # �丮���� ���� �б�
    for p, n in zip(fp, fn): 
        ingreds_df = utils.readFile(p, n, 2)
        ingreds_ds += ingreds_df.values.tolist()
 
    print('\n�󵵼� ���� : ', end = '')
    limit = int(input())
    ingreds_ds = [ingreds_ds[i][0] for i in range(len(ingreds_ds)) if ingreds_ds[i][1] >= limit]

    print('\n�丮���� ������ �������� ����(������ ���� ����)')
    print('���͸��� ������ ����')

    fp, fn = utils.filePaths(2) # �丮���� ������ �������� ����
    for p, n in zip(fp, fn): 
        recipe_df = utils.readFile(p, n, 2)
        recipe_ds = recipe_df.values.tolist()

        newDs = []
        for recipe in recipe_ds[1:2]:
            dishName = recipe[2].split()

            res = dishNameExtract(dishName, ingreds_ds)
            if res != []:
                newDs.append(recipe)
                newDs[-1][2] = ' '.join(res)
                print(newDs[-1])

        name = n[2 : ]
        utils.saveFile(os.getcwd(), f'3_{name}', newDs, 2, recipe_df.columns)

tagging = Komoran()
process()