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
    torch_dtype=torch.float16, # <--- 🚀 SPEED BOOST MAGIC
    device_map={"": "cuda"}
)

# 2. Open the Webcam
cap = cv2.VideoCapture(0) # '0' is usually your default laptop camera

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("🎥 Webcam active!")
print("👉 Press 'SPACEBAR' to analyze the current frame.")
print("👉 Press 'q' to quit.")

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Show the camera feed on screen
    cv2.imshow('Edge Vision Agent', frame)
    
    # Check for key presses
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break # Quit
        
    elif key == 32: # SPACEBAR pressed
        print("\n👀 Snapped a photo! Analyzing...")
        
        # OpenCV uses BGR colors, but the AI expects RGB. We must convert it!
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        # Ask the AI what it sees
        prompt = "Describe what you see in this image in one short sentence."
        
        start_time = time.time()
        result = moondream.query(pil_image, prompt)
        end_time = time.time()

        print(f"🤖 Agent: {result['answer']}")
        print(f"⏱️ Speed: {end_time - start_time:.2f} seconds")

# Cleanup
cap.release()
cv2.destroyAllWindows()