import torch
from transformers import AutoModelForCausalLM
from PIL import Image
import time

print("🧠 Loading Edge Vision Model (Moondream2 2025 Version)...")
print("It will download a small update for the new architecture...")

# 1. Load the Model using the newest 2025 revision
model_id = "vikhyatk/moondream2"
revision = "2025-01-09" # The new, updated architecture

moondream = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True, 
    revision=revision,
    device_map={"": "cuda"} 
)

# 2. Create a Dummy Image (A red square)
print("\n📸 Creating test image...")
img = Image.new('RGB', (400, 400), color = 'red')
img.save('test_image.jpg')

# 3. Analyze the Image using the new, simpler .query() API
prompt = "What color is this image? Answer in one word."
print(f"❓ Question: {prompt}")

start_time = time.time()

# The 2025 API handles the image encoding and tokenizing automatically!
result = moondream.query(img, prompt)

end_time = time.time()

print(f"\n🤖 Answer: {result['answer']}")
print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")