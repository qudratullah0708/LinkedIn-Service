from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class Lead(BaseModel):
    name: str | None = Field(None, description="Name of the Person")
    title: str | None = Field(None, description="Job title of the lead")
    organization: str | None = Field(None, description="Organization the lead belongs to")
    email: str | None = Field(None, description="Email address of the lead")
    phone: str | None = Field(None, description="Phone number of the lead")
    url: str | None = Field(None, description="Source from where the lead was obtained")
    location: str | None = Field(None, description="Location of the lead")


class Leads(BaseModel):
    leads: List[Lead]



class QueryRequest(BaseModel):
    query: str