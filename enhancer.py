from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import config
import platform
import time # Import time module

class TextEnhancer:
    def __init__(self, model_name=config.DEFAULT_MODEL_NAME):
        self.model_name = model_name
        # Determine the primary device preference, but accelerate will manage final placement
        if platform.system() == "Darwin" and torch.backends.mps.is_available():
            self.primary_device_preference = "mps"
        elif torch.cuda.is_available():
            self.primary_device_preference = "cuda"
        else:
            self.primary_device_preference = "cpu"
        # Note: self.device will be determined by the model after loading with device_map='auto'

        print(f"Primary device preference: {self.primary_device_preference}")

        # Use float16 for potential memory saving if GPU/MPS is likely used by accelerate
        dtype = torch.float16 if self.primary_device_preference in ["cuda", "mps"] else torch.float32

        try:
            print(f"Loading tokenizer for {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, padding_side='left')
            print(f"Loading model {self.model_name} with accelerate...")
            # Load model using device_map='auto', DO NOT call .to(device) afterwards
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
                device_map="auto"  # Automatically map layers using accelerate
            )
            # Get the actual device the model (or its first part) is on after accelerate places it
            self.device = self.model.device
            print(f"Model loaded. Effective device determined by accelerate: {self.device}")
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            self.tokenizer = None
            self.model = None

    def enhance_text(self, text, max_length=256):
        """Enhances the input text using the loaded model and returns text and duration."""
        if not self.model or not self.tokenizer:
            print("Model not loaded. Cannot enhance text.")
            # Return None for duration in case of error
            return "Error: Model not available.", None

        # Mistral Instruct Prompt Format: <s>[INST] {prompt} [/INST]
        instruction = (
            f"Correct all grammatical errors, fix awkward phrasing, and improve the clarity and flow of the following sentence. "
            f"Rewrite it completely if necessary to sound natural and correct. Do not include explanations, just provide the corrected sentence.\n\n"
            f"Sentence: {text}"
        )
        prompt = f"<s>[INST] {instruction} [/INST]"

        # Ensure tokenizer has a pad token (Mistral might not have one by default)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        try:
            # Tokenize and ensure inputs are on the same device as the model's input layer
            # Use model.device which reflects accelerate's placement
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.model.device)

            start_time = time.perf_counter() # Start timer
            # Generate completion
            outputs = self.model.generate(
                **inputs,  # Pass tokenized inputs directly
                max_new_tokens=max_length,  # Control length of the *newly generated* text
                do_sample=True,
                temperature=0.7,  # Start lower for Mistral Instruct
                top_p=0.9,  # Adjusted top_p
                repetition_penalty=1.1,  # Adjusted repetition penalty
                pad_token_id=self.tokenizer.eos_token_id  # Use EOS token ID for padding during generation
            )
            end_time = time.perf_counter() # End timer
            duration = end_time - start_time # Calculate duration

            # Decode only the newly generated tokens
            input_token_len = inputs.input_ids.shape[1]
            enhanced_text = self.tokenizer.decode(outputs[0][input_token_len:], skip_special_tokens=True).strip()

            # Basic post-processing
            if enhanced_text and enhanced_text[0].islower():
                enhanced_text = enhanced_text[0].upper() + enhanced_text[1:]

            # Return both text and duration
            return enhanced_text, duration
        except Exception as e:
            print(f"Error during text enhancement: {e}")
            # Return None for duration in case of error
            return f"Error: Could not process text. {e}", None

# Singleton instance (optional)
text_enhancer = TextEnhancer()

def get_text_enhancer():
    """Returns the singleton text enhancer instance."""
    return text_enhancer