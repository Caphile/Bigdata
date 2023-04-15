# -*- coding: cp949 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re

def getText(param):
    if param:
        return param.text
    return 'X'  # 정보없음

def trySoup(url):
    tryCount = 5
    while tryCount:
        try:
            content = requests.get(url).content
            return BeautifulSoup(content, 'html.parser')
        except:
            tryCount -= 1
            print('\n네트워크 확인 (' + str(tryCount) + ')\n')
            time.sleep(6)

def makeXlsx(dt):
    global xCount, divBy, page
    try:
        folder = '10000recipeData'  # 엑셀 저장 폴더명
        os.mkdir(folder)
    except:
        pass

    fileName = folder + '/F' + str(xCount * divBy + 1) + '_T' + str(page) + '.xlsx'
    xCount += 1

    retry = 3
    while retry:
        try:
            df = pd.DataFrame(dt, columns = ['Key', '요리명', '인분', '소요시간', '난이도', '재료', '조리법'])
            df.to_excel(fileName, index = False)
            break
        except:
            retry -= 1

page = 0                    # 4/6 기준 4928이 최대
dCount = 0                  # 누적 데이터
lCount = 0                  # 손실 데이터(삭제 추정)
divBy = 100                 # 엑셀 저장 단위 페이지 수
xCount = int(page / divBy)  # 만들어진 엑셀파일 수

data = []
is_pages_end = False
while not is_pages_end: # 1301~1400, 3501~4929 데이터 남음
    is_data_apd = False
    page += 1
    url = 'https://www.10000recipe.com/recipe/list.html?order=reco&page=' + str(page)
    try:
        soup = trySoup(url)
        print('페이지 :', page)

        idx = 0
        subData = []
        while 1:
            idx += 1
            href = soup.select_one('#contents_area_full > ul > ul > li:nth-child(' + str(idx) + ') > div.common_sp_thumb > a')
            if href:
                print(idx, end = ' ', flush = True)
                key = href.get("href").split('/')[2]
                
                subUrl = 'https://www.10000recipe.com/recipe/' + str(key)
                subSoup = trySoup(subUrl)

                if 'alert' in subSoup.contents[0].text: # 레시피 정보가 없는 경우
                    lCount += 1
                    continue

                title = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > h3'))  # 요리명

                sumInfo1 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info1'))    # 인분
                sumInfo2 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info2'))    # 소요시간
                sumInfo3 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info3'))    # 난이도
                
                ingredInfo = []     # 재료&양
                for i in range(1, 3):
                    ingreds_html = subSoup.select_one('#divConfirmedMaterialArea > ul:nth-child(' + str(i) + ')')
                    if ingreds_html:
                        ingreds = ingreds_html.find_all('a')
                        for i in range(0, len(ingreds), 2):
                            ingred = ingreds[i].text.split()
                            amount = (ingred[2] if len(ingred) > 2 else 'X')   
                            ingredInfo.append({ingred[0] : amount})

                # 노하우(similar) 추가 ?

                recipe = subSoup.select_one('#contents_area')
                recipeLine = recipe.find_all('div', {'id' : re.compile('^stepD')})
                recipeInfo = []     # 조리법
                for c, i in enumerate(recipeLine):
                    recipeInfo.append({c + 1 : i.text})

                subData.append([key, title, sumInfo1, sumInfo2, sumInfo3, ingredInfo, recipeInfo])

            else:
                print('')
                break

        if subData != []:
            data += subData
            dCount += len(subData)
            print('누적 데이터 수 :', dCount)
            print('누적 손실 데이터 수 :', lCount)
            print('========================================================================================================')
            is_data_apd = True

            if not page % divBy:  # divBy 페이지 단위로 엑셀 저장
                makeXlsx(data)
                data = []

        elif not lCount:
            is_pages_end = True

            print('결과없음\n')
            print('수집종료\n')

    except:
        if not is_data_apd:
            page -= 1
            print('\n오류발생으로 인한 재시도\n')
        else:
            print('\n오류발생으로 인한 수집종료\n')

if data != []:
    makeXlsx(data)

print('프로그램 종료')