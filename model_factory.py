from config import MODEL_BACKEND, OLLAMA_CONFIG, LLAMA_CPP_CONFIG

def get_model_client():
    """Factory function to get the appropriate model client"""
    if MODEL_BACKEND == "ollama":
        from ollama_client import OllamaClient
        return OllamaClient(OLLAMA_CONFIG["host"], OLLAMA_CONFIG["model"])
    elif MODEL_BACKEND == "llama_cpp":
        from llama_cpp_client import LlamaCppClient
        return LlamaCppClient(
            model_path=LLAMA_CPP_CONFIG["model_path"],
            model_name=LLAMA_CPP_CONFIG["model_name"],
            n_ctx=LLAMA_CPP_CONFIG["n_ctx"],
            n_threads=LLAMA_CPP_CONFIG["n_threads"]
        )
    else:
        raise ValueError(f"Unknown MODEL_BACKEND: {MODEL_BACKEND}")
