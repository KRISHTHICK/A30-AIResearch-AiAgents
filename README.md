# A30-AIResearch-AiAgents
GenAI

✅ **Code is ready. Here's how to set it up in GitHub and run in VS Code:**

---

### 🧾 Step-by-step Setup (No venv)

#### 1. **Create a GitHub Repository**
- Go to [github.com](https://github.com)
- Click **New Repository**
- Name: `AutoResearcher-AI`
- Choose `Public`
- Do **not** initialize with README
- Click **Create Repository**

#### 2. **Clone in VS Code**
```bash
git clone https://github.com/YOUR_USERNAME/AutoResearcher-AI.git
cd AutoResearcher-AI
code .
```

#### 3. **Add Code File**
- Save the provided code in a file called: `app.py`
- Add a `requirements.txt` file:

```txt
streamlit
langchain
chromadb
ollama
pdfplumber
pdf2image
pytesseract
requests
beautifulsoup4
```

> (Linux/macOS users must also run: `sudo apt install poppler-utils tesseract-ocr`)

#### 4. **Run Locally in VS Code**
- Make sure Ollama is running locally with `ollama run llama3`
- Then run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

Would you like a `README.md` file pre-written to include usage and screenshots for GitHub?
