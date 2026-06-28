import os
import sys
import subprocess

# Ensure the root directory is appended to sys.path for absolute module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def start_app():
    """
    Launches the Streamlit framework seamlessly via a clean subprocess execution chain.
    """
    try:
        print("🚀 Initializing Agri-Health Workspace Engine on port 8080...")
        
        # Execute the streamlined command string in a separate process container
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8080"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Workspace shut down successfully.")
    except subprocess.CalledProcessError as err:
        print(f"\n❌ Execution engine collapsed with error code: {err.returncode}")

if __name__ == "__main__":
    start_app()