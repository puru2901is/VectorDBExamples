# FAQ Search System - Flow Diagram

## System Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FAQ Data      │    │ Sentence        │    │   FAISS         │
│   (Questions &  │───▶│ Transformer     │───▶│   Vector        │
│   Answers)      │    │ Model           │    │   Index         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Metadata      │    │   Embeddings    │    │   Stored        │
│   JSON File     │    │   (384-dim      │    │   Vectors       │
│   (Q&A pairs)   │    │   vectors)      │    │   (IndexFlatL2) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Query Processing Flow

```
┌─────────────────┐
│  User Query     │
│ "forgot pass"   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FastAPI         │
│ Endpoint        │
│ /faq/search     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Sentence        │
│ Transformer     │
│ Encode Query    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Query Vector    │
│ [0.1, -0.3,     │
│  0.7, ...]      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FAISS           │
│ Similarity      │
│ Search          │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Top-K Similar   │
│ Vector Indices  │
│ [0, 3, 1]       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Lookup          │
│ Metadata        │
│ by Index        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Return Results  │
│ (Q, A, Score)   │
└─────────────────┘
```

## Detailed Step-by-Step Process

### Phase 1: Data Ingestion (faq_ingest.py)

```
1. FAQ Data Input
   ├── Load FAQ questions and answers
   └── Format: [{"question": "...", "answer": "..."}]

2. Text Embedding
   ├── Use SentenceTransformer("all-MiniLM-L6-v2")
   ├── Convert each question to 384-dimensional vector
   └── Output: numpy array of embeddings

3. Vector Index Creation
   ├── Create FAISS IndexFlatL2 (L2 distance)
   ├── Add all embeddings to index
   └── Save index to disk (faq_index.index)

4. Metadata Storage
   ├── Save question-answer pairs with indices
   └── Store as JSON (faq_metadata.json)
```

### Phase 2: Query Processing (main.py)

```
1. API Request
   ├── POST /faq/search
   ├── Input: {"query": "text", "top_k": 3}
   └── Validation with Pydantic models

2. Query Embedding
   ├── Use same SentenceTransformer model
   ├── Convert query to 384-dimensional vector
   └── Format as numpy array

3. Similarity Search
   ├── Load FAISS index from disk
   ├── Perform k-nearest neighbor search
   ├── Return distances and indices
   └── Lower distance = higher similarity

4. Result Assembly
   ├── Load metadata JSON
   ├── Map indices to question-answer pairs
   ├── Combine with similarity scores
   └── Format as API response

5. Response
   ├── Return JSON with results array
   └── Each result: {question, answer, score}
```

## Technical Details

### Vector Space
```
Question: "How to reset password?"
     ↓ (SentenceTransformer)
Vector: [0.1, -0.3, 0.7, 0.2, -0.1, ...] (384 dimensions)
     ↓ (FAISS IndexFlatL2)
Stored in index at position 0
```

### Similarity Calculation
```
Query Vector:    [0.1, -0.3, 0.7, ...]
FAQ Vector 1:    [0.2, -0.2, 0.8, ...]  → Distance: 0.38 (Similar!)
FAQ Vector 2:    [0.9, 0.5, -0.4, ...]  → Distance: 1.45 (Different)
FAQ Vector 3:    [-0.1, 0.1, 0.6, ...]  → Distance: 0.42 (Somewhat similar)

Lower distance = Higher similarity
```

### Data Flow
```
Request → Embedding → Search → Lookup → Response
  ↓           ↓          ↓        ↓        ↓
JSON      384-dim    Indices   Q&A     JSON
Input     Vector     [0,3,1]   Pairs   Output
```

## Performance Characteristics

- **Index Type**: IndexFlatL2 (Exact search)
- **Time Complexity**: O(n) where n = number of FAQs
- **Space Complexity**: O(n × d) where d = 384 dimensions
- **Scalability**: Good for <10k FAQs, consider IndexIVF for larger datasets

## Error Handling Flow

```
Request → Validation → File Check → Processing → Response
    ↓         ↓           ↓           ↓          ↓
  Valid?   Files OK?   Success?   Format OK?   200/500
    │         │           │           │          │
    └─No──────└─No────────└─No────────└─No──────┘
                            ↓
                      HTTP Error Response
```
