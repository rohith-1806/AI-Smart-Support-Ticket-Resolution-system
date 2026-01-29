# AI-based Ticket Resolution System

An intelligent knowledge management platform that uses AI (or a smart fallback system) to automatically recommend solutions for support tickets.

## Features
- **AI-Powered Recommendations**: Uses LLMs (via Ollama) or TF-IDF matching to suggest articles.
- **Auto-Bootstrapped**: Single command to launch both Backend (API) and Frontend (UI).
- **Robust Fallback**: Works even if the local AI model is not installed.
- **Modern UI**: Clean, gradient-themed interface.

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- [Optional] [Ollama](https://ollama.com/) with `llama3.2:1b` model for full AI features.

### Installation
1.  Navigate to the project folder:
    ```bash
    cd Final_Project
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App
Run the entire system (Frontend + Backend) with one command:

```bash
streamlit run app.py
```

- **Frontend**: http://localhost:8501
- **Backend API**: http://127.0.0.1:8000

## Project Structure
- `app.py`: Main entry point / launcher.
- `Backend/`: FastAPI application and AI logic.
- `Frontend/`: Streamlit user interface.
- `knowledge_base.csv`: Database of support articles.

- ## To access project directly check the link below

- - **Deployed by Streamlit**: http://localhost:8501](https://ai-smart-support-ticket-resolution-system.streamlit.app/
 
  **Author**: Perumalla Rohith
