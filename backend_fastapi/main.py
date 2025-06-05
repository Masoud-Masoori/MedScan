from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ScanRequest(BaseModel):
    image: str

@app.post("/api/scan")
def scan_pill(data: ScanRequest):
    return {"pill": "Aspirin 100mg", "confidence": "92%"}
