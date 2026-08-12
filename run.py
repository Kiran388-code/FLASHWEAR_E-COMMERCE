import os
import sys
import uvicorn

# Ensure current project root is in sys.path and PYTHONPATH environment variable for subprocesses
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

existing_pythonpath = os.environ.get("PYTHONPATH", "")
if base_dir not in existing_pythonpath:
    os.environ["PYTHONPATH"] = f"{base_dir};{existing_pythonpath}" if existing_pythonpath else base_dir

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
