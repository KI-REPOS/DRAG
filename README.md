📚 Retrieval-Augmented Generation (RAG) Pipeline

This project implements a RAG pipeline using ChromaDB + Flask.
Users can upload documents (PDF, DOCX, PPT, TXT, PNG, JPEG) and URLs (websites, YouTube videos).
The system converts them into vector embeddings, stores them in ChromaDB, and allows interactive querying with an LLM.

<details> <summary>✨ Features</summary>

📂 Ingest multiple document types (PDF, DOCX, PPT, TXT, PNG, JPEG)

🌐 Accept websites & YouTube video links

🧩 Automatic chunking + vector embeddings

🗄️ Storage in ChromaDB

🤖 Query interface powered by Flask

✨ Results refined with Phi-2 (quantized) model

🖥️ Clean web UI for interaction

</details>
<details> <summary>🛠️ Project Workflow</summary>

Add Documents → Run ingest_data.py (processes input → embeddings → ChromaDB).

Query System → Run app.py (Flask UI → query → retrieve → LLM refinement).

Results → See polished answers in the web interface.

</details>
<details> <summary>⚡ Tech Stack</summary>

Backend → Python, Flask

Vector DB → ChromaDB

LLM → Phi-2 Quantized (phi2Q_4_k.ggfu)

Embeddings → Hugging Face Models

Frontend → Flask + HTML Templates

</details>
<details> <summary>📥 Installation & Setup</summary>
1️⃣ Clone the repo
git clone https://github.com/your-username/rag-pipeline.git
cd rag-pipeline

2️⃣ Create & activate virtual environment
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Download Model

The Phi2Q_4_k.ggfu model is large, so it’s not included in this repo.
👉 Download Here
 and place it in the models/ directory.

</details>
<details> <summary>⚙️ Running the Pipeline</summary>
Step 1: Ingest Data
python ingest_data.py


✔️ Converts input files/links into chunks
✔️ Generates embeddings
✔️ Stores them in ChromaDB

Step 2: Run Flask App
python app.py


✔️ Launches the web interface
✔️ Accepts user queries
✔️ Retrieves top-k relevant chunks
✔️ Refines answers using Phi-2 model
✔️ Displays results to user

</details>
<details> <summary>📂 Supported File & Link Types</summary>

PDF (.pdf)

Word (.docx)

PowerPoint (.ppt)

Text (.txt)

Images (.png, .jpeg)

Website URLs

YouTube video links

</details>
<details> <summary>🖼️ Project Flow Diagram</summary>
flowchart LR
    A[User Uploads Docs/Links] --> B[Chunking + Embeddings]
    B --> C[ChromaDB Storage]
    D[User Query] --> E[Retrieve Top-k Matches]
    E --> F[Phi-2 Model]
    F --> G[Polished Answer to User]

</details>
<details> <summary>🎯 Example Usage</summary>

Upload a PDF on quantum computing.

Run ingest_data.py → indexed into ChromaDB.

Start app.py → Ask: “Explain qubits in simple terms”.

System retrieves context + Phi-2 generates a polished answer.

</details>
<details> <summary>📌 Notes</summary>

Model is not included due to size (1.66 GB).

Use external download link provided.

Repo includes only code, configs, and instructions.

Add venv/ and large files to .gitignore.

</details>
<details> <summary>🤝 Contributing</summary>

Pull requests and feature suggestions are welcome!
Fork this repo → make changes → submit PR 🚀

</details>
<details> <summary>📜 License</summary>

This project is licensed under the MIT License.

</details>
