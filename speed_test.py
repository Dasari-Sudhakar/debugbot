import requests
import time

# Test Ollama speed
models = ["llama3.2:3b", "codellama:7b", "codellama"]

for model in models:
    print(f"\nTesting {model}...")
    start = time.time()
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": "What is IndexError?",
            "stream": False
        }, timeout=30)
        
        elapsed = time.time() - start
        print(f"✅ {model}: {elapsed:.2f} seconds")
    except Exception as e:
        print(f"❌ {model}: {e}")