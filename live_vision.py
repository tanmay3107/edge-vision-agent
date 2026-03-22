import cv2
import torch
from transformers import AutoModelForCausalLM
from PIL import Image
import time

print("🧠 Booting up Edge Vision Agent...")

# 1. Load model with float16 for massive speedup on RTX 3050 Ti
model_id = "vikhyatk/moondream2"
moondream = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    revision="2025-01-09",
    torch_dtype=torch.float16, # 🚀 SPEED BOOST MAGIC
    device_map={"": "cuda"}
)

# 2. Open the Webcam
cap = cv2.VideoCapture(0) # '0' is usually your default laptop camera

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

# Give the Agent a Mission
MISSION_PROMPT = "Is there a smartphone or cell phone in this image? Answer only YES or NO."

print("🎥 Security Webcam active!")
print(f"🕵️ Agent Mission: {MISSION_PROMPT}")
print("👉 Press 'SPACEBAR' to scan the area.")
print("👉 Press 'q' to quit.")

# The Action Function
def trigger_security_alert():
    print("🚨 [ALERT] UNAUTHORIZED PHONE DETECTED! 🚨")
    print("📝 Logging incident to file...")
    with open("security_log.txt", "a") as f:
        f.write(f"Incident logged at: {time.ctime()} - Phone detected in restricted area.\n")

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret: 
        break

    # Show the camera feed on screen
    cv2.imshow('Edge Vision Agent - Security Mode', frame)
    
    # Check for key presses
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break # Quit
        
    elif key == 32: # SPACEBAR pressed
        print("\n📸 Scanning area...")
        
        # OpenCV uses BGR colors, but the AI expects RGB. We must convert it!
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        start_time = time.time()
        
        # We use a strict prompt to force a binary decision
        result = moondream.query(pil_image, MISSION_PROMPT)
        answer = result['answer'].strip().upper()
        
        end_time = time.time()

        print(f"🤖 Agent Decision: {answer} (Took {end_time - start_time:.2f}s)")

        # The Agent's "Brain" - Deciding to take action
        if "YES" in answer:
            trigger_security_alert()
        else:
            print("✅ Area clear. No action taken.")

# Cleanup
cap.release()
cv2.destroyAllWindows()