from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import weaviate
import weaviate.classes.query as wq

app = FastAPI()

# Connect to local Weaviate instance
client = weaviate.connect_to_local()

COLLECTION_NAME = "JobPosting"  # Change if using a different collection name

class JobResult(BaseModel):
    job_id: str
    job_title: str
    company: str
    location: str
    skills: str
    job_description: str
    responsibilities: str
    search_text: str
    score: Optional[float] = None
    distance: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[JobResult]

class SemanticSearchRequest(BaseModel):
    query: str
    k: Optional[int] = 10

class HybridSearchRequest(BaseModel):
    query: str
    k: Optional[int] = 10
    alpha: Optional[float] = 0.5

@app.get("/search/exact", response_model=SearchResponse)
def exact_search(
    job_id: Optional[str] = Query(None),
    job_title: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    skills: Optional[str] = Query(None),
    job_description: Optional[str] = Query(None),
    responsibilities: Optional[str] = Query(None),
    k: int = Query(10)
):
    """
    Exact/BM25 keyword search on JobPosting collection across all fields.
    """
    try:
        collection = client.collections.get(COLLECTION_NAME)
        filters = []
        if job_id:
            filters.append(wq.Filter.by_property("job_id").equal(job_id))
        if job_title:
            filters.append(wq.Filter.by_property("job_title").contains_any([job_title]))
        if company:
            filters.append(wq.Filter.by_property("company").contains_any([company]))
        if location:
            filters.append(wq.Filter.by_property("location").contains_any([location]))
        if skills:
            filters.append(wq.Filter.by_property("skills").contains_any([skills]))
        if job_description:
            filters.append(wq.Filter.by_property("job_description").contains_any([job_description]))
        if responsibilities:
            filters.append(wq.Filter.by_property("responsibilities").contains_any([responsibilities]))
        where = None
        if filters:
            where = filters[0]
            for f in filters[1:]:
                where = where & f
        # BM25 search on all fields
        bm25_kwargs = {
            "query": " ".join([v for v in [job_id, job_title, company, location, skills, job_description, responsibilities] if v]),
            "limit": k,
            "return_metadata": wq.MetadataQuery(score=True)
        }
        if where:
            bm25_kwargs["filters"] = where
        response = collection.query.bm25(**bm25_kwargs)
        results = [JobResult(**obj.properties, score=getattr(obj.metadata, 'score', None)) for obj in response.objects]
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/semantic", response_model=SearchResponse)
def semantic_search(request: SemanticSearchRequest):
    """
    Semantic/vector search on JobPosting collection (search_text field).
    """
    try:
        collection = client.collections.get(COLLECTION_NAME)
        response = collection.query.near_text(
            query=request.query,
            limit=request.k,
            return_metadata=wq.MetadataQuery(distance=True)
        )
        results = [JobResult(**obj.properties, distance=getattr(obj.metadata, 'distance', None)) for obj in response.objects]
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/hybrid", response_model=SearchResponse)
def hybrid_search(request: HybridSearchRequest):
    """
    Hybrid search (BM25 + vector) on JobPosting collection (search_text field).
    """
    try:
        collection = client.collections.get(COLLECTION_NAME)
        response = collection.query.hybrid(
            query=request.query,
            limit=request.k,
            alpha=request.alpha,
            fusion_type=wq.HybridFusion.RELATIVE_SCORE,
            return_metadata=wq.MetadataQuery(score=True, distance=True)
        )
        results = [JobResult(**obj.properties, score=getattr(obj.metadata, 'score', None), distance=getattr(obj.metadata, 'distance', None)) for obj in response.objects]
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/jobs/all", response_model=SearchResponse)
def get_all_jobs(offset: int = Query(0, ge=0), limit: int = Query(10, gt=0, le=100)):
    """
    Get all jobs in the collection with pagination.
    """
    try:
        collection = client.collections.get(COLLECTION_NAME)
        response = collection.query.fetch_objects(
            offset=offset,
            limit=limit
        )
        results = [JobResult(**obj.properties) for obj in response.objects]
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    client.close()
