# 🤖 RAG Pipeline — Retrieval-Augmented Generation (ChromaDB + Flask)

A **Flask-based RAG system** where users can upload **files** (`PDF, DOCX, PPT, TXT, PNG, JPEG`) or provide **URLs** (websites, YouTube videos).  
Data is **converted into vector embeddings**, stored in **ChromaDB**, and queried through a clean web interface.  
Retrieved chunks are polished by the **Phi-2 Quantized Model** before being presented to the user.

---

## 🚀 Features

- 📂 **Multi-format ingestion** — PDF, DOCX, PPT, TXT, PNG, JPEG  
- 🌐 **Web & YouTube support** — fetch website content & video transcripts  
- ✂️ **Chunk-based embeddings** — improves retrieval quality  
- 🧠 **ChromaDB integration** — efficient similarity search  
- 💻 **Flask Web UI** — clean query interface  
- 🔍 **Top-k retrieval** — fetches the most relevant chunks only  
- 🎯 **LLM Polishing** — refined answers using **Phi-2 (quantized)**  
- ⚡ **Two-step execution** — `ingest_data.py` (indexing) → `app.py` (querying)  

---

## 📂 Use Cases

- 📝 **Custom Q&A Chatbot** over private documents  
- 🎓 **Research assistant** for papers, slides, & YouTube lectures  
- 🏢 **Enterprise knowledge base** with internal reports  
- 📖 **Summarizer** for articles, PDFs, and videos  

---

## 🛠️ Installation & Setup

<details>
<summary>📦 Step 1 — Clone the repository</summary>

```
git clone https://github.com/your-username/rag-pipeline.git
cd rag-pipeline
```
</details> <details> <summary>🐍 Step 2 — Create & activate virtual environment</summary>

```
# Create virtual environment
py -3.12 -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
</details> <details> <summary>⚙️ Step 3 — Install dependencies</summary>

```
pip install -r requirements.txt
```
</details> <details> <summary>🧠 Step 4 — Download the Phi-2 Model</summary>

- The Phi2Q_4_k.ggfu model (~1.66 GB) is not included in the repository.

👉 [Download here](https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf)

- Place the file in the models/ directory.

</details>

▶️ **Execution**

<details> <summary>📥 Step 1 — Ingest & Index Data</summary>

Run to create vector embeddings/chunks and store them in ChromaDB:
```
python ingest_data.py
```

- ✅ Converts files/URLs into chunks
- ✅ Creates embeddings
- ✅ Stores vectors in ChromaDB

</details> <details> <summary>💡 Step 2 — Run the Flask Web App</summary>
python app.py


- ✅ Starts server at http://0.0.0.0:5000
- ✅ Upload more files / paste URLs
- ✅ Ask questions & get AI-polished results

</details>
