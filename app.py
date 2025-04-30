# AutoResearcher AI - Research Paper Explainer + AI Agents

# --------------------------------------
# 📦 Required Libraries:
# pip install streamlit langchain chromadb ollama pdfplumber pdf2image pytesseract requests beautifulsoup4
# sudo apt install poppler-utils tesseract-ocr

import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import tempfile
import requests
from bs4 import BeautifulSoup

# ------------------ Helper: Extract Text + OCR ------------------
def extract_text_and_ocr(uploaded_files):
    all_text = ""
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

        images = convert_from_path(tmp_path)
        for img in images:
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                all_text += ocr_text + "\n"

    return all_text

# ------------------ Helper: Vector Store Creation ------------------
@st.cache_resource
def create_vector_store(text):
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([text])
    embed_model = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(docs, embed_model)

# ------------------ Helper: ArXiv Related Papers ------------------
def find_related_papers(query):
    try:
        url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("entry")
        return [f"[{e.title.text.strip()}]({e.id.text.strip()})" for e in entries]
    except:
        return ["Error fetching related papers."]

# ------------------ Streamlit App ------------------
st.set_page_config(page_title="AutoResearcher AI", layout="wide")
st.title("🤖 AutoResearcher AI")
st.caption("Smart Research Paper Explainer with AI Agents")

uploaded_files = st.sidebar.file_uploader("📄 Upload Research PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Reading & Processing documents..."):
        full_text = extract_text_and_ocr(uploaded_files)
        vector_store = create_vector_store(full_text)
        retriever = vector_store.as_retriever()
        llm = Ollama(model="llama3")
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    st.subheader("🧠 Ask anything about the uploaded papers")
    user_input = st.chat_input("Ask a question, e.g., Summarize key contributions")

    if "history" not in st.session_state:
        st.session_state.history = []

    if user_input:
        with st.spinner("Thinking..."):
            answer = qa_chain.run(user_input)
            st.session_state.history.append((user_input, answer))

    for q, a in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a)

    # Related Papers Suggestion
    st.divider()
    st.subheader("🔎 Related Papers from arXiv")
    rel_query = st.text_input("Search related papers on arXiv (e.g., GANs for medical imaging):")
    if st.button("Fetch Suggestions") and rel_query:
        results = find_related_papers(rel_query)
        for r in results:
            st.markdown("- " + r)

    # Blog Generation Prompt
    st.divider()
    st.subheader("✍️ Blog Article Generator")
    if st.button("Generate Blog from Papers"):
        prompt = "Write a detailed, engaging blog post summarizing the core ideas, methods, and results from this paper."
        blog = qa_chain.run(prompt)
        st.text_area("Generated Blog:", blog, height=300)

else:
    st.info("⬅️ Upload one or more research PDFs to begin.")
