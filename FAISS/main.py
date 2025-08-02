from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import os

app = FastAPI(title="FAQ Search API", description="A simple FAQ search service using FAISS and sentence transformers")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Use absolute paths to ensure the files are found regardless of working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
faq_index_path = os.path.join(data_dir, "faq_index.index")
faq_meta_path = os.path.join(data_dir, "faq_metadata.json")

class FAQSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class FAQSearchResult(BaseModel):
    question: str
    answer: str
    score: float

class FAQSearchResponse(BaseModel):
    results: List[FAQSearchResult]

@app.post("/faq/search", response_model=FAQSearchResponse)
async def faq_search(request: FAQSearchRequest):
    try:
        # Check if files exist
        if not os.path.exists(faq_index_path):
            raise HTTPException(status_code=404, detail="FAQ index not found. Please run faq_ingest.py first.")
        if not os.path.exists(faq_meta_path):
            raise HTTPException(status_code=404, detail="FAQ metadata not found. Please run faq_ingest.py first.")
        
        # Encode the query
        query_embedding = model.encode([request.query])
        query_np = np.array(query_embedding, dtype='float32')

        # Load index and search
        index = faiss.read_index(faq_index_path)
        D, I = index.search(query_np, request.top_k)

        # Load metadata
        with open(faq_meta_path, 'r') as f:
            metadata = json.load(f)

        # Prepare results
        results = []
        for idx, score in zip(I[0], D[0]):
            if idx < len(metadata):  # Check bounds
                meta = metadata[idx]
                results.append(FAQSearchResult(
                    question=meta["question"],
                    answer=meta["answer"],
                    score=float(score)
                ))

        return FAQSearchResponse(results=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "FAQ Search API is running! Use POST /faq/search to search FAQs."}

@app.get("/health")
async def health_check():
    index_exists = os.path.exists(faq_index_path)
    metadata_exists = os.path.exists(faq_meta_path)
    return {
        "status": "healthy" if index_exists and metadata_exists else "not ready",
        "index_exists": index_exists,
        "metadata_exists": metadata_exists
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
