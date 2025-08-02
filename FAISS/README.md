# FAQ Search API with FAISS

A simple but powerful FAQ search service that uses FAISS (Facebook AI Similarity Search) for vector similarity search and Sentence Transformers for creating semantic embeddings.

## Features

- **Semantic Search**: Uses sentence transformers to understand the meaning of queries, not just keyword matching
- **Fast Vector Search**: Powered by FAISS for efficient similarity search
- **RESTful API**: Built with FastAPI for easy integration
- **Easy Setup**: Simple ingestion script to load your own FAQ data

## Project Structure

```
FAISS/
├── main.py                 # FastAPI application with search endpoints
├── faq_ingest.py          # Script to ingest FAQ data and create vector index
├── test_api.py            # Test script to validate API functionality
├── FLOW_DIAGRAM.md        # Visual flow diagram of how the system works
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── data/                 # Generated data files
    ├── faq_index.index   # FAISS vector index
    └── faq_metadata.json # FAQ metadata with questions and answers
```

## Installation

1. **Clone the repository and navigate to the FAISS folder:**
   ```bash
   cd VectorDBExamples/FAISS
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

1. **Ingest FAQ data to create the vector index:**
   ```bash
   python faq_ingest.py
   ```
   This will create the FAISS index and metadata files in the `data/` directory.

2. **Start the API server:**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
   
   Alternatively, you can run the main.py directly:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

3. **Test the API:**
   Visit `http://localhost:8000/docs` for the interactive API documentation, or use the test script:
   ```bash
   python test_api.py
   ```
   
   Or test manually with curl:
   ```bash
   curl -X POST "http://localhost:8000/faq/search" \
        -H "Content-Type: application/json" \
        -d '{"query": "forgot my password", "top_k": 3}'
   ```

## API Endpoints

### POST /faq/search
Search for similar FAQs based on a natural language query.

**Request Body:**
```json
{
  "query": "How do I reset my password?",
  "top_k": 3
}
```

**Response:**
```json
{
  "results": [
    {
      "question": "How can I reset my password?",
      "answer": "To reset your password, click on 'Forgot Password' on the login screen and follow the instructions.",
      "score": 0.234
    }
  ]
}
```

### GET /
Basic information about the API.

### GET /health
Health check endpoint that shows if the index and metadata files are properly loaded.

## Customizing the FAQ Data

To add your own FAQ data, modify the `faq_data` list in `faq_ingest.py`:

```python
faq_data = [
    {
        "question": "Your question here",
        "answer": "Your answer here"
    },
    # Add more FAQs...
]
```

Then run the ingestion script again:
```bash
python faq_ingest.py
```

## How It Works

1. **Text Embedding**: Questions are converted to dense vector representations using the `all-MiniLM-L6-v2` sentence transformer model
2. **Vector Storage**: These embeddings are stored in a FAISS index for efficient similarity search
3. **Query Processing**: When a search query comes in, it's also converted to a vector using the same model
4. **Similarity Search**: FAISS finds the most similar FAQ vectors to the query vector
5. **Results Return**: The corresponding questions and answers are returned, ranked by similarity score

For a detailed visual flow diagram of the entire process, see [FLOW_DIAGRAM.md](FLOW_DIAGRAM.md).

## Technical Details

- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **FAISS Index Type**: `IndexFlatL2` (exact L2 distance search)
- **Distance Metric**: L2 (Euclidean) distance (lower scores = more similar)
- **API Framework**: FastAPI with automatic OpenAPI documentation

## Performance Considerations

- The current implementation uses `IndexFlatL2` which provides exact search but scales linearly with the number of FAQs
- For larger datasets (>100k FAQs), consider using approximate search indexes like `IndexIVFFlat` or `IndexHNSW`
- The sentence transformer model runs on CPU by default. For better performance with large query volumes, consider GPU acceleration

## Troubleshooting

### "FAQ index not found" error
Run `python faq_ingest.py` to create the index files.

### Import errors
Make sure all dependencies are installed: `pip install -r requirements.txt`

### Memory issues
If you're processing a large number of FAQs, consider processing them in batches in the ingestion script.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and demonstration purposes.
