# -*- encoding= cp949 -*-

from konlpy.tag import Komoran
from ckonlpy.tag import Twitter
import os, re, ast
import utils
import ner

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

    '''
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
    '''
    N = utils.useN()

    print('�������� ����(������ ���� ����)')
    print('���͸��� ������ ����\n')
    fp, fn = utils.filePaths(2) # �丮���� ������ �������� ����
    for p, n in zip(fp, fn): 
        df = utils.readFile(p, n, 2)
        ds = df.values.tolist()

        newDt = []
        for d in ds:
            try:    # ������ �ս��� �Ͼ�� ��츦 ���
                # �丮��
                dish = N.process(d[2])

                tempDish = []
                doc = model(dish)
                for entity in doc.ents:
                    if entity.label_ == 'DISH':
                        tempDish.append(entity.text)

                dish = ' '.join(tempDish)

                if dish == '' or len(dish) > 10:
                    continue
            
                # ���
                if d[6] == '[]':
                    continue
                ingreds = ast.literal_eval(d[6])    # list
                # process

                # ������
                if d[7] == '[]':
                    continue
                recipe = ast.literal_eval(d[7])     # list
                # process

                if d[8] == '[]':
                    continue
                recipe_pt = ast.literal_eval(d[8])

            except:
                continue
            
            # ��� �����Ͱ� ������ ��츸 ����
            if not(d[3] == 'X' or d[4] == 'X' or d[5] == 'X'):
                newDt.append([d[0], d[1], dish, d[3], d[4], d[5], ingreds, recipe, recipe_pt])

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