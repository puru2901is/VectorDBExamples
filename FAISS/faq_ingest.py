from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import os

faq_data = [
    {
        "question": "How can I reset my password?",
        "answer": "To reset your password, click on 'Forgot Password' on the login screen and follow the instructions."
    },
    {
        "question": "Where can I view my purchase history?",
        "answer": "You can find your purchase history under the 'Orders' section in your account dashboard."
    },
    {
        "question": "How do I update my email address?",
        "answer": "Go to your account settings and edit your email address under 'Personal Information'."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can contact our support team via the 'Help & Support' section or email us at support@example.com."
    },
    {
        "question": "What is the return policy?",
        "answer": "You can return any item within 30 days of delivery for a full refund. See our return policy page for details."
    }
]


model = SentenceTransformer("all-MiniLM-L6-v2")

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
faq_index_path = os.path.join(data_dir, "faq_index.index")
faq_meta_path = os.path.join(data_dir, "faq_metadata.json")

# Load or create index
def get_faq_index(dim):
    if os.path.exists(faq_index_path):
        return faiss.read_index(faq_index_path)
    else:
        return faiss.IndexFlatL2(dim)

# Save metadata
def save_faq_metadata(entries):
    if os.path.exists(faq_meta_path):
        with open(faq_meta_path, "r") as f:
            metadata = json.load(f)
    else:
        metadata = []

    metadata.extend(entries)
    with open(faq_meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

# Ingest all FAQs
def ingest_faqs(faq_data):
    questions = [faq["question"] for faq in faq_data]
    embeddings = model.encode(questions)
    embeddings_np = np.array(embeddings, dtype='float32')

    index = get_faq_index(embeddings_np.shape[1])
    start_index = index.ntotal
    index.add(embeddings_np)
    faiss.write_index(index, faq_index_path)

    metadata_entries = []
    for i, faq in enumerate(faq_data):
        metadata_entries.append({
            "question": faq["question"],
            "answer": faq["answer"],
            "vector_index": start_index + i
        })
    save_faq_metadata(metadata_entries)
    print(f"Ingested {len(faq_data)} FAQs.")

# Call this once
ingest_faqs(faq_data)
