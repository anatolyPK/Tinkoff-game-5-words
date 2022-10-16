import pymysql.cursors, random
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
        words = []
        for line in f:
            words.append(line[:-1])
        while True:
            word = random.choice(words)
            if len(set(word)) == 5:
                return word[:], words


def phone_actions(word):
    ''' Принмает слово, вводит его, считывает типы букв. Возвращает три списка с буквами и местами'''
    word_example = 'опись'
    black, grey, yellow = [], [], []
    for i in range(len(word)):
        flag_add = 0
        for k in range(len(word_example)):
            if i == k and word[i] == word_example[k]:
                yellow.append((i, word[i]))
                flag_add += 1
            elif word[i] == word_example[k]:
                grey.append((i, word[i]))
                flag_add += 1
        if flag_add == 0:
            black.append(word[i])
    return black, grey, yellow


def choose_word(words, black, grey, yellow, word):
    '''Принимает списки и отсеивает лишние слова из списка'''
    new_words = []
    for i in range(len(words)):
        word = words[i]
        flag_append = False

        for k in range(len(word)):
            if word[k] in black: #black
                break


            for n in range(len(grey)): #grey
                if word[k] == grey[n][1] and k != grey[n][0]:
                    flag_append = True

            for n in range(len(yellow)): #yellow
                if word[k] == yellow[n][1] and k == yellow[n][0]:
                    flag_append = True
                else:
                    flag_append = False
                    break


        if flag_append is True:
            new_words.append(word)
    return new_words


def main():
    # data_base_choose()
    word, words = choose_random_word()
    print(word)
    while True:
        black, grey, yellow = phone_actions(word) #return black, gray and yellow  (1 - а, 3 - c)
        words = choose_word(words, black, grey, yellow, word)  #reurn edited words  !!!!delete word
        word = random.choice(words)

if __name__ == '__main__':
    main()
    