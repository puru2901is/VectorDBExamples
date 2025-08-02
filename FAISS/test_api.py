#!/usr/bin/env python3
"""
Simple test script to demonstrate the FAQ Search API functionality.
Make sure the server is running before executing this script.
"""

import requests
import json
import sys

# API endpoint
BASE_URL = "http://127.0.0.1:8002"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search(query, top_k=3):
    """Test the search endpoint"""
    print(f"Searching for: '{query}'")
    
    payload = {
        "query": query,
        "top_k": top_k
    }
    
    response = requests.post(
        f"{BASE_URL}/faq/search",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        results = response.json()
        print(f"Found {len(results['results'])} results:")
        for i, result in enumerate(results['results'], 1):
            print(f"\n{i}. Question: {result['question']}")
            print(f"   Answer: {result['answer']}")
            print(f"   Score: {result['score']:.4f}")
    else:
        print(f"Error: {response.text}")
    print("-" * 80)

def main():
    print("FAQ Search API Test Script")
    print("=" * 80)
    
    try:
        # Test health endpoint
        test_health()
        
        # Test various search queries
        test_queries = [
            "forgot my password",
            "purchase history",
            "return item",
            "contact support",
            "update email address"
        ]
        
        for query in test_queries:
            test_search(query)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://127.0.0.1:8002")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
