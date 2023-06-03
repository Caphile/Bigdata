# -*- coding: cp949 -*-

from collections import Counter
import numpy as np
import ast, os
import utils

def process1():
    print('��� ���� ����')
    #N = utils.Normalize()

    fp, fn = utils.filePaths(2)
    for p, n in zip(fp, fn): 
        data = utils.readFile(p, n, 2).values.tolist()
        
        # filter
        subDt = []
        for d in data:
            minT = d[4].find('��')
            if minT != -1 and int(d[4][ : minT]) <= 30 and d[5] in ['�ƹ���', '�ʱ�']:   # 30�� �̳� + �ƹ���, �ʱ� ���̵�
                if d[3] != 'X' and int(d[3][0]) <= 3:                   # 3�κ� �̳�
                    subDt.append(d)

        utils.saveFile(os.getcwd(), f'1_{n}', subDt, 2, ['Key', '���λ���', '�丮��', '�κ�', '�ҿ�ð�', '���̵�', '���', '������', '��������'])

        opt = 0
        if opt == 1:    # ���͸� ����
            subDt = np.array(subDt)
        else:           # ���͸� ������
            subDt = np.array(data)
        ingred = np.transpose(subDt[ : , 6 : 7]).tolist()[0]
        ingred_dict = []
        for i in ingred:
            try:
                ingred_dict.append(ast.literal_eval(i))
            except:
                continue

        ingreds = []
        conds = []
        for ingr in ingred_dict:
            for i in ingr:
                if i == []:
                    continue
                attr = i[0]
                if attr == '���':
                    ingreds.append(i[1])
                elif attr == '���':
                    conds.append(i[1])

        # normalize �����
        '''
        for i in ingred_dict:
            for j in i:
                ingred = N.process(' '.join(j)).split()
                ingreds.append(''.join(ingred))
        '''
        dt = []
        counts = Counter(ingreds)

        counts_key = list(counts.keys())
        counts_val = list(counts.values())
        for i in range(len(counts_key)):
            dt.append([counts_key[i], counts_val[i], '���'])  

        counts = Counter(conds)

        counts_key = list(counts.keys())
        counts_val = list(counts.values())
        for i in range(len(counts_key)):
            dt.append([counts_key[i], counts_val[i], '���'])

        dt.sort(key = lambda x : x[1], reverse = True)
        utils.saveFile(os.getcwd(), f'2_{n}', dt, 2, ['���', '�󵵼�', '�Ӽ�'])

def process2():
    ingreds = [[], []]
    counts = [[], []]
    fp, fn = utils.filePaths(2)
    for p, n in zip(fp, fn): 
        data = utils.readFile(p, n, 2).values.tolist()

        for d in data:
            d = np.array(d).transpose().tolist()

            # ������ ���� ����
            #for i in range(len(d[0])):
            #    d[0][i] = d[0][i].replace(' ', '')

            i = d[0]
            c = d[1]
            a = d[2]
            if a == '���':
                opt = 0
            elif a == '���':
                opt = 1
            
            if i in ingreds[opt]:
                idx = ingreds[opt].index(i)
                counts[opt][idx] += int(c)
            else:
                ingreds[opt].append(i)
                counts[opt].append(int(c))

    op = False
    newData = []
    if op:          # ��� ��� �޾Ҵ� ��� ������� �ѱ��
        for o, a in enumerate(['���', '���']):
            for i, c in zip(ingreds[o], counts[o]):
                newData.append([i, c, a])
    else:         
        for i, c in zip(ingreds[0], counts[0]):
            if i in ingreds[1]:
                idx = ingreds[1].index(i)
                if c <= counts[1][idx]:
                    newData.append([i, c + counts[1][idx], '���'])
                else:
                    newData.append([i, c + counts[1][idx], '���'])
            else:
                newData.append([i, c, '���'])
        for i, c in zip(ingreds[1], counts[1]):
            if i not in ingreds[0]:
                newData.append([i, c, '���'])

    newData = sorted(newData, key = lambda x: x[1], reverse=True)
    utils.saveFile(os.getcwd(), '������.xlsx', newData, 2, ['���', '�󵵼�', '�Ӽ�'])

print('1. �ҿ�ð�, ���̵� ���͸� �� ��� �󵵼�')
print('2. ��� �󵵼� ����')
print('���� :', end = ' ')
n = int(input())

if n == 1:
    process1()
elif n == 2:
    process2()