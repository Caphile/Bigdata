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
            dishName = re.sub('[^a-zA-Z0-9\s\uAC00-\uD7AF]', '', dishName)  # 특수문자 제거
            if ingred in dishName and tagging.pos(dishName)[0][1] == 'NNP':
                dishNameList.append(dishName)
    dishNameList = list(set(dishNameList))
    return dishNameList

def process():
    os.system('cls')
    print('재료사전 선택')
    ingreds_ds = []
    fp, fn = utils.filePaths(2) # 재료사전 파일 읽기
    for p, n in zip(fp, fn): 
        ingreds_df = utils.readFile(p, n, 2)
        ingreds_ds += ingreds_df.values.tolist()[1 : ]

    opt = 2     # 수동, 자동
    if opt == 1:
        print('\n빈도수 제한 : ', end = '')
        limit = int(input())
    else:
        limit = 20
    ingreds_ds = [ingreds_ds[i][0] for i in range(len(ingreds_ds)) if ingreds_ds[i][1] >= limit]
    ingreds_ds += utils.readFile(os.getcwd(), '3. Ingreds.txt')


    print('\n엑셀파일 선택(여러개 선택 가능)')
    print('필터링된 데이터 선택\n')
    fp, fn = utils.filePaths(2) # 요리명을 추출할 엑셀파일 열기
    for p, n in zip(fp, fn): 
        df = utils.readFile(p, n, 2)
        ds = df.values.tolist()[1 : ]

        newDt = []
        for d in ds:
            # 요리명
            dish = d[2]

            tempDish = []
            doc = model(dish)
            for entity in doc.ents:
                if entity.label_ == 'DISH':
                    tempDish.append(entity.text)

            dish = ' '.join(tempDish)

            # 재료
            ingreds = d[6]



            # 레시피
            recipe = d[7]
            recipe = rs.process(recipe)
            
            # 모든 데이터가 온전한 경우만 저장
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