import time
import pyautogui
import cv2
import pytesseract
from PIL import Image
import os
import tinkoff_game


def locate_position():
    with open('position_keyboards_enter.txt', 'a', encoding='utf-8') as file:
        for n in range(32):
            time.sleep(3)
            left_top = pyautogui.position()
            print(left_top)
            # time.sleep(2)
            # right_bot = pyautogui.position()
            # print(right_bot)
            file.write(f"{left_top} \n")


def screen(count, all_picture=None):
    time.sleep(2)
    pyautogui.screenshot('screens/my_screenshot20.png')
    img = loading_displaying_saving()
    return cropping(img, count) if all_picture is not None else img


def cropping(img, count):
    position = [[250, 321, 770, 1150], [335, 410, 770, 1150], [420, 490, 770, 1150], [500, 575, 770, 1150],
                [590, 660, 770, 1150], [670, 745, 770, 1150]]
    coord = position[count]
    return img[coord[0]:coord[1], coord[2]:coord[3]]


def loading_displaying_saving():
    img = cv2.imread('screens/my_screenshot.png')
    # cv2.imshow('my_screenshot', img)
    # cv2.waitKey(0)
    # cv2.imwrite('screens/my_screenshot30.jpg', img)
    # print("Высота:" + str(img.shape[0]))
    # print("Ширина:" + str(img.shape[1]))
    return img


def averaging_blurring(image):
    # image = cv2.imread('girl.jpg')
    img_blur_3 = cv2.blur(image, (3, 3))
    img_blur_7 = cv2.blur(image, (7, 7))
    img_blur_11 = cv2.blur(image, (11, 11))
    cv2.imshow('my_screenshot', img_blur_11)
    cv2.waitKey(0)


def definition_colors(img):
    for y in range(img.shape[0]):
        average_color_b = 0
        average_color_g = 0
        average_color_r = 0

        for x in range(img.shape[1]):
            b, g, r = img[y, x]
            # average_color += (b + g + r) // 3
            average_color_b += b
            average_color_g += g
            average_color_r += r
        print(average_color_b // img.shape[1], average_color_g // img.shape[1], average_color_r // img.shape[1])


def tesser():
    img = cv2.imread('screens/my_screenshot300.jpg')
    preprocess = "blur"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # проверьте, следует ли применять пороговое значение для предварительной обработки изображения

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # если нужно медианное размытие, чтобы удалить шум
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR

    filename = "5.png"
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename), lang='rus')
    os.remove(filename)
    print(text)
    # показать выходные изображения
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.imshow("Output", gray)
    cv2.waitKey(0)


def check_color(step):
    pass

def main():
    # locate_position()
    # for step in range(6):
        # check_color()
    pytesseract.pytesseract.tesseract_cmd = r'D:\TESSERACT\tesseract.exe'
    config = r'--oem 3 --psm 6'
    screen(1)
    # for x in range(1, 6):
    # img = screen(x, 'crop')
    # img = cv2.imread('screens/my_screenshot.png', cv2.COLOR_BGR2RGB)
    # tesser()


if __name__ == '__main__':
    main()