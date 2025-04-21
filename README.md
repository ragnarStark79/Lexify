# Chat Enhancer

Chat Enhancer is a powerful text enhancement tool that leverages state-of-the-art AI models to improve the quality of text. It supports both CLI and web interfaces, making it versatile for various use cases. The application integrates with Hugging Face models and MongoDB for logging interactions.

## Features
- Enhance text using AI models from Hugging Face.
- Support for both CLI and web interfaces.
- Log interactions to a MongoDB database.
- Easily configurable to use different models from Hugging Face.
- Feedback mechanism placeholder for future enhancements.

---

## Installation

### Step 1: Clone or Fork the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/your_username/chat_enhancer.git
cd chat_enhancer
```

Alternatively, fork the repository on GitHub and then clone your fork.

### Step 2: Create a Python Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies
Ensure your virtual environment is active, then install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## Setup

### Step 1: Create a `.env` File
Create a `.env` file in the root directory of the project to store environment variables. Below is an example of what to include in the `.env` file:
```plaintext
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<database-name>
HUGGINGFACE_TOKEN=<your_huggingface_token>
```
Replace `<username>`, `<password>`, `<cluster-url>`, `<database-name>`, and `<your_huggingface_token>` with your actual values.

### Step 2: Configure the Database
1. Set up a MongoDB instance (local or cloud).
2. Update the `MONGO_URI` in the `.env` file with your MongoDB connection details.

### Step 3: Hugging Face Setup
#### Install Hugging Face Hub
If not already installed, run:
```bash
pip install huggingface-hub
```

#### Authenticate via Terminal
1. Run the following command:
   ```bash
   huggingface-cli login
   ```
2. Go to your Hugging Face account settings: [Hugging Face Tokens](https://huggingface.co/settings/tokens).
3. Create a new token with at least a 'read' role.
4. Copy the token and paste it into the terminal when prompted.

#### Configure Models
- Open `config.py` and specify the Hugging Face model you want to use.
- Ensure the model size matches your system's capabilities.

#### Request Access for Gated Models (if required)
1. Visit the model page on Hugging Face (e.g., `https://huggingface.co/your_model_location`).
2. Request access by agreeing to the terms and clicking the necessary buttons.
3. Wait for approval and retry running the application after access is granted.

---

## GPU Setup (Optional for Performance)

### For Windows Users
1. Install the appropriate CUDA version for your GPU:
   - Visit the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) page.
   - Download and install the version compatible with your GPU and system.
2. Install the required PyTorch version with CUDA support:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
   ```
   Replace `cu117` with the appropriate CUDA version for your system.

### For macOS Users
1. macOS does not support CUDA but provides Metal Performance Shaders (MPS) for GPU acceleration.
2. Ensure you are using macOS 12.3 or later and have an Apple Silicon or AMD GPU.
3. Install the required PyTorch version with MPS support:
   ```bash
   pip install torch torchvision torchaudio
   ```
4. Enable MPS in your application by setting the device to `mps`:
   ```python
   device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
   ```

---

## Usage

### CLI Mode
Run the application in CLI mode:
```bash
python main.py
```

### Web Interface
Run the application in web mode:
```bash
python main.py --web
```
By default, the web interface runs on port 5000. You can specify a different port:
```bash
python main.py --web --port 8080
```

---

## Notes
- Ensure your Hugging Face token is saved locally for seamless model downloads.
- For gated models, ensure you have requested and received access before running the application.
- Feedback mechanisms are placeholders and can be extended as needed.

---

## Troubleshooting
- **Model Loading Issues**: Ensure your Hugging Face token is valid and you have access to the specified model.
- **Database Connection Errors**: Verify your MongoDB connection details in the `.env` file.
- **Web Interface Not Starting**: Ensure the specified port is not in use.

---

## Disclaimer
This project is personal and not licensed. Use it at your own discretion.
