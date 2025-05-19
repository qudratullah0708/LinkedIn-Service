
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Lead , Leads
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
async def extract_leads( query: str):
    try:
        # Call the Output_Parser function
        leads = Output_Parser(query)
        # return {"leads": leads}  # Return the leads directly as a dictionary
        return Leads(leads=leads)
    except Exception as e:
        # If any error occurs, return an HTTP 400 Bad Request response
        raise HTTPException(status_code=400, detail=str(e))