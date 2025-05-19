from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from dotenv import load_dotenv
from tavily_search import Retrieve_news
from models import Lead , Leads
from groq import Groq
import instructor
import re
import os
import json
load_dotenv()

groq_client = instructor.from_groq(Groq())

def enrich_query(query: str) -> str:
    # Remove generic verbs
    query = re.sub(r"\b(find|search|scrape|extract)\b", "", query, flags=re.IGNORECASE).strip()
    if not any(term in query.lower() for term in ["linkedin", "twitter", "crunchbase", "founder"]):
        return query + " LinkedIn"
    return query


def Output_Parser(query: str) -> List[Lead]:

    print("\n\n****Retrieving Results***")

    
    new_query = enrich_query(query)
    print(new_query)
    results = Retrieve_news(new_query)
    
    print("\n\n****Extracting Leads From Content ***")
    
    prompt = f"""
    You are a professional B2B lead extraction agent. 
    Extract **people in sales, marketing, product, or leadership roles** from the text below.
    Return your result as a **JSON array of lead objects only**. Do not include anything else — no introduction, no explanation.    
    ### Input:
    {results}
### Task:
Extract individual leads **related to the query below**, from the given content. Each lead should include name, title, organization, and source (if available). Only include leads that are highly relevant to the user's query.
### Query:
{query}

"""
    
    completion = groq_client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        response_model=Leads,
        messages=[{"role": "user", "content": prompt}]
    )
    # print(completion)
     # Assuming completion.leads is a list of Lead objects
    if completion.leads:
        print(completion.leads)
        if all(lead.name is None and lead.title is None for lead in completion.leads):
          raise ValueError("No specific leads extracted for the given query.")
        return completion.leads  # This will be the list of leads extracted from the content
    else:
        raise ValueError("No leads were extracted.")



# @app.post("/extract-leads", response_model=Leads)
# async def extract_leads(content: str, query: str):
#     try:
#         # Call the Output_Parser function
#         leads = Output_Parser(content, query)
#         # return {"leads": leads}  # Return the leads directly as a dictionary
#         return Leads(leads=leads)
#     except Exception as e:
#         # If any error occurs, return an HTTP 400 Bad Request response
#         raise HTTPException(status_code=400, detail=str(e))
    