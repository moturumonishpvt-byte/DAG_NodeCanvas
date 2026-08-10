import json
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from graph_utils import calculate_pipeline_stats

app = FastAPI()

# Defensively add CORS middleware so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    try:
        # Parse the JSON string from the form data
        pipeline_dict = json.loads(pipeline)
        
        # Extract nodes and edges
        nodes = pipeline_dict.get("nodes", [])
        edges = pipeline_dict.get("edges", [])
        
        if not isinstance(nodes, list) or not isinstance(edges, list):
            raise HTTPException(status_code=400, detail="Nodes and edges must be lists.")
            
        # Calculate stats (num_nodes, num_edges, is_dag)
        stats = calculate_pipeline_stats(nodes, edges)
        
        return stats
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in pipeline form data")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
