# -*- coding: cp949 -*-

import requests
from bs4 import BeautifulSoup
import os, re
import time
import utils

def getText(param):
    if param:
        return param.text
    return 'X'  # ��������

def trySoup(url):
    tryCount = 5
    while tryCount:
        try:
            content = requests.get(url).content
            return BeautifulSoup(content.decode('utf-8', 'replace'), 'html.parser')
        except:
            tryCount -= 1
            print('\n��Ʈ��ũ Ȯ�� (' + str(tryCount) + ')\n')
            time.sleep(6)

def makeXlsx(dt):
    global xCount, divBy, page
    try:
        folder = os.getcwd() + '/10000recipeData'  # ���� ���� ������
        os.mkdir(folder)
    except:
        pass

    fileName = '/F' + str(xCount * divBy + 1) + '_T' + str(page) + '.xlsx'
    xCount += 1

    retry = 3
    while retry:
        try:
            utils.saveFile(folder, fileName, dt, 2, ['Key', '���λ���', '�丮��', '�κ�', '�ҿ�ð�', '���̵�', '���', '������', '��������'])
            break
        except:
            retry -= 1

page = 0                    # 4/6 ���� 4928�� �ִ�
dCount = 0                  # ���� ������
lCount = 0                  # �ս� ������(���� ����)
divBy = 100                 # ���� ���� ���� ������ ��
xCount = int(page / divBy)  # ������� �������� ��

data = []
is_pages_end = False
while not is_pages_end:
    is_data_apd = False
    page += 1
    url = 'https://www.10000recipe.com/recipe/list.html?order=reco&page=' + str(page)
    try:
        soup = trySoup(url)
        print('������ :', page)

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

                if 'alert' in subSoup.contents[0].text: # ������ ������ ���� ���
                    lCount += 1
                    continue

                mainImg = subSoup.select_one('#main_thumbs')
                mainSrc = mainImg['src']

                title = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > h3'))  # �丮��
                title = re.sub(r'[^a-zA-Z��-����-�Ӱ�-�R0-9\s]+', '', title)

                sumInfo1 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info1'))    # �κ�
                sumInfo2 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info2'))    # �ҿ�ð�
                sumInfo3 = getText(subSoup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info3'))    # ���̵�
                
                ingredInfo = []     # ���&��
                sub_html = subSoup.select_one('#divConfirmedMaterialArea')
                if sub_html != None:
                    ingreds_html = sub_html.contents[1]
                    ingreds = ingreds_html.find_all('a')
                    for i in ingreds[ : : 2]:
                        ingred = ['���'] + i.contents[1].text.split('\n')
                        ingred = [' '.join(igd.split()) for igd in ingred[ : -1]]
                        ingred.remove('����')
                        ingredInfo.append(ingred)

                    if len(ingreds) == 5:   # ���, ��� �� �� �ִ� ���
                        ingreds_html = sub_html.contents[3]
                        ingreds = ingreds_html.find_all('a')
                        for i in ingreds[ : : 2]:
                            ingred = ['���'] + i.contents[1].text.split('\n')
                            ingred = [' '.join(igd.split()) for igd in ingred[ : -1]]
                            ingred.remove('����')
                            ingredInfo.append(ingred)

                # ���Ͽ�(similar) �߰� ?

                recipe = subSoup.select_one('#contents_area')
                recipeLine = recipe.find_all('div', {'id' : re.compile('^stepD')})
                recipeInfo = []     # ������
                recipeIng = []      # ���� ���
                recipeImg = []      # ���� ����

                for c, i in enumerate(recipeLine):
                    fullL = ''
                    for recipeL in i.contents[0].contents:
                        fullL += recipeL.text + ' '
                    recipeInfo.append(f'{c + 1}. {fullL}')

                    if len(i.contents) > 1:
                        imgTag = i.contents[1].find('img')
                        if imgTag != -1:
                            src = imgTag['src']
                            recipeImg.append(f'{c + 1}. {src}')

                subData.append([key, mainSrc, title, sumInfo1, sumInfo2, sumInfo3, ingredInfo, recipeInfo, recipeImg])

            else:
                print('')
                break

        if subData != []:
            data += subData
            dCount += len(subData)
            print('���� ������ �� :', dCount)
            print('���� �ս� ������ �� :', lCount)
            print('========================================================================================================')
            is_data_apd = True

            if not page % divBy:  # divBy ������ ������ ���� ����
                makeXlsx(data)
                data = []

        else:
            is_pages_end = True

            print('�������\n')
            print('��������\n')

    except:
        if not is_data_apd:
            page -= 1
            print('\n�����߻����� ���� ��õ�\n')
        else:
            print('\n�����߻����� ���� ��������\n')

if data != []:
    page -= 1
    makeXlsx(data)

print('���α׷� ����')