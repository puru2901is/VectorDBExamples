import pandas as pd

# Load your dataset
# Update the filename if needed
filename = "job_descriptions.csv"  # or "large_job_dataset.csv" if that's the actual file

df = pd.read_csv(filename)

# --- 1. Keep only useful columns for demo ---
keep_cols = [
    "Job Id", "Job Title", "Company", "location", "skills", 
    "Job Description", "Responsibilities"
]
df = df[keep_cols]

# --- 2. Drop duplicates & rows missing critical info ---
df = df.drop_duplicates(subset=["Job Id"])
df = df.dropna(subset=["Job Title", "Job Description"])

# --- 3. Create search_text column for semantic search ---
def make_search_text(row):
    parts = [
        row.get("Job Title", ""),
        row.get("Job Description", ""),
        row.get("skills", ""),
        row.get("Responsibilities", "")
    ]
    return " ".join([str(p) for p in parts if pd.notnull(p)])

df["search_text"] = df.apply(make_search_text, axis=1)

# --- 4. Sample smaller dataset for demo ---
demo_df = df.sample(n=300, random_state=42)  # adjust n for speed

# --- 5. Save cleaned demo data ---
demo_df.to_csv("job_dataset_demo.csv", index=False)

print(f"Original size: {len(df)} rows")
print(f"Sampled size: {len(demo_df)} rows")
print("Saved to job_dataset_demo.csv")
