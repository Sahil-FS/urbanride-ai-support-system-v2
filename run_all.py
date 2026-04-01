import subprocess
import sys
import os
import signal
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Only run the main chatbot service (local models, no mocks needed)
SERVICES = [
    {
        "name": "Urban Ride AI Chatbot Service (port 8000)",
        "cmd": [sys.executable, "-m", "uvicorn", "main:app",
                "--port", "8000", "--reload"],
        "cwd": BASE_DIR,
    },
]

def main():
    processes = []
    print("\n" + "="*55)
    print("  Urban Black Taxi — Customer Support AI Stack")
    print("="*55)
    for svc in SERVICES:
        print(f"\n  Starting {svc['name']} ...")
        proc = subprocess.Popen(svc["cmd"], cwd=svc["cwd"])
        processes.append(proc)
        time.sleep(1)
    print("\n" + "="*55)
    print("  All services running!")
    print("-"*55)
    print("  Chatbot API  ->  http://localhost:8000/docs")
    print("  Using local intent model from models/intent/")
    print("-"*55)
    print("  Press Ctrl+C to stop all")
    print("="*55 + "\n")

    def shutdown(sig, frame):
        print("\nShutting down...")
        for proc in processes:
            proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    for proc in processes:
        proc.wait()

if __name__ == "__main__":
    main()
