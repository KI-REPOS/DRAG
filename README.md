# 🤖 RAG Pipeline — Retrieval-Augmented Generation (ChromaDB + Flask)

A **Flask-based RAG system** where users can upload **files (PDF, DOCX, PPT, TXT, PNG, JPEG)** or provide **URLs (websites, YouTube videos)**.  
The data is **converted into vector embeddings**, stored in **ChromaDB**, and queried through a web interface.  
Retrieved chunks are polished by the **Phi-2 Quantized Model** before being shown to the user.

---

## 🚀 Features

- 📂 **Multi-format ingestion** — PDF, DOCX, PPT, TXT, PNG, JPEG  
- 🌐 **Web & YouTube support** — fetch website content & video transcripts  
- ✂️ **Chunk-based embeddings** — improves retrieval quality  
- 🧠 **ChromaDB integration** — efficient similarity search  
- 💻 **Flask Web UI** — clean query interface  
- 🔍 **Top-k retrieval** — fetches only the most relevant chunks  
- 🎯 **LLM Polishing** — refined answers using **Phi-2 (quantized)**  
- ⚡ **Two-step execution** — `ingest_data.py` (indexing) → `app.py` (querying)  

---

## 📂 Use Cases

- 📝 **Custom Q&A Chatbot** over private docs  
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

The Phi2Q_4_k.ggfu model (~1.66 GB) is not included in the repo.
👉 [Download here] (https://cas-bridge.xethub.hf.co/xet-bridge-us/6580aa20419afba19a692cc8/cb5d304e5b36d2f91430fff1530842167680b0958c4083b09e04d4dbf8cf7a08?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cas%2F20250919%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250919T211759Z&X-Amz-Expires=3600&X-Amz-Signature=3f9791d006b1b54525d94235987637eee58a46202cb13e1d99454a2b2901a218&X-Amz-SignedHeaders=host&X-Xet-Cas-Uid=public&response-content-disposition=inline%3B+filename*%3DUTF-8%27%27phi-2.Q4_K_M.gguf%3B+filename%3D%22phi-2.Q4_K_M.gguf%22%3B&x-id=GetObject&Expires=1758320279&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc1ODMyMDI3OX19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2FzLWJyaWRnZS54ZXRodWIuaGYuY28veGV0LWJyaWRnZS11cy82NTgwYWEyMDQxOWFmYmExOWE2OTJjYzgvY2I1ZDMwNGU1YjM2ZDJmOTE0MzBmZmYxNTMwODQyMTY3NjgwYjA5NThjNDA4M2IwOWUwNGQ0ZGJmOGNmN2EwOCoifV19&Signature=LuBwPW25utjxw%7ED9YJiYnYHm%7E1JIR4phreTWysMS8y9VRNlPv7ubbj2v0O9nbOrISDfllFL7p0oS9-PDFLM6ZdpWqqst2yqpE33MqdYZ02w4NI28Wt0a9t9zgVgQNd%7E0cW1PGn8cIMq5zs31af01eSiaT2HWQcaf-ikS71zyaFUkQt1DMbFMMwNyUGVmxjvaQNOvjPptqbbbjZQu9Hh84wVdHafi2%7EBvfVVxF9rLiTlAC6KBPYy5rJ2YbZlLgf-i378pesQZWXZ8-4TGCySKUmgDa%7Ej7G79cvVQyoOYFcegVon%7EuO210PfJ4joNpXa66xQdoYMUFbTkz2RoNyU787A__&Key-Pair-Id=K2L8F4GPSG1IFC)
 and place it in the models/ directory.

</details>
## ▶️ Execution
<details> <summary>📥 Step 1 — Ingest & Index Data</summary>
- First run this create vector emmbedings / chunks and store it in ChromaDB

 ```
 python ingest_data.py
```


- ✅ ## Converts files/URLs into chunks
- ✅ ## Creates embeddings
- ✅ ## Stores vectors in ChromaDB

</details> <details> <summary>💡 Step 2 — Run the Flask Web App</summary>
python app.py


-✅ ### Starts server at http://0.0.0.0:5000
-✅ ### Upload more files / paste URLs
-✅ ### Ask questions & get AI-polished results

</details>
## 📂 Supported Inputs

- ### Documents → .pdf, .docx, .ppt, .txt

- ### Images → .png, .jpeg

- ### Links → websites & YouTube videos (transcripts extracted if available)
