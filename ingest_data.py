# import os
# import glob
# from typing import List, Dict, Any
# from chromadb import PersistentClient
# from chromadb.utils import embedding_functions
# from sentence_transformers import SentenceTransformer
# from utils import *
# from config import Config

# class DataIngestor:
#     def __init__(self):
#         self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
#         self.client = PersistentClient(path=Config.VECTOR_DB_PATH)
#         self.collection = self.client.get_or_create_collection(
#             name=Config.COLLECTION_NAME,
#             embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
#                 model_name=Config.EMBEDDING_MODEL
#             )
#         )
    
#     def process_documents(self) -> int:
#         """Process all documents in the data directory."""
#         processed_count = 0
        
#         # Process local files
#         for ext in Config.SUPPORTED_EXTENSIONS:
#             pattern = os.path.join(Config.DATA_DIR, f"**/*{ext}")
#             for file_path in glob.glob(pattern, recursive=True):
#                 if self.process_file(file_path):
#                     processed_count += 1
        
#         # Process URLs from a urls.txt file if it exists
#         urls_file = os.path.join(Config.DATA_DIR, "urls.txt")
#         if os.path.exists(urls_file):
#             with open(urls_file, 'r') as f:
#                 urls = [line.strip() for line in f if line.strip()]
#                 for url in urls:
#                     if self.process_url(url):
#                         processed_count += 1
        
#         return processed_count
    
#     def process_file(self, file_path: str) -> bool:
#         """Process a single file."""
#         try:
#             print(f"Processing file: {file_path}")
            
#             if file_path.lower().endswith('.pdf'):
#                 text = extract_text_from_pdf(file_path)
#             else:
#                 with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
#                     text = f.read()
            
#             text = clean_text(text)
#             if not text:
#                 return False
            
#             chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
#             self._add_to_vector_db(chunks, file_path)
#             return True
            
#         except Exception as e:
#             print(f"Error processing file {file_path}: {e}")
#             return False
    
#     def process_url(self, url: str) -> bool:
#         """Process a URL."""
#         try:
#             print(f"Processing URL: {url}")
            
#             if 'youtube.com/' in url or 'youtu.be/' in url:
#                 text = extract_transcript_from_youtube(url)
#             else:
#                 text = extract_text_from_website(url)
            
#             text = clean_text(text)
#             if not text:
#                 return False
            
#             chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
#             self._add_to_vector_db(chunks, url)
#             return True
            
#         except Exception as e:
#             print(f"Error processing URL {url}: {e}")
#             return False
    
#     def _add_to_vector_db(self, chunks: List[str], source: str):
#         """Add chunks to vector database."""
#         documents = []
#         metadatas = []
#         ids = []
        
#         for i, chunk in enumerate(chunks):
#             if len(chunk.strip()) < 50:  # Skip very short chunks
#                 continue
                
#             doc_id = generate_document_id(chunk, f"{source}_{i}")
#             documents.append(chunk)
#             metadatas.append({
#                 "source": source,
#                 "chunk_index": i,
#                 "chunk_length": len(chunk)
#             })
#             ids.append(doc_id)
        
#         if documents:
#             self.collection.add(
#                 documents=documents,
#                 metadatas=metadatas,
#                 ids=ids
#             )
#             print(f"Added {len(documents)} chunks from {source}")

# def main():
#     """Main function to ingest data."""
#     # Create directories if they don't exist
#     os.makedirs(Config.DATA_DIR, exist_ok=True)
#     os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
    
#     ingestor = DataIngestor()
#     processed_count = ingestor.process_documents()
    
#     print(f"Data ingestion complete. Processed {processed_count} sources.")
#     print(f"Vector database created at: {Config.VECTOR_DB_PATH}")

# if __name__ == "__main__":
#     main()

import os
import glob
from typing import List, Dict, Any
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from utils import *
from config import Config

class DataIngestor:
    def __init__(self):
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.client = PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=Config.EMBEDDING_MODEL
            )
        )
    
    def process_documents(self) -> int:
        """Process all documents in the data directory."""
        processed_count = 0
        
        # Process local files (skip urls.txt)
        for ext in Config.SUPPORTED_EXTENSIONS:
            pattern = os.path.join(Config.DATA_DIR, f"**/*{ext}")
            for file_path in glob.glob(pattern, recursive=True):
                # Skip urls.txt file
                if file_path.endswith('urls.txt'):
                    continue
                if self.process_file(file_path):
                    processed_count += 1
        
        # Process URLs from urls.txt file if it exists
        urls_file = os.path.join(Config.DATA_DIR, "urls.txt")
        if os.path.exists(urls_file):
            processed_count += self.process_urls_file(urls_file)
        
        return processed_count
    
    def process_urls_file(self, urls_file_path: str) -> int:
        """Process URLs from urls.txt file."""
        processed_count = 0
        try:
            with open(urls_file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            for url in urls:
                if self.process_url(url):
                    processed_count += 1
                    
        except Exception as e:
            print(f"Error processing URLs file {urls_file_path}: {e}")
        
        return processed_count
    
    def process_file(self, file_path: str) -> bool:
        """Process a single file."""
        try:
            print(f"Processing file: {file_path}")
            
            if file_path.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            text = clean_text(text)
            if not text:
                print(f"No text extracted from {file_path}")
                return False
            
            chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
            if not chunks:
                print(f"No chunks created from {file_path}")
                return False
                
            self._add_to_vector_db(chunks, file_path)
            return True
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return False
    
    def process_url(self, url: str) -> bool:
        """Process a URL."""
        try:
            print(f"Processing URL: {url}")
            
            if 'youtube.com/' in url or 'youtu.be/' in url:
                text = extract_transcript_from_youtube(url)
            else:
                text = extract_text_from_website(url)
            
            text = clean_text(text)
            if not text:
                print(f"No text extracted from URL {url}")
                return False
            
            chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
            if not chunks:
                print(f"No chunks created from URL {url}")
                return False
                
            self._add_to_vector_db(chunks, url)
            return True
            
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return False
    
    def _add_to_vector_db(self, chunks: List[str], source: str):
        """Add chunks to vector database."""
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
                
            doc_id = generate_document_id(chunk, f"{source}_{i}")
            documents.append(chunk)
            metadatas.append({
                "source": source,
                "chunk_index": i,
                "chunk_length": len(chunk)
            })
            ids.append(doc_id)
        
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Added {len(documents)} chunks from {source}")

def main():
    """Main function to ingest data."""
    # Create directories if they don't exist
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
    
    ingestor = DataIngestor()
    processed_count = ingestor.process_documents()
    
    print(f"Data ingestion complete. Processed {processed_count} sources.")
    print(f"Vector database created at: {Config.VECTOR_DB_PATH}")

if __name__ == "__main__":
    main()