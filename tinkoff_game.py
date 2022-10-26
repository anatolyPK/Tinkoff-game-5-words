import time
import pyautogui
import pymysql.cursors
import random
import cv2
from config import db_name, user,  password, host


def data_base_choose():
    '''Выбирает существительные из 5 символов в единственном числе и формирует текстовый файл words.txt'''
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            port=3306,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT word FROM nouns_morf WHERE CHAR_LENGTH(word)= 5 AND wcase='им' AND plural=0")
                rows = cursor.fetchall()
                with open('words.txt', 'w',  encoding='utf-8') as file:
                    for row in rows:
                        file.write(f"{row['word']}\n")
        finally:
            connection.close()
    except:
        print('fail')


def choose_random_word():
    with open('words.txt', 'r', encoding='utf-8') as f:
        words = [line[:-1] for line in f]
        while True:
            word = random.choice(words)
            if len(set(word)) == 5:
                return word[:], words


def phone_actions_test(word, word_example):
    ''' Принмает слово, вводит его, считывает типы букв. Возвращает три списка с буквами и местами'''
    black, grey, yellow = [], [], []
    for i in range(len(word)):
        flag_add = 0
        for k in range(len(word_example)):
            if i == k and word[i] == word_example[k]:
                yellow.append((i, word[i]))
                flag_add += 1
                break
            elif word[i] == word_example[k]:
                grey.append((i, word[i]))
                flag_add += 1
                break
        if flag_add == 0:
            black.append(word[i])
    return black, list(set(grey)), yellow, True if word == word_example else False


def choose_word(words, black, grey, yellow):
    '''Принимает списки и отсеивает лишние слова из списка'''
    new_words = []
    for i in range(len(words)):
        word = words[i]
        count_yellow,  count_gray = 0, 0
        exit_flag = False
        flag_check = True

        for k in range(len(word)):
            if word[k] in black: #black
                exit_flag = True
                break

            for n in range(len(grey)): #grey
                if word[k] == grey[n][1] and k != grey[n][0]:
                    count_gray += 1

            for n in range(len(yellow)): #yellow
                if word[k] == yellow[n][1] and k == yellow[n][0]:
                    count_yellow += 1

        check = [grey[z][1] for z in range(len(grey))] + [yellow[z][1] for z in range(len(yellow))]
        for x in range(len(check)):
            if check[x] not in set(word):
                flag_check = False

        if count_gray >= len(grey) and count_yellow == len(yellow) and exit_flag is False and flag_check:
            new_words.append(word)
    return new_words


def input_word_in_form(word):
    symbols = 'йцукенгшщзхъфывапролджэячсмитьбю'
    with open('position_keyboards_symbols.txt', 'r') as f:
        coord = [(int(line[line.find('=')+1:line.find(',')]), int(line[line.find('y=')+2:line.find(")")])) for line in f]

    for symb in word:
        pyautogui.click(coord[symbols.find(symb)])
        time.sleep(2)

    if check_enter():
        print('ENTER')
        pyautogui.click(767, 941)
    else:
        print('ENTER NOT READY')
        delete_word()
        input_word_in_form(word)

    while check_ready_input() is False:
        time.sleep(2)


def delete_word():
    for x in range(5):
        pyautogui.click(1153, 941)
        time.sleep(2)


def check_enter():
    img = screen()
    b, g, r = img[951, 784]
    return True if 20 < b < 50 and 150 < g < 240 and 200 < r < 256 else False


def check_ready_input():
    img = screen()
    b, g, r = img[951, 756]
    return True if b == g and g == r else False


def screen():
    pyautogui.screenshot('screens/my_screenshot_test.png')
    return cv2.imread('screens/my_screenshot_test.png')


def check_each_symbol(img, word, counter):
    with open('position_each_box.txt', 'r') as f:
        coord = [(int(line[line.find('=')+1:line.find(',')]), int(line[line.find('y=')+2:line.find(")")])) for line in f]

    black, grey, yellow = [], [], []
    count = 0
    for i in range(5 * counter, 5 * counter + 5):
        b, g, r = img[coord[i][1], coord[i][0]]
        if 30 < b < 45 and 150 < g < 210 and 215 < r < 256:
            yellow.append((count, word[count]))
        elif b > 150 and b == g and g == r:
            grey.append((count, word[count]))
        else:
            black.append(word[count])
        count += 1
    print(f'Yellow - {yellow}')
    print(f'Grey  - {grey}')
    print(f'Black - {black}')
    return black, grey, yellow, True if len(yellow) == 5 else False


def main():
    word, words = choose_random_word()
    for step in range(6):
        input_word_in_form(word)
        black, grey, yellow, out = check_each_symbol(screen(), word, step)
        words = choose_word(words, black, grey, yellow)
        print(f'Количество оставшихся слов - {len(words)}')
        word = random.choice(words)
        if out:
            return print('Изи!')


if __name__ == '__main__':
    main()
