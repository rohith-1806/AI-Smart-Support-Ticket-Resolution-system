import streamlit as st
import subprocess
import sys
import time
import requests
import os
from Frontend.frontend import frontend_ui

# Page Config (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Ticket Resolution",
    page_icon="🤖",
    layout="wide"
)

def is_backend_running():
    """Checks if the backend is already running by pinging the health endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def start_backend():
    """Starts the backend API in a subprocess."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # We use Popen to let it run in the background
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "Backend.backend:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=base_dir,
        # On Windows, creationflags=subprocess.CREATE_NEW_CONSOLE can open a new window for logs if desired,
        # but let's keep it hidden/embedded for now to be cleaner.
    )

def main():
    # 1. Check/Start Backend
    if not is_backend_running():
        placeholder = st.empty()
        with placeholder.container():
            st.warning("Backend is not running. Starting API server... Please wait.")
            start_backend()
            
            # Wait for backend to come alive
            retries = 10
            for i in range(retries):
                time.sleep(2)
                if is_backend_running():
                    st.success("Backend started successfully!")
                    time.sleep(1)
                    break
            else:
                st.error("Failed to start backend. Please check logs.")
                st.stop()
        
        placeholder.empty()

    # 2. Run Frontend Logic
    frontend_ui()

if __name__ == "__main__":
    main()
