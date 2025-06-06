import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI

from backend.vector_db_client import VectorDBClient

OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-08-01-preview")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt4o")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "ada002")

openai_client = None
if OPENAI_ENDPOINT and OPENAI_KEY:
    openai_client = AzureOpenAI(
        azure_endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_KEY,
        api_version=OPENAI_API_VERSION,
    )

app = FastAPI()

class QueryRequest(BaseModel):
    query_type: int
    question: Optional[str] = None
    filename: Optional[str] = None
    language: Optional[str] = "en"
    groups: Optional[List[str]] = []

class InsertRequest(BaseModel):
    index: str
    documents: List[dict]

@app.post("/query")
def handle_query(req: QueryRequest):
    client = VectorDBClient()

    if req.query_type == 99:
        resp = client.query(req.filename or "", index="legal-documents", top_k=1, filters={"filename": req.filename})
        return {"answer": {"Found": len(resp.get("results", [])) > 0}}

    if req.query_type == 3:
        if not req.question:
            raise HTTPException(status_code=400, detail="question required")
        vec = None
        if openai_client:
            vec = openai_client.embeddings.create(input=req.question, model=OPENAI_EMBEDDING_MODEL).data[0].embedding
        docs = client.query(req.question, vector=vec, index="legal-documents", top_k=3,
                             filters={"groups": ",".join(req.groups or [])})
        answer = ""
        if openai_client:
            context = "\n".join(d.get("paragraph", "") for d in docs.get("results", []))
            completion = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": "Answer the user question"},
                         {"role": "user", "content": f"Question: {req.question}\nContext:{context}"}],
            )
            answer = completion.choices[0].message.content
        return {"answer": {"Answer": answer, "SearchResults": docs.get("results", [])}}

    if req.query_type == 2:
        if not req.question:
            raise HTTPException(status_code=400, detail="question required")
        vec = None
        if openai_client:
            vec = openai_client.embeddings.create(input=req.question, model=OPENAI_EMBEDDING_MODEL).data[0].embedding
        pol = client.query(req.question, vector=vec, index="legal-instructions", top_k=3,
                           filters={"groups": ",".join(req.groups or [])})
        summary = ""
        if openai_client:
            text = str(pol.get("results", []))
            completion = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": "Review text with policy"},
                         {"role": "user", "content": f"Text:{req.question}\nPolicies:{text}"}],
            )
            summary = completion.choices[0].message.content
        return {"answer": {"PolicyItems": pol.get("results", []), "summary": summary}}

    if req.query_type == 1:
        docs = client.query("*", index="legal-documents", top_k=1000)
        summary = ""
        if openai_client:
            completion = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": "Summarize document"},
                         {"role": "user", "content": str(docs.get("results", []))}],
            )
            summary = completion.choices[0].message.content
        results = [
            {
                "title": d.get("title"),
                "summary": d.get("summary"),
                "keyphrases": d.get("keyphrases"),
            }
            for d in docs.get("results", [])
        ]
        return {"answer": results, "full_summary": summary}

    raise HTTPException(status_code=400, detail="unsupported query_type")

@app.post("/insert")
def handle_insert(req: InsertRequest):
    client = VectorDBClient()
    return client.insert(req.documents, index=req.index)


