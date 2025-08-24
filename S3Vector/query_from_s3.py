# Query a vector index with an embedding from SentenceTransformer.
import boto3 
import json
from sentence_transformers import SentenceTransformer 

# Create S3 Vectors client and initialize SentenceTransformer model. 
s3vectors = boto3.client("s3vectors", region_name="us-east-1")
# Using a model that produces 1024-dimensional embeddings to match your S3 vector index
model = SentenceTransformer("sentence-transformers/all-roberta-large-v1")  # 1024 dimensions 

# Query text to convert to an embedding. 
input_text = "adventures in space"

# Generate the vector embedding using SentenceTransformer.
embedding = model.encode([input_text])[0].tolist()

# Query vector index.
try:
    response = s3vectors.query_vectors(
        vectorBucketName="media-embeddings",
        indexName="movies",
        queryVector={"float32": embedding}, 
        topK=3, 
        returnDistance=True,
        returnMetadata=True
    )
    print("Query results:")
    print(json.dumps(response["vectors"], indent=2))

    # Query vector index with a metadata filter.
    response = s3vectors.query_vectors(
        vectorBucketName="media-embeddings",
        indexName="movies",
        queryVector={"float32": embedding}, 
        topK=3, 
        filter={"genre": "scifi"},
        returnDistance=True,
        returnMetadata=True
    )
    print("\nFiltered query results (scifi only):")
    print(json.dumps(response["vectors"], indent=2))
    
except Exception as e:
    print(f"Error querying vectors: {e}")
    print(f"\nDemo: Generated embedding for query '{input_text}'")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print("\nNote: To run this script successfully, you need:")
    print("1. AWS credentials configured")
    print("2. An S3 bucket named 'media-embeddings' with S3 vectors enabled")
    print("3. A vector index named 'movies' with ingested data")
    