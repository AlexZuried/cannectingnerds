import subprocess
import json
import os
from huggingface_hub import hf_hub_download

class LlamaCppClient:
    def __init__(self, model_path=None, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                 n_ctx=2048, n_threads=4):
        """
        Initialize llama.cpp client.
        - model_path: Path to .gguf model file (if None, downloads from HF)
        - model_name: HuggingFace model name for auto-download
        - n_ctx: Context window size
        - n_threads: Number of CPU threads
        """
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        
        if model_path:
            self.model_path = model_path
        else:
            # Download model from HuggingFace
            print(f"Downloading model {model_name} from HuggingFace...")
            self.model_path = self._download_model(model_name)
        
        self.llama_process = None

    def _download_model(self, model_name):
        """Download GGUF model from HuggingFace"""
        try:
            # Try to find a GGUF file in the repo
            model_path = hf_hub_download(
                repo_id=model_name,
                filename="model.gguf",
                repo_type="model"
            )
            return model_path
        except Exception:
            # Try common GGUF filenames
            gguf_files = [
                "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
                "model.Q4_K_M.gguf",
                "*.gguf"
            ]
            for pattern in gguf_files:
                try:
                    model_path = hf_hub_download(
                        repo_id=model_name,
                        filename=pattern if not pattern.startswith("*") else None,
                        repo_type="model"
                    )
                    return model_path
                except Exception:
                    continue
            
            raise FileNotFoundError(
                f"No GGUF model found for {model_name}. "
                "Please download a GGUF model manually or specify model_path."
            )

    def generate(self, prompt, context="", max_tokens=256, temperature=0.7):
        """Generate response using llama.cpp"""
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        try:
            # Run llama.cpp inference
            cmd = [
                "./main",  # llama.cpp main binary
                "-m", self.model_path,
                "-p", full_prompt,
                "-n", str(max_tokens),
                "--temp", str(temperature),
                "-t", str(self.n_threads),
                "--ctx-size", str(self.n_ctx),
                "-ngl", "0"  # No GPU offload by default
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"llama.cpp error: {result.stderr}")
                return ""
                
        except subprocess.TimeoutExpired:
            print("llama.cpp generation timed out")
            return ""
        except FileNotFoundError:
            print("llama.cpp binary not found. Please compile llama.cpp first.")
            print("Clone: git clone https://github.com/ggerganov/llama.cpp")
            print("Build: cd llama.cpp && make")
            return ""
        except Exception as e:
            print(f"llama.cpp error: {e}")
            return ""

    def generate_with_pipes(self, prompt, context="", max_tokens=256, temperature=0.7):
        """Alternative: Use stdin/stdout pipes for faster repeated inference"""
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        if self.llama_process is None:
            # Start persistent llama.cpp process
            cmd = [
                "./main",
                "-m", self.model_path,
                "-n", str(max_tokens),
                "--temp", str(temperature),
                "-t", str(self.n_threads),
                "--ctx-size", str(self.n_ctx),
                "-i",  # Interactive mode
                "--no-display-prompt"
            ]
            self.llama_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        
        try:
            self.llama_process.stdin.write(full_prompt + "\n")
            self.llama_process.stdin.flush()
            
            # Read response (simplified - may need better parsing)
            response = ""
            for _ in range(max_tokens):
                char = self.llama_process.stdout.read(1)
                if not char:
                    break
                response += char
                if response.endswith("\n\n"):
                    break
            
            return response.strip()
            
        except Exception as e:
            print(f"Pipe error: {e}")
            self.llama_process = None  # Reset process
            return ""

    def is_available(self):
        """Check if llama.cpp is available and model exists"""
        if not os.path.exists(self.model_path):
            return False
        
        # Check if llama.cpp binary exists
        if not os.path.exists("./main"):
            return False
        
        # Quick test
        try:
            result = subprocess.run(
                ["./main", "-m", self.model_path, "-h"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0 or "usage" in result.stderr.lower()
        except:
            return False

    def close(self):
        """Clean up resources"""
        if self.llama_process:
            self.llama_process.terminate()
            self.llama_process.wait()
