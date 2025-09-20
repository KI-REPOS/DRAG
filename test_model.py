import os
import sys
from config import Config
import subprocess
import psutil

def check_system_resources():
    """Check available system resources."""
    print("🖥️  System Resources Check")
    print("=" * 50)
    
    # Check RAM
    memory = psutil.virtual_memory()
    print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
    print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
    print(f"RAM used: {memory.percent}%")
    
    # Check disk space
    disk = psutil.disk_usage('/')
    print(f"Disk free: {disk.free / (1024**3):.2f} GB")
    
    return memory.available / (1024**3)  # Return available GB

def check_model_file():
    """Check the model file details."""
    print("\n📁 Model File Check")
    print("=" * 50)
    
    if not os.path.exists(Config.LLM_MODEL_PATH):
        print(f"❌ Model file not found: {Config.LLM_MODEL_PATH}")
        return False
    
    file_size = os.path.getsize(Config.LLM_MODEL_PATH) / (1024**3)  # GB
    print(f"✅ Model file found: {Config.LLM_MODEL_PATH}")
    print(f"✅ File size: {file_size:.2f} GB")
    
    # Check file integrity
    try:
        with open(Config.LLM_MODEL_PATH, 'rb') as f:
            header = f.read(100)
            if header.startswith(b'GGUF'):
                print("✅ File format: GGUF (correct)")
            else:
                print("❌ File format: Not GGUF (may be corrupted)")
                return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    return True

def check_llama_cpp_installation():
    """Check llama-cpp-python installation."""
    print("\n🐍 Llama.cpp Check")
    print("=" * 50)
    
    try:
        import llama_cpp
        print(f"✅ llama-cpp-python version: {llama_cpp.__version__}")
        
        # Check if it has GPU support
        try:
            has_gpu = hasattr(llama_cpp, 'llama_gpu_init')
            print(f"✅ GPU support: {has_gpu}")
        except:
            print("⚠️  GPU support: Unknown")
            
        return True
    except ImportError as e:
        print(f"❌ llama-cpp-python not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with llama-cpp: {e}")
        return False

def test_model_loading_detailed():
    """Test model loading with detailed error reporting."""
    print("\n🔧 Detailed Model Loading Test")
    print("=" * 50)
    
    available_ram = check_system_resources()
    if not check_model_file():
        return False
    if not check_llama_cpp_installation():
        return False
    
    # Check if we have enough RAM (Phi-3 needs ~4GB+ to load)
    if available_ram < 4.0:
        print(f"❌ Insufficient RAM: {available_ram:.2f} GB available, need ~4GB+")
        return False
    
    try:
        import llama_cpp
        
        print("\n🚀 Attempting to load model...")
        
        # Try with minimal settings first
        model = llama_cpp.Llama(
            model_path=Config.LLM_MODEL_PATH,
            n_ctx=512,      # Very small context
            n_threads=1,    # Single thread
            n_batch=128,    # Small batch
            n_gpu_layers=0, # No GPU
            use_mlock=False, # Don't lock memory
            verbose=True    # Show detailed output
        )
        
        print("✅ Model loaded successfully with minimal settings!")
        
        # Test a tiny generation
        print("\n🧪 Testing generation...")
        output = model("Hello", max_tokens=5, stop=[], echo=False)
        print(f"✅ Test output: {output['choices'][0]['text']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Detailed error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        
        # Check for common errors
        error_str = str(e).lower()
        if 'memory' in error_str:
            print("💡 Issue: Insufficient memory to load model")
            print("💡 Solution: Use a smaller model or close other applications")
        elif 'cuda' in error_str or 'gpu' in error_str:
            print("💡 Issue: GPU-related error")
            print("💡 Solution: Set n_gpu_layers=0 to use CPU only")
        elif 'file' in error_str or 'path' in error_str:
            print("💡 Issue: File not found or inaccessible")
        elif 'format' in error_str or 'gguf' in error_str:
            print("💡 Issue: Corrupted or invalid model file")
            print("💡 Solution: Re-download the model file")
        else:
            print("💡 Issue: Unknown error during model loading")
        
        return False

def check_alternative_models():
    """Suggest alternative models that will work."""
    print("\n💡 Alternative Model Suggestions")
    print("=" * 50)
    
    models = [
        {
            "name": "TinyLlama 1.1B",
            "size": "0.7GB",
            "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
            "ram_required": "2GB"
        },
        {
            "name": "Microsoft DialoGPT Small",
            "size": "0.3GB", 
            "url": "https://huggingface.co/lmstudio-community/Microsoft-DialoGPT-small-gguf/resolve/main/dialogpt-small.q4_0.gguf",
            "ram_required": "1.5GB"
        },
        {
            "name": "Phi-2 (smaller than Phi-3)",
            "size": "1.6GB",
            "url": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
            "ram_required": "3GB"
        }
    ]
    
    print("If Phi-3 is too large, try these smaller models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model['name']} ({model['size']}, needs {model['ram_required']} RAM)")
        print(f"   Download: {model['url']}")
    
    return models

if __name__ == "__main__":
    print("🔍 Phi-3 Model Loading Debug")
    print("=" * 60)
    
    success = test_model_loading_detailed()
    
    if not success:
        check_alternative_models()
        
        # Quick fix: Create a simple test without full loading
        print("\n🚨 Creating fallback version...")
        try:
            from llm_model import LocalLLM
            llm = LocalLLM()
            if llm.fallback_mode:
                print("✅ Fallback mode activated - system will work with basic responses")
            else:
                print("✅ Model loaded successfully in fallback class")
        except Exception as e:
            print(f"❌ Fallback also failed: {e}")


# import os
# import hashlib

# def check_model_file():
#     """Check model file integrity."""
#     model_path = "./models/phi-3-mini-4k-instruct-q4.gguf"
    
#     if not os.path.exists(model_path):
#         print("❌ Model file not found")
#         return False
    
#     # Check file size
#     file_size = os.path.getsize(model_path)
#     expected_size = 2280000000  # ~2.28GB
#     size_diff = abs(file_size - expected_size) / expected_size
    
#     print(f"File size: {file_size / (1024**3):.2f} GB")
#     print(f"Expected: {expected_size / (1024**3):.2f} GB")
#     print(f"Difference: {size_diff * 100:.1f}%")
    
#     if size_diff > 0.05:  # More than 5% difference
#         print("❌ File size suspicious - likely corrupted download")
#         return False
    
#     # Check first few bytes for GGUF signature
#     try:
#         with open(model_path, 'rb') as f:
#             header = f.read(100)
#             if header.startswith(b'GGUF'):
#                 print("✅ GGUF signature found")
#                 return True
#             else:
#                 print("❌ Not a valid GGUF file")
#                 return False
#     except Exception as e:
#         print(f"❌ Error reading file: {e}")
#         return False

# if __name__ == "__main__":
#     if check_model_file():
#         print("✅ Model file appears valid")
#     else:
#         print("❌ Model file may be corrupted - please re-download")