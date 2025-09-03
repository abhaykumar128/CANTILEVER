import os
from ocr.ocr_utils import extract_text

DATASET = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

for fname in os.listdir(DATASET):
    if fname.lower().endswith((".png",".jpg",".jpeg",".tiff",".bmp")):
        path = os.path.join(DATASET, fname)
        text = extract_text(path)
        outname = fname + ".txt"
        with open(os.path.join(OUT, outname), "w", encoding="utf-8") as f:
            f.write(text)
        print("Processed:", fname)
