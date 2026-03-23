# EdgeVision Security Agent 👁️🛡️

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Model](https://img.shields.io/badge/Model-Moondream2_VLM-purple)
![Hardware](https://img.shields.io/badge/Optimized_For-4GB_VRAM-green)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Offline-red)

An autonomous, multimodal security agent that runs entirely offline on consumer edge hardware. By combining a Vision-Language Model (VLM) with live computer vision (OpenCV), this agent monitors a physical space, detects unauthorized devices (e.g., smartphones), and generates highly descriptive, context-aware audit logs.



---

## 🚀 The Problem & Solution

* **The Problem:** Traditional security cameras rely on basic motion detection (triggering false alarms) or send sensitive video feeds to cloud APIs for analysis (violating privacy).
* **The Solution:** EdgeVision brings the reasoning capabilities of a Large Language Model directly to the camera. It processes frames locally, understands the context of the scene, and logs specific threats without a single pixel leaving the device.

---

## ✨ Key Features

1.  **Dual-Query Reasoning:** The agent doesn't just return "YES" or "NO". It runs two parallel queries on the same frame:
    * *Query 1:* Analyzes the scene and generates a descriptive string.
    * *Query 2:* Performs strict binary classification for the security threat.
2.  **Context-Aware Logging:** Security events are logged to a local `.txt` file along with the AI-generated context of the suspect/scene.
3.  **FP16 Hardware Optimization:** The model is optimized using `torch.float16` and the `accelerate` library, allowing a 2-billion parameter VLM to run smoothly on a standard 4GB VRAM GPU (NVIDIA RTX 3050 Ti).

---

## 🛠️ Tech Stack

* **Vision-Language Model:** `vikhyatk/moondream2` (2025-01-09 Architecture)
* **Computer Vision:** `OpenCV` (Live Webcam Feed Processing)
* **Deep Learning Framework:** `PyTorch` & `Hugging Face Transformers`
* **Memory Management:** `Accelerate` (For dynamic GPU offloading)
* **Image Processing Engine:** `pyvips`

---

## 📂 Project Structure

```text
edge-vision-agent/
├── live_vision.py         # Main application script (Webcam + Agent Logic)
├── security_log.txt       # Auto-generated audit trail for detected threats
└── README.md              # Project documentation
```

---

## 💻 Installation & Setup

### Prerequisites
* Anaconda (Python 3.10+)
* NVIDIA GPU (Minimum 4GB VRAM) with CUDA installed.

### 1. Create the Environment
```bash
conda create -n vision-agent python=3.10 -y
conda activate vision-agent
```

### 2. Install Dependencies
```bash
# Core Machine Learning & Vision Libraries
pip install torch torchvision transformers pillow opencv-python accelerate

# Windows-Specific Image Processing Engine (Fixes DLL errors)
pip install pyvips-binary pyvips
```

---

## 🏃‍♂️ Usage

Run the main agent script from your terminal:

```bash
python live_vision.py
```

### Controls:
* **`SPACEBAR`**: Triggers the agent to snap a frame, analyze the scene, and evaluate the threat condition.
* **`q`**: Quits the application and safely releases the webcam.

---

## 📝 Example Output Log (`security_log.txt`)

When the agent detects an unauthorized device, it automatically generates an audit trail like this:

```text
[Sun Mar 22 18:31:01 2026] ALERT: Phone detected.
   Context: A person holds a black phone displaying the word "DEADLY" and a picture of a man's face, with a serious expression.
----------------------------------------
```