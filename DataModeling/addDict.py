# ������ �ܼ� ����� �����Ͽ� ����
# �ܼ��� XŰ�� ���� ������ ������ �� �ȵ� ���� ����
# ����Ű�� ���� ������ ��

from colorama import Fore, Style
import os

filePath = ''
fileName = 'dict.txt'

with open(fileName, 'r+', encoding ='UTF8') as f:
    lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    print('\n')
    while 1:
        print('enter�� ���� ����')
        print('�߰�/������ �ҿ�� �Է� : ', end = '')
        stopW = input()
        if stopW == '':
            break

        os.system('cls')

        if stopW in lines:  # �̹� �����ϸ� ����
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}�� ��Ͽ��� {Fore.RED}����{Style.RESET_ALL}(Y/N)', end = ' ')
            opt = input()
            os.system('cls')
            if opt == 'Y' or opt == 'y':
                lines.remove(stopW)
                print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}�� ��Ͽ��� {Fore.RED}����{Style.RESET_ALL}��\n')
            else:
                continue
        else:
            lines.append(stopW)
            print(f'{Fore.LIGHTBLACK_EX}{stopW}{Style.RESET_ALL}�� ��Ͽ� {Fore.BLUE}�߰�{Style.RESET_ALL}��\n')

        lines.sort()    
        
        f.seek(0)
        f.truncate(0)
        f.write('\n'.join(lines))