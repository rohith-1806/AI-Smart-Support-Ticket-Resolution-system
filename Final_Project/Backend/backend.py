import os
from contextlib import asynccontextmanager
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np

# Global Knowledge Base Engine instance
kb_engine = None

class KnowledgeBaseEngine:
    def __init__(self):
        self.use_fallback = False
        self.vector_store = None
        self.retriever = None
        self.documents = []
        self.df = None
        
        # Fallback components
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None

        print("Initializing Knowledge Base Engine...")
        try:
            # Check if we can actually connect to Ollama by trying to initialize embeddings
            # (Lazy init might not throw immediately, but we will try-catch the actual load)
            self.llm = ChatOllama(model="llama3.2:1b")
            self.embeddings = OllamaEmbeddings(model="llama3.2:1b")
            
            # Attempt to embed a dummy string to verifiy connection
            self.embeddings.embed_query("test")
            
            print("Ollama connection successful. using Vector Store.")
            self._initialize_vector_knowledge_base()
        except Exception as e:
            print(f"Ollama not detected or error occurred: {e}. Switching to Fallback (TF-IDF).")
            self.use_fallback = True
            self._initialize_fallback_knowledge_base()

    def _initialize_vector_knowledge_base(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, 'knowledge_base.csv')
            self.df = pd.read_csv(csv_path)
            self.documents = list(self.df['article'])
            self.vector_store = FAISS.from_texts(self.documents, self.embeddings)
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            print("Vector Knowledge Base initialized.")
        except Exception as e:
            print(f"Error initializing vector store: {e}. Fallback enabled.")
            self.use_fallback = True
            self._initialize_fallback_knowledge_base()

    def _initialize_fallback_knowledge_base(self):
        # Simple TF-IDF based recommendation
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, 'knowledge_base.csv')
            self.df = pd.read_csv(csv_path)
            self.documents = list(self.df['article'])
            
            self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)
            print("Fallback TF-IDF Knowledge Base initialized.")
        except Exception as e:
             print(f"CRITICAL: Could not initialize fallback knowledge base: {e}")

    def recommend_articles(self, ticket_content: str) -> List[str]:
        if not ticket_content:
            return []

        if self.use_fallback:
            return self._recommend_fallback(ticket_content)
        else:
            return self._recommend_vector(ticket_content)

    def _recommend_vector(self, ticket_content: str):
        try:
            docs = self.retriever.invoke(ticket_content)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error during vector retrieval: {e}. Using fallback.")
            return self._recommend_fallback(ticket_content)

    def _recommend_fallback(self, ticket_content: str):
        # Compute cosine similarity between query and all documents
        try:
            if self.tfidf_matrix is None:
               return ["Knowledge base not initialized."]
               
            query_vec = self.tfidf_vectorizer.transform([ticket_content])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Get top 3 indices
            top_indices = similarities.argsort()[-3:][::-1]
            
            # Filter out results with 0 similarity (irrelevant)
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:
                    results.append(self.documents[idx])
            
            if not results:
                return ["No relevant articles found in the knowledge base."]
                
            return results
        except Exception as e:
             return [f"Error in recommendation: {str(e)}"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model on startup
    global kb_engine
    kb_engine = KnowledgeBaseEngine()
    yield
    # Clean up resources if needed
    pass

app = FastAPI(title="Knowledge Management Platform API", lifespan=lifespan)

class Ticket(BaseModel):
    content: str

@app.post("/recommend")
def recommend_content(ticket: Ticket):
    try:
        if kb_engine is None:
             raise HTTPException(status_code=503, detail="Knowledge Engine not initialized")
        
        recommendations = kb_engine.recommend_articles(ticket.content)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "active", "model": "llama3.2:1b"}
