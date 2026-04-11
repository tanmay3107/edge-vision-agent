# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import base64
import io
import time
import os
from PIL import Image
from transformers import AutoModelForCausalLM

# Import our database layer
from database import SessionLocal, ThreatLog

# Setup directories
EVIDENCE_DIR = "captured_frames"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# Define what our incoming JSON request should look like
class ImagePayload(BaseModel):
    image_base64: str

app = FastAPI(title="EdgeVision AI Server", version="1.0")

# Global variables for our model
moondream = None

@app.on_event("startup")
def load_model():
    """Loads the heavy VLM into the GPU when the server starts."""
    global moondream
    print("🧠 Booting up EdgeVision AI Engine (FastAPI)...")
    model_id = "vikhyatk/moondream2"
    moondream = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        revision="2025-01-09",
        torch_dtype=torch.float16,
        device_map={"": "cuda"}
    )
    print("✅ Model loaded into VRAM. Server ready for requests.")

@app.post("/api/v1/analyze")
async def analyze_frame(payload: ImagePayload):
    """Endpoint that receives an image and returns a threat assessment."""
    start_time = time.time()
    
    try:
        # 1. Decode the base64 string back into a PIL Image
        image_data = base64.b64decode(payload.image_base64)
        pil_image = Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format.")

    # 2. Run Query 1: Scene Description
    desc_result = moondream.query(pil_image, "Describe what you see in this image in one short sentence.")
    description = desc_result['answer'].strip()

    # 3. Run Query 2: Threat Detection
    sec_result = moondream.query(pil_image, "Is there a smartphone or cell phone in this image? Answer only YES or NO.")
    decision = sec_result['answer'].strip().upper()
    is_threat = "YES" in decision

    # 4. Handle Logging if a threat is detected
    image_filepath = None
    if is_threat:
        # Save the image to disk
        timestamp_str = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"threat_api_{timestamp_str}.jpg"
        image_filepath = os.path.join(EVIDENCE_DIR, image_filename)
        pil_image.save(image_filepath)

        # Log to SQLite
        db = SessionLocal()
        new_log = ThreatLog(
            threat_type="phone",
            is_threat=True,
            context_string=description,
            image_path=image_filepath
        )
        db.add(new_log)
        db.commit()
        db.close()
        print(f"🚨 ALERT LOGGED: {description}")

    # 5. Return structured JSON to the client
    return {
        "is_threat": is_threat,
        "context": description,
        "processing_time_seconds": round(time.time() - start_time, 2),
        "evidence_saved": bool(image_filepath)
    }