# 1. Use an official NVIDIA CUDA base image (adjust version if needed for your specific PyTorch build)
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install Python, pip, and clean up to keep the image small
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install them
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Copy your server and database logic
COPY server.py database.py ./

# 6. Expose the port your FastAPI server runs on
EXPOSE 8000

# 7. Start the server!
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]