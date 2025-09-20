from typing import List, Dict, Any, Tuple
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from llm_model import LocalLLM, ConversationManager
from config import Config

class RAGPipeline:
    def __init__(self):
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.llm = LocalLLM()
        self.conversation_manager = ConversationManager(self.llm)
        
        # Initialize vector database
        self.client = PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.client.get_collection(
            Config.COLLECTION_NAME,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=Config.EMBEDDING_MODEL
            )
        )
    
    def query(self, question: str) -> Tuple[str, List[Dict]]:
        """Process a query and return response with sources."""
        # Retrieve relevant documents
        results = self.collection.query(
            query_texts=[question],
            n_results=Config.TOP_K_RESULTS
        )
        
        # Format context from retrieved documents
        context, sources = self._format_context(results)
        
        # Build prompt with conversation history and context
        prompt = self._build_prompt(question, context)
        
        # Generate response
        response = self.llm.generate_response(prompt)
        
        # Update conversation history
        self.conversation_manager.add_message("user", question)
        self.conversation_manager.add_message("assistant", response)
        
        return response, sources
    
    def _format_context(self, results: Dict) -> Tuple[str, List[Dict]]:
        """Format retrieved context and extract sources."""
        context_parts = []
        sources = []
        
        if results and 'documents' in results and results['documents']:
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], 
                                                  results['metadatas'][0])):
                context_parts.append(f"[Document {i+1}]: {doc}")
                sources.append({
                    "content": doc,
                    "source": metadata.get('source', 'Unknown'),
                    "chunk_index": metadata.get('chunk_index', 0)
                })
        
        return "\n\n".join(context_parts), sources
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build the prompt for the LLM."""
        conversation_context = self.conversation_manager.get_conversation_context()
        
        prompt = f"""You are a cyber-forensics expert assistant. Help investigators with questions about hardware, USBs, cameras, system analysis, and digital forensics.

Use the following context information to answer the question. If the context doesn't contain relevant information, use your knowledge but be clear about the limitations.

Context Information:
{context}

{'Previous Conversation:' if conversation_context else ''}
{conversation_context}

Current Question: {question}

Instructions:
- Provide clear, technical answers suitable for investigators
- Cite sources when referring to specific documents
- Be precise and factual
- If unsure, say so and suggest where to find more information

Assistant: """
        
        return prompt
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_manager.clear_history()