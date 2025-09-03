import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output

# If you are on Windows and tesseract.exe is not in PATH, uncomment & set:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image_cv(path, max_width=1500):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    h, w = img.shape[:2]
    if w > max_width:
        scale = max_width / w
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Denoise + adaptive thresholding (works well for scanned docs)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img, th

def extract_text(image_path, lang='eng'):
    """Return full recognized text as a string."""
    # Use PIL image for pytesseract.image_to_string (robust)
    pil_img = Image.open(image_path)
    text = pytesseract.image_to_string(pil_img, lang=lang)
    return text

def extract_boxes(image_path, lang='eng', conf_threshold=30):
    """
    Return bounding boxes with text and confidence:
    [{'text': 'Hello', 'conf': 93, 'box': (x,y,w,h)}, ...]
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=Output.DICT, lang=lang)
    boxes = []
    n = len(data['text'])
    for i in range(n):
        text = data['text'][i].strip()
        conf_str = data['conf'][i]
        try:
            conf = int(float(conf_str))
        except:
            conf = -1
        if text != "" and conf >= conf_threshold:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            boxes.append({'text': text, 'conf': conf, 'box': (x, y, w, h)})
    return boxes

def draw_boxes(image_path, boxes, out_path):
    img = cv2.imread(image_path)
    for item in boxes:
        x, y, w, h = item['box']
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(out_path, img)
    return out_path
