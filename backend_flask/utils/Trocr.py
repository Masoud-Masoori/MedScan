from ultralytics import YOLO
import cv2
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import os


model = YOLO("../runs/detect/ocr_91percent2/weights/best.pt")


img_path = "../ocr_test/good/3.png"
image = cv2.imread(img_path)


results = model(image)[0]


sorted_boxes = sorted(results.boxes, key=lambda b: (b.xyxy[0][1].item(), b.xyxy[0][0].item()))


processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")


def preprocess_image(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    adaptive = cv2.adaptiveThreshold(blur, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 3)
    return cv2.cvtColor(adaptive, cv2.COLOR_GRAY2RGB)  # TrOCR expects RGB

# === OCR each sorted bounding box ===
ocr_results = []

for box in sorted_boxes:
    if box.conf[0] < 0.1:
        continue  # Skip low-confidence boxes

    x1, y1, x2, y2 = map(int, box.xyxy[0])
    crop = image[y1:y2, x1:x2]
    crop = preprocess_image(crop)

    pil_img = Image.fromarray(crop)
    pixel_values = processor(images=pil_img, return_tensors="pt").pixel_values
    generated_ids = trocr_model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    if text:
        ocr_results.append(text)

# === Save to corpus (avoid duplicates) ===
corpus_path = "../OCR/corpus/ocr_corpus.txt"

# Load existing lines
if os.path.exists(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        existing_lines = set(line.strip() for line in f)
else:
    existing_lines = set()

# Append only new entries
with open(corpus_path, "a", encoding="utf-8") as f:
    for entry in ocr_results:
        if entry not in existing_lines:
            f.write(entry + "\n")

print("Raw OCR results saved to plain-text corpus (duplicates removed).")
