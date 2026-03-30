import subprocess
import sys
import os
import signal
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Priority: Use local venv python if available
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
PYTHON_EXE = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

# ... (rest of the file)
SERVICES = [
    {
        "name": "Chatbot Backend (port 8000)",
        "cmd": [PYTHON_EXE, "-m", "uvicorn", "main:app", "--port", "8000", "--reload"],
        "cwd": BASE_DIR,
    },
    {
        "name": "React Frontend (port 5173)",
        "cmd": "npm run dev",
        "cwd": os.path.join(BASE_DIR, "frontend"),
        "shell": True,
    },
    {
        "name": "Ticket Escalation Cron",
        "cmd": [PYTHON_EXE, "-m", "app.cron.run_cron"],
        "cwd": BASE_DIR,
    },
]

def main():
    processes = []
    print("\n" + "="*55)
    print("  UrbanRide Customer Support - Full Stack")
    print("="*55)
    for svc in SERVICES:
        print(f"\n  Starting {svc['name']} ...")
        proc = subprocess.Popen(
            svc["cmd"], 
            cwd=svc["cwd"], 
            shell=svc.get("shell", False)
        )
        processes.append(proc)
        time.sleep(1)
    
    print("\n" + "="*55)
    print("  All services running!")
    print("-"*55)
    print("  Frontend UI  ->  http://localhost:5173")
    print("  Backend API  ->  http://localhost:8000/docs")
    print("-"*55)
    print("  Press Ctrl+C to stop all")
    print("="*55 + "\n")
# ... (rest of the file)

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
