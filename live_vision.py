# live_vision.py
import cv2
import torch
import time
import os
from transformers import AutoModelForCausalLM
from PIL import Image

# Import our new database layer
from database import SessionLocal, ThreatLog

print("🧠 Booting up Edge Vision Agent...")

# Ensure the evidence directory exists
EVIDENCE_DIR = "captured_frames"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# 1. Load model with float16 for massive speedup
model_id = "vikhyatk/moondream2"
moondream = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    revision="2025-01-09",
    torch_dtype=torch.float16,
    device_map={"": "cuda"}
)

# 2. Open the Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("\n🎥 Security Webcam active!")
print("🕵️ Agent Mission: Detect phones and describe the scene.")
print("👉 Press 'SPACEBAR' to scan the area.")
print("👉 Press 'q' to quit.")

# Open a database session
db = SessionLocal()

# The Action Function (Upgraded to use SQLite and save images)
def trigger_security_alert(evidence_description, frame_to_save):
    print("🚨 [ALERT] UNAUTHORIZED PHONE DETECTED! 🚨")
    
    # 1. Save the visual evidence
    timestamp_str = time.strftime("%Y%m%d-%H%M%S")
    image_filename = f"threat_{timestamp_str}.jpg"
    image_filepath = os.path.join(EVIDENCE_DIR, image_filename)
    cv2.imwrite(image_filepath, frame_to_save)
    
    # 2. Log to Database
    print("📝 Committing incident and evidence to SQLite database...")
    new_log = ThreatLog(
        threat_type="phone",
        is_threat=True,
        context_string=evidence_description,
        image_path=image_filepath
    )
    
    db.add(new_log)
    db.commit()
    print("✅ Database commit successful.")
    print("-" * 40)

while True:
    ret, frame = cap.read()
    if not ret: 
        break

    cv2.imshow('Edge Vision Agent - Security Mode', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break 
        
    elif key == 32: # SPACEBAR
        print("\n📸 Scanning area...")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        start_time = time.time()
        
        # Query 1: Get the general description
        print("🔍 Generating scene description...")
        desc_result = moondream.query(pil_image, "Describe what you see in this image in one short sentence.")
        description = desc_result['answer'].strip()

        # Query 2: Get the strict YES/NO decision
        print("🕵️ Checking for unauthorized devices...")
        sec_result = moondream.query(pil_image, "Is there a smartphone or cell phone in this image? Answer only YES or NO.")
        decision = sec_result['answer'].strip().upper()
        
        end_time = time.time()

        print(f"\n👁️  Scene: {description}")
        print(f"🤖 Agent Decision: {decision} (Total time: {end_time - start_time:.2f}s)")

        # The Agent's "Brain" - Deciding to take action
        if "YES" in decision:
            # Pass both the description and the raw frame to the alert function
            trigger_security_alert(description, frame)
        else:
            print("✅ Area clear. No action taken.")

# Cleanup
db.close()
cap.release()
cv2.destroyAllWindows()