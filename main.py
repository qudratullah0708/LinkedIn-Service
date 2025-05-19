
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Lead , Leads, QueryRequest
from tavily_search import Retrieve_news
from Output_parser import Output_Parser

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.post("/extract-leads", response_model=Leads)
async def extract_leads(request: QueryRequest):
    try:
        leads = Output_Parser(request.query)
        return Leads(leads=leads)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))