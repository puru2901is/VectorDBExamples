import weaviate
import pandas as pd

# Connect to local Weaviate instance
client = weaviate.connect_to_local()

# Load job dataset from CSV
csv_path = "job_dataset_demo.csv"
df = pd.read_csv(csv_path)

# Get the JobPosting collection
job_collection = client.collections.get("JobPosting")

# Prepare batch insert
with job_collection.batch.fixed_size(batch_size=100) as batch:
    for _, row in df.iterrows():
        obj = {
            "job_id": str(row.get("Job Id", "")),
            "job_title": str(row.get("Job Title", "")),
            "company": str(row.get("Company", "")),
            "location": str(row.get("location", "")),
            "skills": str(row.get("skills", "")),
            "job_description": str(row.get("Job Description", "")),
            "responsibilities": str(row.get("Responsibilities", "")),
            "search_text": str(row.get("search_text", "")),
        }
        batch.add_object(obj)
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = job_collection.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")
else:
    print("✅ All objects imported successfully!")

client.close()  # Free up resources
