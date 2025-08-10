curl -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{
    "class": "JobPosting",
    "vectorizer": "text2vec-ollama",
    "moduleConfig": {
      "text2vec-ollama": {
        "apiEndpoint": "http://host.docker.internal:11434",
        "model": "nomic-embed-text"
      }
    },
    "properties": [
      {
        "name": "job_id",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "job_title",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "company",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "location",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "skills",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "job_description",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "responsibilities",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-ollama": { "skip": true } },
        "tokenization": "word"
      },
      {
        "name": "search_text",
        "dataType": ["text"],
        "tokenization": "word"
        // This property will be vectorized (no skip)
      }
    ]
  }'
