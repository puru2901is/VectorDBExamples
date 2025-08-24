# S3 Vector Database Examples

This directory contains examples for working with AWS S3 Vector databases using SentenceTransformer embeddings.

## Setup

1. Create a virtual environment:
```bash
cd /Users/pubaghel/Documents/learning/myGit/VectorDBExamples/S3Vector
source s3vector_env/bin/activate
pip install -r requirements.txt
python query_from_s3.py
```

## Files

- `ingest_to_s3.py` - Ingests movie descriptions as vectors into S3
- `query_from_s3.py` - Queries the S3 vector database
- `requirements.txt` - Python dependencies

## Usage

### Ingest Data
```bash
python ingest_to_s3.py
```

### Query Data  
```bash
python query_from_s3.py
```

## Prerequisites

To run these scripts successfully, you need:

1. **AWS credentials configured** (via AWS CLI, environment variables, or IAM roles)
2. **An S3 bucket** with S3 vectors enabled (e.g., 'media-embeddings')
3. **A vector index** created in that bucket (e.g., 'movies')

## Index Configuration

Your S3 Vector index configuration:
- **Distance Metric**: COSINE
- **Dimensions**: 1024  
- **Data Type**: float32

## Demo Mode

The scripts include error handling and will show demo output even if AWS resources aren't configured, making them useful for learning purposes.

## Embedding Model

Uses SentenceTransformer `sentence-transformers/all-roberta-large-v1` model for generating 1024-dimensional embeddings locally to match the S3 vector index dimensions.

## Understanding Distance Values

The query results show **cosine distances** where:
- **Lower values** = better matches
- **Distance range**: 0.0 (perfect match) to 2.0 (complete opposite)
- **Convert to similarity**: `cosine_similarity = 1 - cosine_distance`

### Cosine Distance vs Cosine Similarity

#### **Cosine Similarity**
- **Range**: -1 to +1
- **Formula**: `dot(A, B) / (||A|| * ||B||)`
- **Interpretation**:
  - `+1`: Identical direction (perfect match)
  - `0`: Orthogonal (90° angle, no similarity)
  - `-1`: Opposite direction (180° angle)
- **Higher values = more similar**

#### **Cosine Distance** 
- **Range**: 0 to 2
- **Formula**: `1 - cosine_similarity`
- **Interpretation**:
  - `0`: Identical vectors (perfect match)
  - `1`: Orthogonal vectors (no similarity)
  - `2`: Opposite vectors
- **Lower values = more similar**

#### **Quick Conversion**
```python
cosine_distance = 1 - cosine_similarity
cosine_similarity = 1 - cosine_distance
```

#### **Example from S3 Results**
```python
# Your distance: 1.026
cosine_similarity = 1 - 1.026 = -0.026  # Slightly opposite direction
cosine_distance = 1.026                  # What S3 returns
```

**Key Point**: Your S3 Vector index returns **cosine distance** (lower = better), while many ML contexts use **cosine similarity** (higher = better). They're just inverse relationships of the same underlying measurement!