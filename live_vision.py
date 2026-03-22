import cv2
import torch
from transformers import AutoModelForCausalLM
from PIL import Image
import time

print("🧠 Booting up Edge Vision Agent...")

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

# The Action Function (Now accepts the description as evidence!)
def trigger_security_alert(evidence_description):
    print("🚨 [ALERT] UNAUTHORIZED PHONE DETECTED! 🚨")
    print("📝 Logging incident and evidence to file...")
    with open("security_log.txt", "a") as f:
        f.write(f"[{time.ctime()}] ALERT: Phone detected.\n")
        f.write(f"   Context: {evidence_description}\n")
        f.write("-" * 40 + "\n")

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
            trigger_security_alert(description)
        else:
            print("✅ Area clear. No action taken.")

# Cleanup
cap.release()
cv2.destroyAllWindows()