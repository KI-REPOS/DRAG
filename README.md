<h1>📚 Retrieval-Augmented Generation (RAG) Pipeline</h1>
🔥 Overview

This project implements a RAG pipeline using ChromaDB + Flask.
It lets users upload documents (PDF, DOCX, PPT, TXT, PNG, JPEG) and URLs (websites, YouTube videos), converts them into vector embeddings, stores them in ChromaDB, and allows interactive querying with an LLM.

✨ Key Highlights

🧩 Automatic Chunking + Embeddings

📂 Multi-format support → PDF, DOCX, PPT, TXT, PNG, JPEG

🌐 Websites & YouTube ingestion

🗄️ Vector storage with ChromaDB

🤖 Phi-2 Quantized LLM (phi2Q_4_k.ggfu)

🎨 Flask Web UI for seamless interaction

<details> <summary><h2>⚡ Project Workflow</h2></summary>
 <ul>
    <li>Option 1</li>
    <li>Option 2</li>
    <li>Option 3</li>
  </ul>
🔹 Step 1: Ingest Data

Run ingest_data.py

Converts files/URLs → chunks → embeddings → stored in ChromaDB

🔹 Step 2: Query System

Run app.py

Query → Retrieve top-k relevant chunks → Refined via Phi-2 LLM → Displayed in Flask UI

</details>
<details> <summary><h2>🛠️ Tech Stack</h2></summary>
🖥️ Backend

Python

Flask

📦 Database

ChromaDB (Vector DB)

🧠 LLM

Phi-2 (Quantized phi2Q_4_k.ggfu)

🔍 Embeddings

Hugging Face Models

🎨 Frontend

Flask Templates (HTML, CSS)

</details>
<details> <summary><h2>📥 Installation & Setup</h2></summary>
1️⃣ Clone Repo
git clone https://github.com/your-username/rag-pipeline.git
cd rag-pipeline

2️⃣ Create & Activate Virtual Environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Download Model

The Phi2Q_4_k.ggfu model is large (1.66 GB), so it’s not in this repo.
👉 Download Here
 and place inside models/ directory.

</details>
<details> <summary><h2>⚙️ Running the Pipeline</h2></summary>
▶️ Ingest Data
python ingest_data.py

▶️ Launch Web App
python app.py


✔️ Opens Flask Web UI
✔️ Accepts queries
✔️ Retrieves top-k matches
✔️ Refines with Phi-2 LLM
✔️ Displays final result

</details>
<details> <summary><h2>📂 Supported File & Link Types</h2></summary>

📄 PDF (.pdf)

📝 Word (.docx)

🎞️ PowerPoint (.ppt)

📜 Text (.txt)

🖼️ Images (.png, .jpeg)

🌐 Website URLs

▶️ YouTube video links

</details>
<details> <summary><h2>🖼️ Project Flow Diagram</h2></summary>
flowchart LR
    A[User Uploads Docs/Links] --> B[Chunking + Embeddings]
    B --> C[ChromaDB Storage]
    D[User Query] --> E[Retrieve Top-k Matches]
    E --> F[Phi-2 Model]
    F --> G[Polished Answer to User]

</details>
<details> <summary><h2>🎯 Example Usage</h2></summary>

Upload a PDF on quantum computing

Run ingest_data.py → indexed into ChromaDB

Start app.py → Ask: “Explain qubits in simple terms”

System retrieves context + Phi-2 generates a refined answer

</details>
<details> <summary><h2>📌 Notes</h2></summary>

🚫 Model not included (too large) → use provided download link

📦 Repo only contains code, configs, instructions

🗂️ Use .gitignore → exclude venv/ & large files

</details>
<details> <summary><h2>🤝 Contributing</h2></summary>

💡 Fork → Create a feature branch → Commit → Push → Submit PR 🚀

</details>
<details> <summary><h2>📜 License</h2></summary>

📄 Licensed under the MIT License

</details>
