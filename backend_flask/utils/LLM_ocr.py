import cv2
import torch
import json
import requests
from PIL import Image
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# === Load models ===
yolo_model = YOLO("../runs/detect/ocr_91percent2/weights/best.pt")
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten").to("cuda" if torch.cuda.is_available() else "cpu")

# === Preprocess each cropped box ===
def preprocess_image(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    adaptive = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
    return cv2.cvtColor(adaptive, cv2.COLOR_GRAY2RGB)

# === OCR with YOLO + TrOCR ===
def extract_text_from_image(img_path):
    image = cv2.imread(img_path)
    results = yolo_model(image)[0]
    sorted_boxes = sorted(results.boxes, key=lambda b: (b.xyxy[0][1].item(), b.xyxy[0][0].item()))

    texts = []
    for box in sorted_boxes:
        if box.conf[0] < 0.1:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = preprocess_image(image[y1:y2, x1:x2])
        pil_img = Image.fromarray(crop)
        pixel_values = processor(images=pil_img, return_tensors="pt").pixel_values.to(trocr_model.device)
        generated_ids = trocr_model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        if text:
            texts.append(text)
    return texts

# === Ask Ollama via HTTP ===
def ask_ollama(prompt, model="deepseek-llm"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"⚠️ Error contacting Ollama: {e}"


image_path = "../ocr_test/good/9.jpg"
ocr_texts = extract_text_from_image(image_path)

combined_text = " ".join(ocr_texts).replace("smL", "mL").replace("/ ", "/")

print(combined_text)
prompt = f"""
You are a helpful professional medical assistant. Analyze the following prescription text and extract:
1. The medicine name
2. The quantity or dosage
3. Instructions if have
4. Refill 

Return the result as a JSON array like:
[{{"medicine": "Name", "quantity": "Dosage"}}]

Prescription Text:
\"\"\"{combined_text}\"\"\"
"""

response = ask_ollama(prompt)
print("\n🧾 LLM Response:")
print(response)

# Try to parse and show JSON
try:
    start = response.find("[")
    end = response.rfind("]") + 1
    parsed = json.loads(response[start:end])
    print("\n✅ Extracted Medicines and Quantities:")
    for item in parsed:
        print(f"- {item['medicine']}: {item['quantity']}")
except Exception as e:
    print("\n⚠️ Could not parse JSON from response.")
