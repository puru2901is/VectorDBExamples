# Populate a vector index with embeddings from SentenceTransformer.
import boto3
import json
from sentence_transformers import SentenceTransformer

# Create S3 Vectors client and initialize SentenceTransformer model. 
s3vectors = boto3.client("s3vectors", region_name="us-east-1")
# Using a model that produces 1024-dimensional embeddings to match your S3 vector index
model = SentenceTransformer("sentence-transformers/all-roberta-large-v1")  # 1024 dimensions

# Texts to convert to embeddings.
texts = [
    "Star Wars: A farm boy joins rebels to fight an evil empire in space", 
    "Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong",
    "Finding Nemo: A father fish searches the ocean to find his lost son"
]

# Generate vector embeddings using SentenceTransformer.
embeddings = model.encode(texts)
# Convert numpy arrays to lists for S3 vectors API compatibility
embeddings = [embedding.tolist() for embedding in embeddings]

# Write embeddings into vector index with metadata.
# Note: This requires the S3 bucket and vector index to exist
try:
    s3vectors.put_vectors(
        vectorBucketName="media-embeddings",   
        indexName="movies",   
        vectors=[
            {
                "key": "Star Wars",
                "data": {"float32": embeddings[0]},
                "metadata": {"source_text": texts[0], "genre":"scifi"}
            },
            {
                "key": "Jurassic Park",
                "data": {"float32": embeddings[1]},
                "metadata": {"source_text": texts[1], "genre":"scifi"}
            },
            {
                "key": "Finding Nemo",
                "data": {"float32": embeddings[2]},
                "metadata": {"source_text": texts[2], "genre":"family"}
            }
        ]
    )
    print("Successfully ingested vectors to S3!")
except Exception as e:
    print(f"Error ingesting vectors: {e}")
    print("\nDemo: Showing what would be ingested:")
    print(f"Generated {len(embeddings)} embeddings with dimension {len(embeddings[0])}")
    for i, text in enumerate(texts):
        print(f"  {i+1}. {text[:50]}... -> embedding dimension: {len(embeddings[i])}")
    print("\nNote: To run this script successfully, you need:")
    print("1. AWS credentials configured")
    print("2. An S3 bucket named 'media-embeddings' with S3 vectors enabled")
    print("3. A vector index named 'movies' created in that bucket")