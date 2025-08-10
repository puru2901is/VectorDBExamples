import streamlit as st
import requests
import pandas as pd
import json

# FastAPI backend URL
API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Job Search App", page_icon="🔍", layout="wide")

st.title("🔍 Job Search Application")
st.markdown("Search through job postings using different search methods")

# Sidebar for search options
st.sidebar.header("Search Options")
search_type = st.sidebar.selectbox(
    "Choose Search Type",
    ["All Jobs (Paginated)", "Exact Search", "Semantic Search", "Hybrid Search"]
)

def display_jobs(jobs_data):
    """Display jobs in a nice format"""
    if not jobs_data or "results" not in jobs_data or not jobs_data["results"]:
        st.warning("No jobs found!")
        return
    
    jobs = jobs_data["results"]
    st.success(f"Found {len(jobs)} job(s)")
    
    for i, job in enumerate(jobs):
        with st.expander(f"{job['job_title']} at {job['company']}", expanded=(i < 3)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Job ID:** {job['job_id']}")
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Skills:** {job['skills']}")
                if job.get('score'):
                    st.write(f"**Score:** {job['score']:.4f}")
                if job.get('distance'):
                    st.write(f"**Distance:** {job['distance']:.4f}")
            
            with col2:
                st.write("**Job Description:**")
                st.write(job['job_description'][:300] + "..." if len(job['job_description']) > 300 else job['job_description'])
                
            st.write("**Responsibilities:**")
            st.write(job['responsibilities'][:200] + "..." if len(job['responsibilities']) > 200 else job['responsibilities'])
            st.divider()

# Main content based on search type
if search_type == "All Jobs (Paginated)":
    st.header("📋 All Jobs")
    
    col1, col2 = st.columns(2)
    with col1:
        offset = st.number_input("Offset", min_value=0, value=0, step=10)
    with col2:
        limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
    
    if st.button("Load Jobs", type="primary"):
        try:
            response = requests.get(f"{API_BASE_URL}/jobs/all", params={"offset": offset, "limit": limit})
            if response.status_code == 200:
                jobs_data = response.json()
                display_jobs(jobs_data)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif search_type == "Exact Search":
    st.header("🎯 Exact/BM25 Search")
    st.markdown("Search across all job fields: Job ID, Job Title, Company, Location, Skills, Job Description, and Responsibilities")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        job_id = st.text_input("Job ID")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
    with col2:
        location = st.text_input("Location")
        skills = st.text_input("Skills")
    with col3:
        job_description = st.text_area("Job Description", height=100)
        responsibilities = st.text_area("Responsibilities", height=100)
    
    k = st.slider("Number of results", min_value=1, max_value=50, value=10)
    
    if st.button("Search", type="primary"):
        params = {"k": k}
        if job_id:
            params["job_id"] = job_id
        if job_title:
            params["job_title"] = job_title
        if company:
            params["company"] = company
        if location:
            params["location"] = location
        if skills:
            params["skills"] = skills
        if job_description:
            params["job_description"] = job_description
        if responsibilities:
            params["responsibilities"] = responsibilities
        
        try:
            response = requests.get(f"{API_BASE_URL}/search/exact", params=params)
            if response.status_code == 200:
                jobs_data = response.json()
                display_jobs(jobs_data)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif search_type == "Semantic Search":
    st.header("🧠 Semantic Search")
    st.markdown("Search using natural language and find semantically similar jobs")
    
    query = st.text_area("Enter your search query", placeholder="e.g., 'Machine learning engineer with Python experience'")
    k = st.slider("Number of results", min_value=1, max_value=50, value=10)
    
    if st.button("Search", type="primary") and query:
        try:
            payload = {"query": query, "k": k}
            response = requests.post(f"{API_BASE_URL}/search/semantic", json=payload)
            if response.status_code == 200:
                jobs_data = response.json()
                display_jobs(jobs_data)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif search_type == "Hybrid Search":
    st.header("⚡ Hybrid Search")
    st.markdown("Combine keyword and semantic search for best results")
    
    query = st.text_area("Enter your search query", placeholder="e.g., 'Data scientist with SQL and machine learning'")
    
    col1, col2 = st.columns(2)
    with col1:
        alpha = st.slider("Alpha (0=semantic, 1=keyword)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    with col2:
        k = st.slider("Number of results", min_value=1, max_value=50, value=10)
    
    st.info(f"Current balance: {int((1-alpha)*100)}% semantic + {int(alpha*100)}% keyword search")
    
    if st.button("Search", type="primary") and query:
        try:
            payload = {"query": query, "k": k, "alpha": alpha}
            response = requests.post(f"{API_BASE_URL}/search/hybrid", json=payload)
            if response.status_code == 200:
                jobs_data = response.json()
                display_jobs(jobs_data)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Load initial data on startup
if st.sidebar.button("🔄 Load Initial Data (10 jobs)"):
    try:
        response = requests.get(f"{API_BASE_URL}/jobs/all", params={"offset": 0, "limit": 10})
        if response.status_code == 200:
            jobs_data = response.json()
            st.header("📋 Initial Job Listings")
            display_jobs(jobs_data)
        else:
            st.error(f"Error loading initial data: {response.status_code}")
    except Exception as e:
        st.error(f"Could not load initial data: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Instructions:**")
st.sidebar.markdown("1. Make sure FastAPI server is running on localhost:8000")
st.sidebar.markdown("2. Choose a search type from the dropdown")
st.sidebar.markdown("3. Fill in search parameters and click Search")
st.sidebar.markdown("4. Use 'Load Initial Data' to see some sample jobs")
