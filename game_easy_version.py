from tinkoff_game import choose_random_word, choose_word
import random


def main():
    word, words = choose_random_word()  #вечер'
    counter = 0
    while True:
        print(f'Введите слово "{word}". Длина массива - {len(words)}')
        yellow, black, grey = [], [], []
        while True:
            try:
                symbol = input('Введите желтую букву и ее индекс. Если нет - Enter')
                if symbol == '':
                    break
                symbol = symbol.split()
                symbol[1] = int(symbol[1]) - 1
                yellow.append(symbol[::-1])
                print(yellow)
            except:
                print('Попробуйте еще')
        while True:
            try:
                symbol = input('Введите белую букву и ее индекс. Если нет - Enter')
                if symbol == '':
                    break
                symbol = symbol.split()
                symbol[1] = int(symbol[1]) - 1
                grey.append(symbol[::-1])
            except:
                print('Попробуйте еще')
        while True:
            symbol = input('Введите серую букву. Если нет - Enter')
            if symbol == '':
                break
            black.append(symbol.strip())

        words = choose_word(words, black, grey, yellow)
        word = random.choice(words)
        counter += 1
        print(counter)


if __name__ == '__main__':
    main()
