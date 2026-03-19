import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import time

print("🧠 Loading Edge Vision Model (Moondream2)...")
print("This might take a minute the first time as it downloads the model weights.")

# 1. Load the Model and Tokenizer
model_id = "vikhyatk/moondream2"
revision = "2024-08-26" # Using a stable, optimized revision

tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
moondream = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)

# Optimize for your local GPU
moondream.eval()

# 2. Create a Dummy Image (Just for our first test)
# We will create a simple red square to prove the pipeline works
print("\n📸 Creating test image...")
img = Image.new('RGB', (400, 400), color = 'red')
img.save('test_image.jpg')

# 3. Analyze the Image
prompt = "What color is this image?"
print(f"❓ Question: {prompt}")

start_time = time.time()
# Encode the image and generate the answer
encoded_image = moondream.encode_image(img)
answer = moondream.answer_question(encoded_image, prompt, tokenizer)
end_time = time.time()

print(f"\n🤖 Answer: {answer}")
print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")