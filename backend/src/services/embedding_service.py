from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 200
        self.index = None
        self.chunks = []

    def create_chunks(self, text: str) -> List[str]:
        print(f"\n=== DEBUG: CREAZIONE CHUNKS ===")
        words = text.split()
        chunks = [' '.join(words[i:i + self.chunk_size]) for i in range(0, len(words), self.chunk_size)]
        print(f"Creati {len(chunks)} chunks")
        return chunks

    def index_documents(self, documents: List[str]):
        print(f"\n=== DEBUG: INDICIZZAZIONE DOCUMENTI ===")
        print(f"Documenti da processare: {len(documents)}")
        
        self.chunks = []
        for i, doc in enumerate(documents):
            print(f"Processando documento {i+1}...")
            doc_chunks = self.create_chunks(doc)
            self.chunks.extend(doc_chunks)
        
        if not self.chunks:
            print("ERRORE: Nessun chunk creato!")
            return
        
        print(f"Creazione embedding per {len(self.chunks)} chunks...")
        embeddings = self.model.encode(self.chunks)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print(f"Indicizzazione completata: {len(self.chunks)} chunks indicizzati")

    def find_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        print(f"\n=== DEBUG: RICERCA CHUNKS PER QUERY: {query} ===")
        if self.index is None or len(self.chunks) == 0:
            print("ERRORE: Nessun indice disponibile!")
            return []
            
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        print(f"Trovati {len(indices[0])} chunks rilevanti")
        relevant_chunks = [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
        for i, chunk in enumerate(relevant_chunks):
            print(f"Chunk {i+1} (primi 100 caratteri):")
            print(chunk[:100])
        return relevant_chunks