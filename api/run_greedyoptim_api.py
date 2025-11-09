#!/usr/bin/env python3
"""
Startup script for GreedyOptim API
Run this to start the advanced optimization API service
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("GreedyOptim Scheduling API")
    print("=" * 70)
    print()
    print("Starting FastAPI server on port 8001...")
    print()
    print("API Documentation:      http://localhost:8001/docs")
    print("Alternative Docs:       http://localhost:8001/redoc")
    print("Health Check:           http://localhost:8001/health")
    print("Available Methods:      http://localhost:8001/methods")
    print()
    print("Main Endpoints:")
    print("  POST /optimize              - Optimize with custom data")
    print("  POST /compare               - Compare multiple methods")
    print("  POST /generate-synthetic    - Generate test data")
    print("  POST /validate              - Validate data structure")
    print()
    print("=" * 70)
    print()
    
    # Run the API
    uvicorn.run(
        "api.greedyoptim_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
