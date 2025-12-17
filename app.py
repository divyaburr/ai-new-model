from fastapi import FastAPI, Query
import subprocess

app = FastAPI()

OLLAMA_PATH = r"C:\Users\SYR00347\AppData\Local\Programs\Ollama\ollama.exe"
MODEL = "phi"   # low RAM system ki best


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chat")
def chat(query: str = Query(..., description="Error or question")):
    try:
        # ✅ PROMPT ADDED
        prompt = f"""
You are a senior Python developer.
Explain the error clearly and give solution with example.

Error:
{query}
"""

        result = subprocess.run(
            [OLLAMA_PATH, "run", MODEL],
            input=prompt,              # ✅ CHANGED
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=60
        )

        if result.returncode != 0:
            return {
                "error": "Ollama execution failed",
                "details": result.stderr
            }

        return {
            "query": query,
            "solution": result.stdout.strip()
        }

    except Exception as e:
        return {"error": str(e)}
