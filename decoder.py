import easyocr
import cv2
import numpy as np


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def convert(image_file):
    img = cv2.resize(image_file, (1920, int(1920 / image_file.shape[1] * image_file.shape[0])))
    img_blur_11 = cv2.GaussianBlur(img, (13, 13), 0)
    img_c = apply_brightness_contrast(img_blur_11, contrast=10, brightness=-64)
    return img_c


def convert_pic(image_file):
    image = np.asarray(bytearray(image_file), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    img = convert(image)

    reader = easyocr.Reader(['ru', 'en'], gpu=False)
    result = reader.readtext(img, detail=1)

    result2 = []
    if len(result) == 0:
        return '"Ничего"', '"Ничего"'
    for i in result:
        t = i[1].replace(' ', '')
        t = t.replace('^', 'Л')
        t = t.upper()
        result2.append(t)

    en = 0
    ru = 0
    num = 0
    for word in result2:
        for letter in word:
            if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                en += 1
            elif letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
                ru += 1
            else:
                num += 1

    result3 = []
    result4 = []

    if (en > ru) & (en > num):
        reader_en = easyocr.Reader(['en'], gpu=False)
        result_en = reader_en.readtext(img, detail=0)
        lang = 'Английский'
        if len(result_en) > 1:
            for i in result_en:
                t = i.replace(' ', '')
                result3.append(t)
        else:
            result3 = result_en
        for i in result3:
            t = i.replace('0', 'O')
            t = t.upper()
            result4.append(t)
    elif (ru >= en) & (ru >= num):
        reader_ru = easyocr.Reader(['ru'], gpu=False)
        result_ru = reader_ru.readtext(img, detail=0)
        lang = 'Русский'
        if len(result_ru) > 1:
            for i in result_ru:
                t = i.replace(' ', '')
                result3.append(t)
        else:
            result3 = result_ru
        for i in result3:
            t = i.replace('^', 'Л')
            t = t.replace('0', 'O')
            t = t.replace('3', 'З')
            t = t.upper()
            result4.append(t)
    elif (num >= ru) & (num >= en):
        reader_en = easyocr.Reader(['en'], gpu=False)
        result_en = reader_en.readtext(img, detail=0)
        lang = 'Цифры'
        if len(result_en) > 1:
            for i in result_en:
                t = i.replace(' ', '')
                result3.append(t)
        else:
            result3 = result_en
        for i in result3:
            t = i.upper()
            result4.append(t)
    decode = ''
    for i in result4:
        decode = decode + ' ' + i
    return decode, lang
