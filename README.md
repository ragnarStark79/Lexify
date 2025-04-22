# Lexify

Lexify is a powerful text enhancement tool that leverages state-of-the-art AI models to improve the quality of text. It supports both CLI and web interfaces, making it versatile for various use cases. The application integrates with Hugging Face models and MongoDB for logging interactions and user data.

## Features
- Enhance text using AI models from Hugging Face (currently configured for `mistralai/Mistral-7B-Instruct-v0.1`).
- **Web Interface:**
    - User authentication (signup, login, logout).
    - User profile management (view/update name and email).
    - Protected routes requiring login.
    - Interactive text input and output display with loading animations.
    - Feedback mechanism (rating) for enhanced text.
    - Flash messages and welcome popups for user feedback.
    - Responsive design with scroll-triggered animations.
- **CLI Mode:** Basic command-line interface for text enhancement.
- **Database Integration:**
    - Log text enhancement interactions (original, enhanced, model, user ID, feedback) to MongoDB.
    - Store user credentials and profile information securely in MongoDB (passwords hashed using Bcrypt).
- Easily configurable model via `config.py`.
- Secure configuration using `.env` file for sensitive data (API keys, database URI, secret key).

---

## Installation

### Step 1: Clone or Fork the Repository
```bash
git clone https://github.com/ragnarStark79/Lexify.git # Replace with actual repo URL if different
cd lexify
```

### Step 2: Create a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # macOS/Linux
# or
venv\Scripts\activate # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Setup

### Step 1: Create and Configure `.env` File
Create a `.env` file in the root directory of the project. Add the following variables, replacing placeholder values with your actual credentials:

```plaintext
# MongoDB Connection String (local or cloud)
MONGO_URI="mongodb://localhost:27017/"
# Database and Collection Names (optional, defaults are provided in config.py)
MONGO_DB_NAME="lexify_data"
MONGO_COLLECTION_NAME="interactions"
MONGO_USERS_COLLECTION_NAME="users"

# Flask Secret Key (generate a strong random key)
# Example generation: python -c 'import secrets; print(secrets.token_hex(32))'
SECRET_KEY="your_strong_random_secret_key"

# Hugging Face Token (optional, needed for private/gated models)
HUGGINGFACE_TOKEN="your_huggingface_token"
```

**Important:**
- Ensure your MongoDB server is running and accessible at the specified `MONGO_URI`.
- Generate a unique and strong `SECRET_KEY` for Flask session security.

### Step 2: Hugging Face Setup (If using private/gated models)
Follow the steps in the original README section for Hugging Face Hub installation, authentication (`huggingface-cli login`), and requesting access if needed.

### Step 3: Configure Model (Optional)
- The default model is set in `config.py` (`mistralai/Mistral-7B-Instruct-v0.1`).
- You can change `DEFAULT_MODEL_NAME` to another compatible Hugging Face model.
- Ensure the chosen model is suitable for your hardware resources.

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

### Web Interface (Recommended)
Run the Flask web application:
```bash
python webapp.py
```
- Access the application in your browser, usually at `http://127.0.0.1:5000`.
- Sign up for a new account or log in.
- Navigate to the enhancer page to use the tool.
- Visit the profile page via the user icon dropdown to manage your details.

### CLI Mode (Basic Functionality)
Run the application in CLI mode:
```bash
python main.py
```
- Follow the prompts to enter text for enhancement.

---

## Notes
- The web interface provides the full set of features, including user accounts and feedback.
- Ensure your `.env` file is correctly configured before running the application.
- The feedback mechanism currently logs the rating to the database but doesn't yet influence model behavior.

---

## Troubleshooting
- **Authentication Issues**: Double-check email/password. Ensure the database connection is working and the `users` collection exists.
- **Model Loading Issues**: Verify `HUGGINGFACE_TOKEN` in `.env` (if needed), internet connection, and model access permissions on Hugging Face.
- **Database Connection Errors**: Confirm `MONGO_URI` in `.env` is correct and the MongoDB server is running.
- **Web Interface Not Starting**: Check for port conflicts (default 5000) and look for errors in the terminal output when running `python webapp.py`.
- **JavaScript Errors**: Open the browser's developer console (usually F12) to check for errors on the web pages.

---

## Disclaimer
This project is personal and not licensed. Use it at your own discretion.
