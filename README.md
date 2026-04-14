# EdgeVision Security Agent 👁️🛡️

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Architecture](https://img.shields.io/badge/Architecture-Decoupled_Microservice-orange)
![Model](https://img.shields.io/badge/Model-Moondream2_VLM-purple)
![Hardware](https://img.shields.io/badge/Optimized_For-4GB_VRAM-green)
![Deployment](https://img.shields.io/badge/Deployment-Docker-2496ED)

An autonomous, multimodal edge security pipeline designed to run entirely offline. EdgeVision decouples computer vision motion detection from a heavy Vision-Language Model (VLM) inference engine. It detects physical intrusions, analyzes the scene contextually, and persists visual evidence to a local relational database.

**Author:** Tanmay Janak

---

## 🚀 System Architecture

Unlike traditional monolithic scripts, EdgeVision utilizes a **Client-Server Microservice Architecture**:
1. **The Edge Client (`edge_client.py`):** A lightweight OpenCV script that monitors a webcam feed for physical motion. When movement is detected, it captures a frame, encodes it, and sends it via HTTP POST.
2. **The Inference API (`server.py`):** A FastAPI backend that hosts a 2-billion parameter VLM (Moondream2). It receives frames, runs dual-query analysis (scene description + threat classification), and logs incidents.
3. **The Data Layer (`database.py`):** An SQLAlchemy-managed SQLite database that persistently stores event timestamps, AI-generated context strings, and file paths to saved visual evidence.

---

## ✨ Key Engineering Features

* **Decoupled Deployment:** The camera client and the AI server operate independently, allowing the camera to run on low-power IoT devices while the server runs on a centralized GPU.
* **FP16 Hardware Optimization:** The massive VLM is explicitly constrained using `torch.float16` and dynamic device mapping, allowing it to run smoothly on standard consumer hardware (e.g., an NVIDIA RTX 3050 Ti with 4GB VRAM).
* **Dual-Query Reasoning:** Runs two parallel zero-shot prompts per frame to minimize false positives:
    * *Query 1:* Contextual scene description.
    * *Query 2:* Strict binary classification for unauthorized devices/entities.
* **Evidence Persistence:** Automatically saves the exact frame that triggered the alert to disk, linking the image path directly to the SQLite database entry.
* **Containerized Backend:** The API and AI engine are fully containerized via Docker for hardware-agnostic deployment.

---

## 🛠️ Tech Stack

* **Machine Learning:** `PyTorch`, `Hugging Face Transformers`, `Accelerate`
* **Vision-Language Model:** `vikhyatk/moondream2` (2025-01-09 Revision)
* **Backend Framework:** `FastAPI`, `Uvicorn`, `Pydantic`
* **Database:** `SQLite`, `SQLAlchemy` (ORM)
* **Computer Vision:** `OpenCV` (Motion Detection & Frame Processing)
* **DevOps:** `Docker`

---

## 📂 Repository Structure

```text
edge-vision-agent/
├── captured_frames/       # Directory generated at runtime to store visual evidence
├── database.py            # SQLAlchemy ORM schemas and DB initialization
├── Dockerfile             # Container configuration for the AI Server
├── edge_client.py         # Lightweight OpenCV motion detector and API caller
├── requirements.txt       # Python dependencies
└── server.py              # FastAPI application and Moondream2 inference logic
```

---

## 💻 Local Setup & Execution

### Prerequisites
* NVIDIA GPU (Minimum 4GB VRAM) with CUDA installed.
* Python 3.10+

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the AI Server (Terminal 1)
Boot up the FastAPI server. This will load the Moondream2 model into your GPU VRAM.
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```
*Wait until the console outputs: `Application startup complete.`*

### 3. Start the Edge Client (Terminal 2)
In a separate terminal window, launch the lightweight camera client to begin motion tracking.
```bash
python edge_client.py
```

---

## 🐳 Docker Deployment (Server)

To deploy the inference engine in an isolated container with GPU passthrough:

1. Build the Docker image:
```bash
docker build -t edgevision-server .
```

2. Run the container (Requires NVIDIA Container Toolkit):
```bash
docker run --gpus all -p 8000:8000 edgevision-server
```

---

## 📝 Example Database Record

When motion triggers an alert, the AI logs a structured record into the `threat_logs` SQLite table:

| id | timestamp | threat_type | is_threat | context_string | image_path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 2026-04-14 18:31:01 | phone | TRUE | A person holds a black phone displaying the word "DEADLY"... | captured_frames/threat_api_20260414-183101.jpg |