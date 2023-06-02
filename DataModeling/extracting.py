# -*- encoding= cp949 -*-

from konlpy.tag import Komoran
from ckonlpy.tag import Twitter
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
    os.system('cls')
    print('������ ����')
    ingreds_ds = []
    fp, fn = utils.filePaths(2) # ������ ���� �б�
    for p, n in zip(fp, fn): 
        ingreds_df = utils.readFile(p, n, 2)
        ingreds_ds += ingreds_df.values.tolist()

    opt = 2     # ����, �ڵ�
    if opt == 1:
        print('\n�󵵼� ���� : ', end = '')
        limit = int(input())
    else:
        limit = 20
    ingreds_ds = [ingreds_ds[i][0] for i in range(len(ingreds_ds)) if ingreds_ds[i][1] >= limit]
    ingreds_ds += utils.readFile(os.getcwd(), '3. Ingreds.txt')

    print('\n�丮���� ������ �������� ����(������ ���� ����)')
    print('���͸��� ������ ����\n')
    fp, fn = utils.filePaths(2) # �丮���� ������ �������� ����
    for p, n in zip(fp, fn): 
        recipe_df = utils.readFile(p, n, 2)
        recipe_ds = recipe_df.values.tolist()

        newDs = []
        for recipe in recipe_ds:
            origin = recipe[2].split()
            reorg = twitter.morphs(' '.join(origin))
            res = dishNameExtract(reorg, ingreds_ds)

            # ��ó���� print �Լ�
            print('origin  : ', origin)
            print('twitter : ', reorg)
            print('result  : ', res)
            print('')
            if res != []:
                newDs.append(recipe)
                newDs[-1][2] = ' '.join(res) 

        name = n[2 : ]
        utils.saveFile(os.getcwd(), f'3_{name}', newDs, 2, recipe_df.columns)

def addDict():
    words = utils.readFile(os.getcwd(), '2. Dictionary.txt')
    for word in words:
        twitter.add_dictionary(word, 'Noun')

twitter = Twitter()
addDict()
tagging = Komoran()
process()