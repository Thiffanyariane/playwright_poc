import os
import re
from util import DiretorioUtil
import cv2
import pytesseract
import logging


def extract_captcha_text(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 10:
                cv2.drawContours(opening, [c], -1, (0, 0, 0), -1)

        result = 255 - opening
        median = cv2.medianBlur(result, 3)

        resultado = pytesseract.image_to_string(median)

        numeros = re.findall(r'\d', resultado)

        return ''.join(numeros)
    except Exception as ex:
        logging.error(ex, 'get_captcha')
        raise Exception


def saveImg(image, name, db_name, ext='.png'):
    try:
        DiretorioUtil.createDir(os.getcwd() + "/imgs/" + db_name)
        with open("imgs/" + db_name + "/" + name + ext, 'wb')as f:
            f.write(image)
    except Exception as ex:
        logging.error(ex, 'saveImg')
        raise Exception
