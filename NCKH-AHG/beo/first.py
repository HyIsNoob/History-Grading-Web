import random
from time import sleep

#0 là béo
#1 là kéo
#2 là kiệt
def game():
    computer = random.randint(0, 2)
    print('Nhập kéo búa hay bao gì đó đi thằng lồn kiệt:', end='') 
    a = input()
    sleep(0.5)
    if computer == 0:
        print('Tao chọn Búa')
    elif computer == 1:
        print('Tao chọn Kéo')
    elif computer == 2:
        print('Tao Chọn Bao')
    if "bua" in a:
        a = 0
    elif "keo" in a:
        a = 1
    elif "bao" in a:
        a = 2
    

