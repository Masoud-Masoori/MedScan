import spacy
import os

medicine="medicine_names"
os.makedirs(medicine, exist_ok=True)


nlp = spacy.load(r"C:\Data\AIG\YOLO\OCR\model\en_ner_bc5cdr_md-0.5.1\en_ner_bc5cdr_md-0.5.1\en_ner_bc5cdr_md\en_ner_bc5cdr_md-0.5.1")

with open("corpus/ocr_corpus.txt", "r", encoding="utf-8") as f:
    # lines = [line.strip() for line in f if line.strip()]
    lines=f.read()

ocr_text = " ".join(lines)


doc = nlp(ocr_text)

# medicine names (label: CHEMICAL)
medicine_names = sorted(set(ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"))

# Save to file
with open("medicine_names/medicine_names.txt", "w", encoding="utf-8") as f:
    for name in medicine_names:
        f.write(name + "\n")

print("✅ Extracted medicine names saved to medicine_names.txt")
